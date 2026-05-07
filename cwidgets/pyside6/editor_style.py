"""
editor_style.py - Formatting layer

Handles: colors, fonts, alignment, read-only mode.
Inherits from EditorCore for basic operations.
"""

import ctypes
import ctypes.wintypes
import re
import logging

import win32gui
import win32con

from .editor_core import EditorCore

# ============================================================================
# Logger for this module
# ============================================================================
logger = logging.getLogger("cwidgets")

# ============================================================================
# RichEdit constants for CHARFORMAT2
# ============================================================================
CFM_BOLD = 0x00000001
CFM_ITALIC = 0x00000002
CFM_CHARSET = 0x00000008
CFM_COLOR = 0x40000000
CFM_FACE = 0x20000000
CFM_SIZE = 0x80000000
CFE_BOLD = 0x00000001
CFE_ITALIC = 0x00000002

# ============================================================================
# RichEdit constants for PARAFORMAT2
# ============================================================================
EM_SETBKGNDCOLOR = 0x0443
EM_SETCHARFORMAT = 0x0444
EM_SETPARAFORMAT = 0x0447
EM_SETSEL = 0x00B1
EM_SCROLLCARET = 0x00B7
SCF_ALL = 0x0004
SCF_SELECTION = 0x0001
PFM_ALIGNMENT = 0x0008
PFA_LEFT = 1
PFA_CENTER = 3
PFA_RIGHT = 2

VALID_ALIGNMENTS = {
    'left': PFA_LEFT,
    'center': PFA_CENTER,
    'right': PFA_RIGHT,
}

# Arabic detection for auto alignment
UNICODE_ARABIC_START = 0x0600
UNICODE_ARABIC_END = 0x06FF

# ============================================================================
# Win32 structures (defined once)
# ============================================================================
class CHARFORMAT2(ctypes.Structure):
    """CHARFORMAT2 structure for character formatting in RichEdit."""
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwMask", ctypes.c_uint),
        ("dwEffects", ctypes.c_uint),
        ("yHeight", ctypes.c_int),
        ("yOffset", ctypes.c_int),
        ("crTextColor", ctypes.c_uint),
        ("bCharSet", ctypes.c_byte),
        ("bPitchAndFamily", ctypes.c_byte),
        ("szFaceName", ctypes.c_wchar * 32),
        ("wWeight", ctypes.c_ushort),
        ("sSpacing", ctypes.c_short),
        ("crBackColor", ctypes.c_uint),
        ("lcid", ctypes.c_uint),
        ("dwReserved", ctypes.c_uint),
        ("sStyle", ctypes.c_short),
        ("wKerning", ctypes.c_ushort),
        ("bUnderlineType", ctypes.c_byte),
        ("bAnimation", ctypes.c_byte),
        ("bRevAuthor", ctypes.c_byte),
        ("bReserved1", ctypes.c_byte),
    ]

class PARAFORMAT2(ctypes.Structure):
    """PARAFORMAT2 structure for paragraph formatting in RichEdit."""
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwMask", ctypes.c_uint),
        ("wNumbering", ctypes.c_ushort),
        ("wEffects", ctypes.c_ushort),
        ("dxStartIndent", ctypes.c_int),
        ("dxRightIndent", ctypes.c_int),
        ("dxOffset", ctypes.c_int),
        ("wAlignment", ctypes.c_ushort),
        ("cTabCount", ctypes.c_short),
        ("rgxTabs", ctypes.c_int * 32),
        ("dySpaceBefore", ctypes.c_int),
        ("dySpaceAfter", ctypes.c_int),
        ("dyLineSpacing", ctypes.c_int),
        ("sStyle", ctypes.c_short),
        ("bLineSpacingRule", ctypes.c_ubyte),
        ("bOutlineLevel", ctypes.c_ubyte),
        ("wShadingWeight", ctypes.c_ushort),
        ("wShadingStyle", ctypes.c_ushort),
        ("wNumberingStart", ctypes.c_ushort),
        ("wNumberingStyle", ctypes.c_ushort),
        ("wNumberingTab", ctypes.c_ushort),
        ("wBorderSpace", ctypes.c_ushort),
        ("wBorderWidth", ctypes.c_ushort),
        ("wBorders", ctypes.c_ushort),
    ]

# ============================================================================
# Optimized SendMessage
# ============================================================================
_user32 = ctypes.windll.user32
_user32.SendMessageW.argtypes = [ctypes.wintypes.HWND, ctypes.c_uint,
                                  ctypes.c_longlong, ctypes.c_void_p]
_user32.SendMessageW.restype = ctypes.c_longlong

def _send_message(hwnd, msg, wparam, lparam):
    """Sends a Windows message in an optimized way."""
    return _user32.SendMessageW(hwnd, msg, wparam, lparam)

# ============================================================================
# Main class
# ============================================================================
class EditorStyle(EditorCore):
    """
    Manages text formatting in the RichEdit control.

    Inherits from EditorCore and adds:
        - Font management (family, size, bold, italic)
        - Color management (text and background)
        - Alignment management (left, center, right, auto)
        - Read-only mode management
        - Automatic style reapplication after set_text() or clear()
    """

    def __init__(self):
        """Initializes the style manager with default values."""
        super().__init__()
        self._readonly = False
        self._bg_color = (255, 255, 255)   # white
        self._text_color = (0, 0, 0)       # black
        self._alignment = 'auto'
        self._font_name = ''
        self._font_size = 11
        self._font_bold = False
        self._font_italic = False
        self._pf_cache = PARAFORMAT2()      # cache reused for performance

    # ------------------------------------------------------------------
    # Color conversion utility method
    # ------------------------------------------------------------------
    @staticmethod
    def parse_color(color):
        """
        Converts a color to RGB tuple (r, g, b).

        Accepts:
            - Name: "red", "blue", "black", etc.
            - Tuple/list: (255, 0, 0)

        Args:
            color (str or tuple): Color to convert

        Returns:
            tuple: (r, g, b) with each component between 0 and 255

        Raises:
            ValueError: If the color is unknown or format is invalid
        """
        COLOR_NAMES = {
            "black": (0, 0, 0), "white": (255, 255, 255),
            "red": (255, 0, 0), "green": (0, 255, 0),
            "blue": (0, 0, 255), "yellow": (255, 255, 0),
            "cyan": (0, 255, 255), "magenta": (255, 0, 255),
            "gray": (128, 128, 128), "darkgray": (64, 64, 64),
            "lightgray": (192, 192, 192), "orange": (255, 165, 0),
            "purple": (128, 0, 128), "violet": (238, 130, 238),
            "pink": (255, 192, 203), "brown": (165, 42, 42),
            "navy": (0, 0, 128), "teal": (0, 128, 128),
            "lime": (0, 255, 0), "olive": (128, 128, 0),
            "maroon": (128, 0, 0), "coral": (255, 127, 80),
            "salmon": (250, 128, 114), "gold": (255, 215, 0),
            "silver": (192, 192, 192),
        }

        if isinstance(color, str):
            color_lower = color.lower()
            if color_lower in COLOR_NAMES:
                return COLOR_NAMES[color_lower]
            raise ValueError(f"Unknown color: '{color}'")
        elif isinstance(color, (tuple, list)) and len(color) == 3:
            return tuple(color)
        raise ValueError(f"Invalid color format: {color}")

    # ------------------------------------------------------------------
    # Validity check
    # ------------------------------------------------------------------
    def _is_valid(self):
        """Checks if the control handle is still valid."""
        return self.edit_hwnd is not None

    # ------------------------------------------------------------------
    # Text operations (append, clear, set_text)
    # ------------------------------------------------------------------
    def append(self, text):
        """
        Appends text to the end of the document.

        Args:
            text (str): Text to append (line breaks are normalized to \r\n)
        """
        if not self._is_valid():
            return

        try:
            length = win32gui.SendMessage(self.edit_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
            prefix = "\r\n" if length > 0 else ""
            formatted_text = prefix + text.replace("\n", "\r\n")

            win32gui.SendMessage(self.edit_hwnd, win32con.EM_SETSEL, -1, -1)
            _send_message(self.edit_hwnd, win32con.EM_REPLACESEL, True, formatted_text)

            new_len = win32gui.SendMessage(self.edit_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
            win32gui.SendMessage(self.edit_hwnd, win32con.EM_SETSEL, new_len, new_len)
            win32gui.SendMessage(self.edit_hwnd, win32con.EM_SCROLLCARET, 0, 0)
            self._saved_sel = (new_len, new_len)

        except Exception as e:
            logger.exception("Error in append")

    def clear(self):
        """Clears all content and reapplies styles."""
        if not self._is_valid():
            return

        try:
            win32gui.SetWindowText(self.edit_hwnd, "")
        except Exception as e:
            logger.exception("Error in clear")
            return

        self._reapply_styles()

    def set_text(self, text: str):
        """
        Sets the complete text and reapplies styles.

        Args:
            text (str): New text (line breaks \n are converted to \r\n)
        """
        if not self._is_valid():
            return

        try:
            if '\n' in text and '\r\n' not in text:
                text = text.replace('\n', '\r\n')
            win32gui.SetWindowText(self.edit_hwnd, text)
        except Exception as e:
            logger.exception("Error in set_text")
            return

        self._reapply_styles()

    # ------------------------------------------------------------------
    # Style application (called after set_text, clear)
    # ------------------------------------------------------------------
    def _reapply_styles(self):
        """Reapplies all styles after text change."""
        if not self._is_valid():
            return

        self._apply_bg_color()
        self._apply_charformat()
        self._apply_alignment()
        self._apply_readonly()

    # ------------------------------------------------------------------
    # Font and text attributes
    # ------------------------------------------------------------------
    def _apply_charformat(self):
        """Applies font and attributes to all text."""
        if not self._is_valid():
            return

        try:
            r, g, b = self._text_color

            cf = CHARFORMAT2()
            cf.cbSize = ctypes.sizeof(CHARFORMAT2)
            cf.dwMask = CFM_COLOR | CFM_SIZE | CFM_BOLD | CFM_ITALIC
            cf.crTextColor = r | (g << 8) | (b << 16)
            cf.yHeight = self._font_size * 20   # conversion points → twips

            if self._font_name:
                cf.dwMask |= CFM_FACE | CFM_CHARSET
                cf.szFaceName = self._font_name[:31]
                cf.bCharSet = 0

            if self._font_bold:
                cf.dwEffects |= CFE_BOLD
            if self._font_italic:
                cf.dwEffects |= CFE_ITALIC

            _send_message(self.edit_hwnd, EM_SETCHARFORMAT, SCF_ALL, ctypes.addressof(cf))

        except Exception as e:
            logger.exception("Error in _apply_charformat")

    def set_font(self, name: str, size: int, bold: bool = False, italic: bool = False):
        """
        Sets the text font.

        Args:
            name (str): Font name (ex: "Arial", "Segoe UI")
            size (int): Size in points (minimum forced to 12 for NVDA readability)
            bold (bool): True for bold
            italic (bool): True for italic
        """
        if not name or not name.strip() or size <= 0:
            return

        self._font_size = max(int(size), 12)
        self._font_name = name
        self._font_bold = bool(bold)
        self._font_italic = bool(italic)

        if self._is_valid():
            self._apply_charformat()

    # ------------------------------------------------------------------
    # Text color
    # ------------------------------------------------------------------
    def set_text_color(self, *args):
        """
        Sets the text color.

        Usage:
            set_text_color(255, 0, 0)   # RGB
            set_text_color("red")       # color name

        Args:
            *args: Either 1 color name, or 3 RGB integers

        Raises:
            ValueError: If the number of arguments is invalid or color unknown
        """
        if len(args) == 1:
            r, g, b = self.parse_color(args[0])
        elif len(args) == 3:
            r, g, b = args
        else:
            raise ValueError("set_text_color expects 1 name or 3 RGB integers")

        self._validate_rgb(r, g, b)
        self._text_color = (r, g, b)
        if self._is_valid():
            self._apply_charformat()

    # ------------------------------------------------------------------
    # Background color
    # ------------------------------------------------------------------
    def set_background_color(self, *args):
        """
        Sets the editor background color.

        Usage:
            set_background_color(255, 255, 255)   # RGB
            set_background_color("white")         # color name

        Args:
            *args: Either 1 color name, or 3 RGB integers

        Raises:
            ValueError: If the number of arguments is invalid or color unknown
        """
        if len(args) == 1:
            r, g, b = self.parse_color(args[0])
        elif len(args) == 3:
            r, g, b = args
        else:
            raise ValueError("set_background_color expects 1 name or 3 RGB integers")

        self._validate_rgb(r, g, b)
        self._bg_color = (r, g, b)
        if self._is_valid():
            self._apply_bg_color()

    def _apply_bg_color(self):
        """Applies the background color to the control."""
        try:
            r, g, b = self._bg_color
            _send_message(self.edit_hwnd, EM_SETBKGNDCOLOR, 0, r | (g << 8) | (b << 16))
        except Exception as e:
            logger.exception("Error in _apply_bg_color")

    # ------------------------------------------------------------------
    # Alignment
    # ------------------------------------------------------------------
    def set_alignment(self, alignment: str):
        """
        Sets the text alignment.

        Args:
            alignment (str): 'left', 'center', 'right' or 'auto'
                'auto' detects Arabic and aligns right
        """
        if alignment not in VALID_ALIGNMENTS and alignment != 'auto':
            alignment = 'auto'
        self._alignment = alignment
        if self._is_valid():
            self._apply_alignment()

    def _detect_paragraph_alignment(self, paragraph: str) -> int:
        """
        Detects if the paragraph is Arabic (then right alignment).

        Args:
            paragraph (str): Paragraph text

        Returns:
            int: PFA_RIGHT for Arabic, PFA_LEFT otherwise
        """
        for ch in paragraph:
            if ch.isalpha():
                if UNICODE_ARABIC_START <= ord(ch) <= UNICODE_ARABIC_END:
                    return PFA_RIGHT
                return PFA_LEFT
        return PFA_LEFT

    def _apply_alignment(self):
        """Applies alignment to all paragraphs."""
        try:
            full_text = self.get_text()
            if not full_text:
                return

            paragraphs = re.split(r'\r?\n|\r', full_text)

            pf = self._pf_cache
            pf.cbSize = ctypes.sizeof(PARAFORMAT2)
            pf.dwMask = PFM_ALIGNMENT

            pos = 0
            for para in paragraphs:
                para_len = len(para)

                if self._alignment == 'auto':
                    align = self._detect_paragraph_alignment(para) if para_len > 0 else PFA_LEFT
                elif self._alignment == 'center':
                    align = PFA_CENTER
                elif self._alignment == 'right':
                    align = PFA_RIGHT
                else:
                    align = PFA_LEFT

                if para_len > 0:
                    win32gui.SendMessage(self.edit_hwnd, EM_SETSEL, pos, pos + para_len)
                    pf.wAlignment = align
                    _send_message(self.edit_hwnd, EM_SETPARAFORMAT, 0, ctypes.addressof(pf))

                pos += para_len + 1

        except Exception as e:
            logger.exception("Error in _apply_alignment")

    # ------------------------------------------------------------------
    # Read-only mode
    # ------------------------------------------------------------------
    def set_readonly(self, readonly: bool):
        """
        Enables or disables read-only mode.

        Args:
            readonly (bool): True for read-only, False for edit mode
        """
        self._readonly = bool(readonly)
        if self._is_valid():
            self._apply_readonly()

    def _apply_readonly(self):
        """Applies read-only mode to the control."""
        try:
            _send_message(self.edit_hwnd, win32con.EM_SETREADONLY, int(self._readonly), 0)
        except Exception as e:
            logger.exception("Error in _apply_readonly")

    # ------------------------------------------------------------------
    # RGB validation
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_rgb(r, g, b):
        """
        Validates that RGB values are valid (0-255).

        Args:
            r, g, b (int): RGB components

        Raises:
            ValueError: If a value is out of range or not an integer
        """
        for val in (r, g, b):
            if not isinstance(val, int) or not (0 <= val <= 255):
                raise ValueError(f"Invalid RGB: {val}")
