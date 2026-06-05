#cwidgets/pyqt6/ctextedit_methods.py
"""
ctextedit_methods.py - Extended methods for CTextEdit

Contains additional public methods not present in the base CTextEdit class.
Designed as a mixin to be inherited by CTextEdit.
"""

import re
import win32gui
import win32con
import ctypes

WM_COPY  = 0x0301
WM_CUT   = 0x0300
WM_PASTE = 0x0302
WM_UNDO  = 0x0304
EM_REDO = 0x0454

class CTextEditMethods:
    """
    Mixin class providing extended methods for CTextEdit.
    Requires self.core (EditorStyle instance) to be available.
    """

    # ------------------------------------------------------------------ #
    #  Properties                                                         #
    # ------------------------------------------------------------------ #

    def isReadOnly(self) -> bool:
        """
        Returns True if the editor is in read-only mode.

        Returns:
            bool: True if read-only, False if editable

        Example:
            if editor.isReadOnly():
                print("read-only")
        """
        if self.core:
            return self.core._readonly
        for name, args in reversed(self.pending_styles):
            if name == 'set_readonly':
                return args[0]
        return False

    # ------------------------------------------------------------------ #
    #  Content                                                            #
    # ------------------------------------------------------------------ #

    def insertPlainText(self, text: str):
        """
        Inserts plain text at the current cursor position.
        Existing text is not erased.

        Args:
            text (str): Text to insert

        Example:
            editor.insertPlainText("Inserted text\\n")
        """
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(
                self.core.edit_hwnd,
                win32con.EM_REPLACESEL,
                True,
                text
            )

    def insertHtml(self, html: str):
        """
        Extracts plain text from HTML content and inserts it
        at the current cursor position.

        HTML tags are removed. <br> and <p> tags are converted to line breaks.
        Formatting is then applied via setFont(), setTextColor(), setAlignment().

        Args:
            html (str): HTML content to insert

        Example:
            editor.insertHtml("<p>Hello <b>world</b></p>")
            # inserts: "Hello world"

            editor.insertHtml("<p>Line 1</p><br/>Line 2")
            # inserts: "Line 1\\nLine 2"

        Note:
            toHtml() and setHtml() are not supported —
            Win32 RichEdit uses RTF format, not HTML.
        """
        text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
        text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.strip()
        if text and self.core and self.core.edit_hwnd:
            win32gui.SendMessage(
                self.core.edit_hwnd,
                win32con.EM_REPLACESEL,
                True,
                text
            )

    def selectAll(self):
        """
        Selects all text in the editor.

        Example:
            editor.selectAll()
            text = editor.selectedText()  # retrieves all text
        """
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(
                self.core.edit_hwnd,
                win32con.EM_SETSEL,
                0, -1
            )

    def selectedText(self) -> str:
        """
        Returns the selected text.
        Returns an empty string if no selection.

        Returns:
            str: Selected text or empty string

        Example:
            editor.selectAll()
            text = editor.selectedText()
            print(text)
        """
        if not self.core or not self.core.edit_hwnd:
            return ""

        sel = win32gui.SendMessage(
            self.core.edit_hwnd, win32con.EM_GETSEL, 0, 0
        )
        start = sel & 0xFFFF
        end   = (sel >> 16) & 0xFFFF

        if start == end:
            return ""

        length = end - start
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.SendMessageW(
            self.core.edit_hwnd, 0x043E, 0, buf  # EM_GETSELTEXT
        )
        # Normalize \r to \n
        return buf.value.replace('\r', '\n')

    def lineCount(self) -> int:
        """
        Returns the number of lines in the editor.

        Returns:
            int: Number of lines, 0 if editor not initialized

        Example:
            count = editor.lineCount()
            print(f"Number of lines: {count}")
        """
        if self.core and self.core.edit_hwnd:
            return win32gui.SendMessage(
                self.core.edit_hwnd,
                win32con.EM_GETLINECOUNT,
                0, 0
            )
        return 0

    # ------------------------------------------------------------------ #
    #  Clipboard                                                         #
    # ------------------------------------------------------------------ #

    def copy(self):
        """Copies the selection to the clipboard."""
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(self.core.edit_hwnd, WM_COPY, 0, 0)

    def cut(self):
        """Cuts the selection."""
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(self.core.edit_hwnd, WM_CUT, 0, 0)

    def paste(self):
        """Pastes content from the clipboard."""
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(self.core.edit_hwnd, WM_PASTE, 0, 0)

    def undo(self):
        """Undoes the last action."""
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(self.core.edit_hwnd, WM_UNDO, 0, 0)

    def redo(self):
        """Redoes the last undone action."""
        if self.core and self.core.edit_hwnd:
            win32gui.SendMessage(self.core.edit_hwnd, EM_REDO, 0, 0)