"""
editor_core.py - Low-level Win32 layer

Handles creation, subclassing and basic operations on the RICHEDIT20W control.
This module is Qt-independent and only depends on win32gui and ctypes.
"""

import sys
import ctypes
from ctypes import wintypes
import logging
import win32gui
import win32con

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Resolve user32 functions with explicit signatures
user32 = ctypes.windll.user32

user32.AttachThreadInput.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_bool]
user32.AttachThreadInput.restype = ctypes.c_bool

user32.GetWindowThreadProcessId.restype = ctypes.c_uint
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.c_void_p]

user32.IsWindow.argtypes = [wintypes.HWND]
user32.IsWindow.restype = ctypes.c_bool

user32.PostMessageW.argtypes = [wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM]
user32.PostMessageW.restype = ctypes.c_bool

user32.NotifyWinEvent.argtypes = [ctypes.c_uint, wintypes.HWND, ctypes.c_long, ctypes.c_long]
user32.NotifyWinEvent.restype = None

# SetWindowLongPtrW - required for 64-bit subclassing
WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.c_longlong,
    wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM
)

CallWindowProcW = user32.CallWindowProcW
CallWindowProcW.restype = ctypes.c_longlong
CallWindowProcW.argtypes = [ctypes.c_longlong, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM]

SetWindowLongPtrW = user32.SetWindowLongPtrW
SetWindowLongPtrW.restype = ctypes.c_int64
SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int64]

# Constants
EVENT_OBJECT_FOCUS = 0x8005
EM_SETLANGOPTIONS = win32con.WM_USER + 120
EM_GETLANGOPTIONS = win32con.WM_USER + 121
IMF_AUTOKEYBOARD = 0x0001
MAX_TEXT_LENGTH = 10_000_000  # Safeguard: 10 MB

# Logger for this module
logger = logging.getLogger("cwidgets")
logger.debug(f"logger initialized in {__file__}")


class EditorCore:
    """
    Creates and manages a native Win32 RICHEDIT20W control embedded in a Qt window.

    This class handles:
    - Creating the RichEdit control with appropriate styles
    - Installing subclassing to capture Windows messages
    - Managing keyboard shortcuts (Tab, Ctrl+Home, Shift+End, etc.)
    - Saving/restoring selection during focus changes
    - Disabling automatic keyboard language switching
    - Providing an accessible name to NVDA via an invisible STATIC label
    """
    # shared across all instances — one subclass per window
    _subclassed_windows = {}      
    # last editor that had focus before Alt+Tab
    _last_focused_editor = None   

    def __init__(self):
        """
        Initializes the RichEdit manager.

        Attributes:
            edit_hwnd (int): Win32 handle of the RichEdit control
            _label_hwnd (int): Handle of the STATIC label for NVDA accessibility
            old_edit_proc (int): Original WndProc of the control (for restoration)
            _tab_callback (callable): Function called when Tab is pressed (Qt navigation)
            _had_focus (bool): Indicates if the editor has ever received focus
            _main_hwnd (int): Handle of the main Qt window
            _old_main_proc (int): Original WndProc of the main window
            _new_main_proc (WNDPROC): New WndProc of the main window
            _focus_callback (callable): Function called when the app regains focus
            _saved_sel (tuple): Last saved cursor position (start, end)
            _dll_handle (int): Handle of loaded riched20.dll
        """
        self.edit_hwnd = None
        self._label_hwnd = None
        self.old_edit_proc = None
        self._tab_callback = lambda forward: None
        self._had_focus = False
        self._main_hwnd = None
        self._old_main_proc = None
        self._new_main_proc = None
        self._focus_callback = None
        self._saved_sel = (0, 0)
        self._cleaned_up = False  
        
        
        # Load riched20.dll
        self._dll_handle = ctypes.windll.kernel32.LoadLibraryW("riched20.dll")
        if not self._dll_handle:
            err = ctypes.GetLastError()
            raise RuntimeError(
                f"[EditorCore] Failed to load riched20.dll "
                f"(Win32 error: {err})"
            )
        logger.debug("riched20.dll loaded successfully")

    def create(self, parent_hwnd, x, y, width, height, text="", accessible_name=""):
        """
        Creates the RICHEDIT20W control in the parent window.

        Args:
            parent_hwnd (int): Win32 handle of the Qt parent widget
            x (int): Initial horizontal position
            y (int): Initial vertical position
            width (int): Initial width
            height (int): Initial height
            text (str): Initial text (optional)
            accessible_name (str): Name announced by NVDA when the editor receives focus

        Returns:
            int: Win32 handle of the created RichEdit control

        Raises:
            RuntimeError: If creation fails
        """
        if not user32.IsWindow(parent_hwnd):
            raise RuntimeError(
                f"[EditorCore] create(): invalid parent handle ({parent_hwnd})"
            )

        # Invisible static label for NVDA accessibility
        if accessible_name:
            self._label_hwnd = win32gui.CreateWindowEx(
                0,
                "STATIC",
                accessible_name,
                win32con.WS_CHILD | win32con.SS_LEFT,
                0, 0, 0, 0,
                parent_hwnd, 0, 0, None
            )
            logger.debug(f"STATIC label created with name: {accessible_name}")

        self.edit_hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_CLIENTEDGE,
            "RICHEDIT20W",
            "",
            (win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.ES_MULTILINE |
             win32con.WS_TABSTOP | win32con.WS_VSCROLL | win32con.ES_NOHIDESEL),
            x, y, width, height,
            parent_hwnd, 1, 0, None
        )

        if not self.edit_hwnd:
            err = ctypes.GetLastError()
            logger.error(f"CreateWindowEx failed: error {err}")
            raise RuntimeError(
                f"[EditorCore] CreateWindowEx (RICHEDIT20W) failed "
                f"(Win32 error: {err})"
            )
        logger.debug("RichEdit control created successfully")

        # Disable automatic keyboard language switching
        try:
            lang_options = win32gui.SendMessage(self.edit_hwnd, EM_GETLANGOPTIONS, 0, 0)
            lang_options &= ~IMF_AUTOKEYBOARD
            win32gui.SendMessage(self.edit_hwnd, EM_SETLANGOPTIONS, 0, lang_options)
        except Exception as e:
            logger.exception("Error disabling IMF_AUTOKEYBOARD")

        # Subclass the control to capture keyboard messages
        self.old_edit_proc = win32gui.SetWindowLong(
            self.edit_hwnd, win32con.GWL_WNDPROC, self._subclass_proc
        )
        if not self.old_edit_proc:
            err = ctypes.GetLastError()
            logger.error(f"SetWindowLong (subclassing) failed: error {err}")
            raise RuntimeError(
                f"[EditorCore] SetWindowLong (control subclassing) failed "
                f"(Win32 error: {err})"
            )
        logger.debug("RichEdit control subclassing installed")

        win32gui.SendMessage(self.edit_hwnd, win32con.EM_SETSEL, 0, 0)
        return self.edit_hwnd

    def _subclass_proc(self, hwnd, msg, wparam, lparam):
        """
        Substitute WndProc to capture control messages.

        Args:
            hwnd (int): Window handle
            msg (int): Windows message
            wparam (int): wParam message parameter
            lparam (int): lParam message parameter

        Returns:
            int: Message processing result
        """
        try:
            return self._handle_edit_msg(hwnd, msg, wparam, lparam)
        except Exception as e:
            logger.exception("Exception in _subclass_proc")
            return win32gui.CallWindowProc(self.old_edit_proc, hwnd, msg, wparam, lparam)

    def _handle_edit_msg(self, hwnd, msg, wparam, lparam):
        """
        Processes Windows messages from the RichEdit control.

        Args:
            hwnd (int): Window handle
            msg (int): Windows message
            wparam (int): wParam message parameter
            lparam (int): lParam message parameter

        Returns:
            int: Message result (0 if processed, otherwise call to original WndProc)
        """
        # Block automatic keyboard language switching
        if msg == 0x0051:  # WM_IME_NOTIFY
            return 0

        if msg == win32con.WM_KILLFOCUS:
            self._save_selection(hwnd)

        if msg == win32con.WM_SETFOCUS:
            self._had_focus = True
            self._disable_autokeyboard(hwnd)
            self._restore_selection(hwnd)

        elif msg == win32con.WM_CHAR:
            # Tab alone (without Ctrl) -> do nothing
            if wparam == 0x09:
                ctrl = user32.GetKeyState(0x11) & 0x8000
                if not ctrl:
                    return 0

        elif msg == win32con.WM_KEYDOWN:
            ctrl = user32.GetKeyState(win32con.VK_CONTROL) & 0x8000
            shift = user32.GetKeyState(win32con.VK_SHIFT) & 0x8000

            # Tab key handling
            if wparam == win32con.VK_TAB:
                if ctrl:
                    win32gui.SendMessage(hwnd, win32con.WM_CHAR, 0x09, 0)
                else:
                    self._transfer_focus_to_parent(hwnd)
                    if self._tab_callback:
                        self._tab_callback(not shift)
                return 0

            # Ctrl+Home: beginning of document
            if wparam == win32con.VK_HOME and ctrl and not shift:
                win32gui.SendMessage(hwnd, win32con.EM_SETSEL, 0, 0)
                return 0

            # Ctrl+End: end of document
            if wparam == win32con.VK_END and ctrl and not shift:
                length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
                win32gui.SendMessage(hwnd, win32con.EM_SETSEL, length, length)
                return 0

            # Shift+End: select to end of line
            if wparam == win32con.VK_END and shift and not ctrl:
                current_line = win32gui.SendMessage(hwnd, win32con.EM_LINEFROMCHAR, -1, 0)
                line_start = win32gui.SendMessage(hwnd, win32con.EM_LINEINDEX, current_line, 0)
                line_len = win32gui.SendMessage(hwnd, win32con.EM_LINELENGTH, -1, 0)
                sel = win32gui.SendMessage(hwnd, win32con.EM_GETSEL, 0, 0)
                start = sel & 0xFFFF
                end = line_start + line_len
                win32gui.SendMessage(hwnd, win32con.EM_SETSEL, start, end)
                return 0

            # Ctrl+Shift+Home: select to beginning of document
            if wparam == win32con.VK_HOME and ctrl and shift:
                sel = win32gui.SendMessage(hwnd, win32con.EM_GETSEL, 0, 0)
                end = (sel >> 16) & 0xFFFF
                win32gui.SendMessage(hwnd, win32con.EM_SETSEL, 0, end)
                return 0

            # Ctrl+Shift+End: select to end of document
            if wparam == win32con.VK_END and ctrl and shift:
                sel = win32gui.SendMessage(hwnd, win32con.EM_GETSEL, 0, 0)
                start = sel & 0xFFFF
                length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
                win32gui.SendMessage(hwnd, win32con.EM_SETSEL, start, length)
                return 0

            # Home alone: beginning of line
            if wparam == win32con.VK_HOME and not ctrl and not shift:
                current_line = win32gui.SendMessage(hwnd, win32con.EM_LINEFROMCHAR, -1, 0)
                line_start = win32gui.SendMessage(hwnd, win32con.EM_LINEINDEX, current_line, 0)
                win32gui.SendMessage(hwnd, win32con.EM_SETSEL, line_start, line_start)
                return 0

            # End alone: end of line
            if wparam == win32con.VK_END and not ctrl and not shift:
                current_pos = win32gui.SendMessage(hwnd, win32con.EM_LINEFROMCHAR, -1, 0)
                line_start = win32gui.SendMessage(hwnd, win32con.EM_LINEINDEX, current_pos, 0)
                line_len = win32gui.SendMessage(hwnd, win32con.EM_LINELENGTH, -1, 0)
                win32gui.SendMessage(
                    hwnd, win32con.EM_SETSEL,
                    line_start + line_len, line_start + line_len
                )
                return 0

            # Prevent arrow keys from leaving the text
            if wparam in (win32con.VK_UP, win32con.VK_DOWN):
                line_count = win32gui.SendMessage(hwnd, win32con.EM_GETLINECOUNT, 0, 0)
                current_line = win32gui.SendMessage(hwnd, win32con.EM_LINEFROMCHAR, -1, 0)
                if wparam == win32con.VK_UP and current_line == 0:
                    return 0
                if wparam == win32con.VK_DOWN and current_line == line_count - 1:
                    return 0

        return win32gui.CallWindowProc(self.old_edit_proc, hwnd, msg, wparam, lparam)

    def _disable_autokeyboard(self, hwnd):
        """
        Disables automatic keyboard language switching for this control.

        Args:
            hwnd (int): RichEdit control handle
        """
        try:
            lang_options = win32gui.SendMessage(hwnd, EM_GETLANGOPTIONS, 0, 0)
            lang_options &= ~IMF_AUTOKEYBOARD
            win32gui.SendMessage(hwnd, EM_SETLANGOPTIONS, 0, lang_options)
        except Exception as e:
            logger.exception("Error in _disable_autokeyboard")

    def _save_selection(self, hwnd):
        """
        Saves the cursor position before losing focus.

        Args:
            hwnd (int): RichEdit control handle
        """
        try:
            sel = win32gui.SendMessage(hwnd, win32con.EM_GETSEL, 0, 0)
            self._saved_sel = (sel & 0xFFFF, (sel >> 16) & 0xFFFF)
            logger.debug(f"Selection saved: {self._saved_sel}")
        except Exception as e:
            logger.exception("Error in _save_selection")

    def _restore_selection(self, hwnd):
        """
        Restores the cursor position after regaining focus.

        Args:
            hwnd (int): RichEdit control handle
        """
        try:
            start, end = self._saved_sel
            win32gui.SendMessage(hwnd, win32con.EM_SETSEL, start, end)
            logger.debug(f"Selection restored: ({start}, {end})")
        except Exception as e:
            logger.exception("Error in _restore_selection")

    def _transfer_focus_to_parent(self, hwnd):
        """
        Transfers Win32 focus to the parent window (for Tab navigation).

        Args:
            hwnd (int): RichEdit control handle
        """
        try:
            parent_hwnd = win32gui.GetParent(hwnd)
            tid_edit = user32.GetWindowThreadProcessId(hwnd, None)
            tid_parent = user32.GetWindowThreadProcessId(parent_hwnd, None)
            user32.AttachThreadInput(tid_edit, tid_parent, True)
            win32gui.SetFocus(parent_hwnd)
            user32.AttachThreadInput(tid_edit, tid_parent, False)
        except Exception as e:
            logger.exception("Error in _transfer_focus_to_parent")



    def subclass_main(self, main_hwnd, focus_callback):
        """
        Subclasses the main Qt window's WndProc to intercept WM_ACTIVATEAPP.
        Only subclasses once per window handle — subsequent editors register
        their callback without installing a new WndProc.

        Args:
            main_hwnd (int): Win32 handle of the main application window.
            focus_callback (callable): Called when the application regains focus.
        """
        if not user32.IsWindow(main_hwnd):
            logger.warning(f"subclass_main: invalid main window handle {main_hwnd}")
            return

        self._main_hwnd = main_hwnd
        self._focus_callback = focus_callback

        # window already subclassed by another editor — register callback only
        if main_hwnd in EditorCore._subclassed_windows:
            EditorCore._subclassed_windows[main_hwnd]['callbacks'].append(focus_callback)
            # share the existing proc references with this editor
            self._old_main_proc = EditorCore._subclassed_windows[main_hwnd]['old_proc']
            self._new_main_proc = EditorCore._subclassed_windows[main_hwnd]['new_proc']
            logger.debug(f"subclass_main: callback registered for existing subclass hwnd={main_hwnd}")
            return

        # first editor for this window — install the subclass
        def main_proc(hwnd, msg, wparam, lparam):
            try:
                if msg == win32con.WM_ACTIVATEAPP and wparam == 1:
                    # restore focus to the last editor that had focus before Alt+Tab
                    last = EditorCore._last_focused_editor
                    if last and last._focus_callback:
                        QTimer.singleShot(50, last._focus_callback)
            except Exception:
                logger.exception("main_proc: error handling WM_ACTIVATEAPP")

            # always forward to the original WndProc
            entry = EditorCore._subclassed_windows.get(main_hwnd)
            if entry and entry['old_proc']:
                return CallWindowProcW(entry['old_proc'], hwnd, msg, wparam, lparam)
            return 0

        new_proc = WNDPROC(main_proc)
        addr = ctypes.cast(new_proc, ctypes.c_void_p).value
        old_proc = SetWindowLongPtrW(main_hwnd, -4, ctypes.c_int64(addr).value)

        if not old_proc:
            logger.error("subclass_main: SetWindowLongPtrW failed for hwnd={main_hwnd}")
            return

        # register in the class-level dictionary shared across all instances
        EditorCore._subclassed_windows[main_hwnd] = {
            'old_proc': old_proc,
            'new_proc': new_proc,
            'callbacks': [focus_callback]
        }

        # store proc references for this editor instance
        self._old_main_proc = old_proc
        self._new_main_proc = new_proc

        logger.debug(f"subclass_main: WndProc installed for hwnd={main_hwnd}")



    def _is_valid(self):
        """
        Checks if the control handle is still valid.

        Returns:
            bool: True if the control is valid, False otherwise
        """
        return bool(self.edit_hwnd and user32.IsWindow(self.edit_hwnd))

    def set_text(self, text):
        """
        Replaces all content in the editor.

        Args:
            text (str): New text
        """
        if not self._is_valid():
            logger.warning("set_text called while control is not valid")
            return
        try:
            win32gui.SetWindowText(self.edit_hwnd, text)
        except Exception as e:
            logger.exception("Error in set_text")

    def get_text(self):
        """
        Returns all content from the editor.

        Returns:
            str: Complete text, or empty string on error
        """
        if not self._is_valid():
            logger.warning("get_text called while control is not valid")
            return ""
        try:
            length = win32gui.SendMessage(self.edit_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
            if length == 0:
                return ""
            if length > MAX_TEXT_LENGTH:
                logger.warning(f"Text too long: {length} characters, limited to {MAX_TEXT_LENGTH}")
                return ""
            buf = ctypes.create_unicode_buffer(length + 1)
            win32gui.SendMessage(self.edit_hwnd, win32con.WM_GETTEXT, length + 1, buf)
            return buf.value
        except Exception as e:
            logger.exception("Error in get_text")
            return ""

    def clear(self):
        """
        Clears all content from the editor.
        """
        if not self._is_valid():
            logger.warning("clear called while control is not valid")
            return
        try:
            win32gui.SetWindowText(self.edit_hwnd, "")
        except Exception as e:
            logger.exception("Error in clear")

    def set_focus(self):
        """
        Gives focus to the RichEdit control and notifies NVDA.

        Sends an EVENT_OBJECT_FOCUS event after 100ms so NVDA announces the name.
        """
        EditorCore._last_focused_editor = self
        if not self._is_valid():
            logger.warning("set_focus called while control is not valid")
            return
        try:
            QApplication.processEvents()
            win32gui.SetFocus(self.edit_hwnd)
            user32.PostMessageW(self.edit_hwnd, win32con.WM_SETFOCUS, 0, 0)
            QTimer.singleShot(
                100,
                lambda: user32.NotifyWinEvent(EVENT_OBJECT_FOCUS, self.edit_hwnd, -4, 0)
            )
        except Exception as e:
            logger.exception("Error in set_focus")

    def resize(self, x, y, width, height):
        """
        Resizes the RichEdit control.

        Args:
            x (int): New horizontal position
            y (int): New vertical position
            width (int): New width
            height (int): New height
        """
        if not self._is_valid():
            return
        try:
            win32gui.MoveWindow(self.edit_hwnd, x, y, width, height, True)
        except Exception as e:
            logger.exception("Error in resize")


    
    def cleanup(self):
        """
        Restores original WndProcs, destroys the STATIC label and releases resources.
        Call this method before destroying the parent Qt widget.
        Handles shared subclassing — restores main WndProc only when last editor is cleaned up.
        """
        # avoid double cleanups
        if self._cleaned_up:
            logger.debug("cleanup already called, skipping")
            return
        self._cleaned_up = True

        logger.debug("cleanup called")

        # destroy STATIC label
        if self._label_hwnd:
            try:
                win32gui.DestroyWindow(self._label_hwnd)
                logger.debug("STATIC label destroyed")
            except Exception:
                logger.exception("Error destroying STATIC label")
            self._label_hwnd = None

        # restore RichEdit WndProc
        if self.old_edit_proc and self.edit_hwnd and user32.IsWindow(self.edit_hwnd):
            try:
                SetWindowLongPtrW(self.edit_hwnd, -4, self.old_edit_proc)
                logger.debug("RichEdit control procedure restored")
            except Exception:
                logger.exception("Error restoring old_edit_proc")

        # restore main window WndProc — only when last editor is cleaned up
        if self._main_hwnd and user32.IsWindow(self._main_hwnd):
            entry = EditorCore._subclassed_windows.get(self._main_hwnd)
            if entry:
                # remove this editor's callback from the shared list
                if self._focus_callback in entry['callbacks']:
                    entry['callbacks'].remove(self._focus_callback)
                    logger.debug("focus callback removed from shared subclass")
                # restore original WndProc only if no more editors registered
                if not entry['callbacks']:
                    try:
                        SetWindowLongPtrW(self._main_hwnd, -4, entry['old_proc'])
                        del EditorCore._subclassed_windows[self._main_hwnd]
                        logger.debug("main WndProc restored — last editor cleaned up")
                    except Exception:
                        logger.exception("Error restoring main WndProc")

        # clear last focused editor if it was this instance
        if EditorCore._last_focused_editor is self:
            EditorCore._last_focused_editor = None

        # free riched20.dll
        if self._dll_handle:
            try:
                ctypes.windll.kernel32.FreeLibrary(self._dll_handle)
                logger.debug("riched20.dll freed")
            except Exception:
                logger.exception("Error during FreeLibrary")

        self.old_edit_proc = None
        self._old_main_proc = None
        self._dll_handle = None
        self.edit_hwnd = None
        self._main_hwnd = None


    def __del__(self):
        """Destructor: clean up properly."""
        self.cleanup()

    def navigate_tab(self, forward: bool):
        """
        Navigates to the next/previous widget in the Qt hierarchy.

        Args:
            forward (bool): True for Tab (next), False for Shift+Tab (previous)
        """
        if not self.edit_hwnd:
            return

        try:
            tid_edit = user32.GetWindowThreadProcessId(self.edit_hwnd, None)
            parent_hwnd = win32gui.GetParent(self.edit_hwnd)
            tid_parent = user32.GetWindowThreadProcessId(parent_hwnd, None)

            user32.AttachThreadInput(tid_edit, tid_parent, True)
            win32gui.SetFocus(parent_hwnd)
            user32.AttachThreadInput(tid_edit, tid_parent, False)

            self._had_focus = False

            if self._tab_callback:
                self._tab_callback(forward)

        except Exception as e:
            logger.exception("Error in navigate_tab")
