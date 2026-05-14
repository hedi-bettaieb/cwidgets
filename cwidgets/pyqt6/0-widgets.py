# -*- coding: utf-8 -*-

"""
CWidgets: Qt widget library optimized for accessibility with NVDA.
PyQt6 version.

This library provides wrappers around standard PyQt6 widgets to ensure
proper screen reader feedback and keyboard navigation for users of
screen readers like NVDA.

Included classes:

- CTextEdit: Rich text editing control based on the Win32 RichEdit API, compatible with QTextEdit.

- CLabel: Text label that dynamically manages 'buddy' relationships for accessibility.

- CButton: Push button supporting activation via Enter and Space keys.

- CLineEdit: Single-line input field with explicit validation signal.

- CComboBox: Dropdown list optimized for smooth screen reader navigation.

- CListWidget: List widget optimized for accessible focus and selection.

- CMessageBox: Modal or timed dialog boxes with audio feedback.
"""

import logging

from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QPushButton, QComboBox, QListWidget,
    QMessageBox, QApplication, QWidget
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal as Signal
from PyQt6.QtGui import QFont, QKeyEvent

from .editor_style import EditorStyle
from .validate_parent import validate_parent

logger = logging.getLogger("cwidgets")
logger.debug(f"logger initialized in {__file__}")


# ============================================================================
# Common constants
# ============================================================================

#: Keys that validate components (CButton, CComboBox, CListWidget).
VALID_KEYS = (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space)

#: Keys that validate without Space (CLineEdit).
VALID_LINE_KEYS = (Qt.Key.Key_Return, Qt.Key.Key_Enter)

# CSS style configuration for disabled states.
BUTTON_DISABLED_STYLE = "QPushButton { color: gray; background-color: #e0e0e0; }"

# ###########################################################################
# CTextEdit
# ###########################################################################

class CTextEdit(QWidget):
    """
    Rich text editing component using Windows' native RichEdit engine.

    This widget encapsulates the low-level functionality of the Win32 RichEdit control
    to provide a programming interface (API) similar to QTextEdit, while ensuring
    maximum compatibility with screen readers like NVDA through the use of native
    window handles.
    """

    def __init__(self, parent=None, accessible_name="", stretch=1, x=0, y=0, width=None, height=None):
        validate_parent(parent, "CTextEdit")
        super().__init__(parent)
        self.stretch = stretch
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._appending = False
        self.core = None
        self.pending_text = None
        # List of tuples (method_name, args) for deferred style application after Win32 handle initialization.
        self.pending_styles = []
        self._destroyed = False
        self._first_focus = True
        self._focus_pending = False
        self._accessible_name = accessible_name

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        QTimer.singleShot(0, self._create)

    # --------------------------------------------------------------------
    # Internal creation
    # --------------------------------------------------------------------
    def _create(self):
        """
        Asynchronously initializes the native Win32 RichEdit control.
        Checks for window handle (HWND) availability before EditorStyle instantiation.
        """
        if self._destroyed:
            logger.debug("_create: widget destroyed, aborting")
            return
        try:
            # Retrieve the native window handle (HWND) for Win32 control injection.
            hwnd = int(self.winId())
        except RuntimeError as e:
            # If winId() is not ready yet, defer creation via the event loop.
            logger.debug(f"_create: winId() not available, retrying in 20ms: {e}")
            QTimer.singleShot(20, self._create)
            return
        if not hwnd:
            logger.debug("_create: hwnd is null, retrying in 20ms")
            QTimer.singleShot(20, self._create)
            return
        try:
            self.core = EditorStyle()
            self.core._tab_callback = self._navigate_tab
            w = self._width if self._width is not None else self.width()
            h = self._height if self._height is not None else self.height()
            # Effective creation of the RichEdit control in the Qt container.
            self.core.create(hwnd, self._x, self._y, w, h, "", self._accessible_name)

            # Restore text that was pending before handle creation.
            if self.pending_text is not None:
                self.core.set_text(self.pending_text)
                self.pending_text = None

            # Apply deferred styles configured during initialization.
            for method_name, args in self.pending_styles:
                try:
                    getattr(self.core, method_name)(*args)
                except Exception as e:
                    logger.exception(f"_create: error applying style {method_name}")
            self.pending_styles.clear()

            # Initialize selection at the start of the document via Win32 API.
            win32gui.SendMessage(self.core.edit_hwnd, win32con.EM_SETSEL, 0, 0)

            # Subclass the main window to intercept system focus changes.
            main_hwnd = int(self.window().winId())
            self.core.subclass_main(main_hwnd, self._on_app_focus)

            # Handle a focus request that occurred before creation was finalized.
            if self._focus_pending:
                self._focus_pending = False
                self.setFocus()

            logger.info("CTextEdit created successfully")
        except Exception as e:
            logger.exception("_create: error during control creation")
            self.core = None

    def _navigate_tab(self, forward: bool):
        """
        Handles tab navigation via Qt's focus manager.
        """
        self.focusNextPrevChild(forward)

    def _on_app_focus(self):
        """
        Callback to restore focus when the application returns to the foreground.
        """
        self.setFocus()

    # --------------------------------------------------------------------
    # Focus management
    # --------------------------------------------------------------------
    def setFocus(self):
        """
        Assigns keyboard focus to the underlying RichEdit control.
        Handles cases where the control is not yet instantiated (deferred focus).
        """
        if self.core and self.core.edit_hwnd:
            self.core.set_focus()
            super().setFocus()
            self._first_focus = False
            self._focus_pending = False
            return
        self._focus_pending = True
        super().setFocus()
        QTimer.singleShot(50, self._check_pending_focus)

    def _check_pending_focus(self):
        """
        Checks and applies focus that was pending handle creation.
        """
        if self._focus_pending and self.core and self.core.edit_hwnd:
            self._focus_pending = False
            self.core.set_focus()
            super().setFocus()
            self._first_focus = False

    def focusInEvent(self, event):
        """
        Captures the focus-in event to synchronize Win32 focus.
        """
        super().focusInEvent(event)
        if self.core and not self._appending:
            self.core.set_focus()

    # --------------------------------------------------------------------
    # Public API (QTextEdit-compatible)
    # --------------------------------------------------------------------
    def toPlainText(self) -> str:
        """
        Retrieves the raw text content of the control.
        Returns:
            str: Text content extracted from the Win32 engine or the pending buffer.
        """
        if self.core:
            return self.core.get_text()
        return self.pending_text if self.pending_text is not None else ""

    def text(self) -> str:
        """
        Synonym accessor for toPlainText() to ensure compatibility with the standard Qt API.
        """
        return self.toPlainText()

    def setText(self, text: str):
        """
        Sets the entire text content.
        Args:
            text (str): String to inject into the control.
        """
        if self.core and self.core.edit_hwnd:
            self.core.set_text(text)
        else:
            self.pending_text = text

    def clear(self):
        """
        Resets the control's content (full clear).
        """
        if self.core:
            self.core.clear()
        else:
            self.pending_text = ""

    def append(self, text: str):
        """
        Appends a text sequence to the end of the document with automatic scrolling.
        Args:
            text (str): Text to append.
        """
        if self.core:
            self._appending = True
            try:
                self.core.append(text)
            finally:
                self._appending = False
            self.setFocus()
        else:
            if self.pending_text:
                self.pending_text += "\n" + text
            else:
                self.pending_text = text

    def setReadOnly(self, readonly: bool):
        """
        Configures the read-only attribute of the control.
        Args:
            readonly (bool): True to enable read-only mode.
        """
        if self.core:
            self.core.set_readonly(readonly)
        else:
            self.pending_styles.append(('set_readonly', (readonly,)))

    def setFont(self, *args):
        """
        Configures typographic attributes (family, size, weight, italic).
        Supports passing a QFont object or a list of explicit attributes.
        """
        if len(args) == 1 and isinstance(args[0], QFont):
            font = args[0]
            name = font.family()
            size = font.pointSize()
            bold = font.bold()
            italic = font.italic()
            self._set_font_impl(name, size, bold, italic)
        elif len(args) == 4:
            self._set_font_impl(*args)
        else:
            raise TypeError("setFont() accepts either QFont or (str, int, bool, bool)")

    def _set_font_impl(self, name: str, size: int, bold: bool, italic: bool):
        """
        Internal implementation of font setting.
        """
        if self.core:
            self.core.set_font(name, size, bold, italic)
        else:
            self.pending_styles.append(('set_font', (name, size, bold, italic)))

    def setAlignment(self, alignment):
        """
        
        Sets the horizontal alignment of the current paragraph.
        Args:
            alignment: Union[str, Qt.Alignment] representing the desired alignment.
        """
        if isinstance(alignment, Qt.AlignmentFlag):
            if alignment == Qt.AlignLeft:
                a = "left"
            elif alignment == Qt.AlignCenter:
                a = "center"
            elif alignment == Qt.AlignRight:
                a = "right"
            else:
                a = "auto"
        else:
            a = alignment
        if self.core:
            self.core.set_alignment(a)
        else:
            self.pending_styles.append(('set_alignment', (a,)))


    def set100Alignment(self, alignment):
        """
        Sets the horizontal alignment of the current paragraph.
        Args:
            alignment: Union[str, Qt.AlignmentFlag] representing the desired alignment.
        """
        if isinstance(alignment, Qt.AlignmentFlag):
            if alignment == Qt.AlignmentFlag.AlignLeft:
                a = "left"
            elif alignment == Qt.AlignmentFlag.AlignCenter:
                a = "center"
            elif alignment == Qt.AlignmentFlag.AlignRight:
                a = "right"
            else:
                a = "auto"
        else:
            a = alignment
        if self.core:
            self.core.set_alignment(a)
        else:
            self.pending_styles.append(('set_alignment', (a,)))



    def setTextColor(self, *args):
        """
        Sets the foreground (text) color of the selected text.
        """
        if self.core:
            self.core.set_text_color(*args)
        else:
            self.pending_styles.append(('set_text_color', args))

    def setBackgroundColor(self, *args):
        """
        Sets the background color of the control.
        """
        if self.core:
            self.core.set_background_color(*args)
        else:
            self.pending_styles.append(('set_background_color', args))

    # --------------------------------------------------------------------
    # Qt events
    # --------------------------------------------------------------------
    def resizeEvent(self, event):
        if self.core:
            self.core.resize(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def closeEvent(self, event):
        if self.core:
            self.core.cleanup()
        self._destroyed = True
        super().closeEvent(event)

    def hideEvent(self, event):
        if self.core:
            self.core.cleanup()
        self._destroyed = True
        super().hideEvent(event)

# ###########################################################################
# CLabel
# ###########################################################################

class CLabel(QLabel):
    """
    Text label optimized for accessibility with NVDA.

    Behavior varies based on the association with a companion ('buddy') widget:
    - Standalone mode: The widget receives keyboard focus (StrongFocus) and sets its
      own accessible name. NVDA announces the label directly.
    - Buddy mode: The widget is ignored by focus (NoFocus). Its text is
      cleaned and passed as the accessible name to the 'buddy' widget. NVDA announces
      the label when focus reaches the linked component.

    Example instantiations:
    - CLabel("Status", self, prefix="Information")
    - CLabel("Name:", self, self.edit_name)
    - CLabel(text="First name:", parent=self, buddy=self.edit_first_name)
    """

    def __init__(
        self,
        text: str = "",
        parent: QWidget = None,
        *args,
        prefix: str = "",
        buddy: QWidget = None,
    ):
        # Extract the buddy widget from positional arguments (backward compatibility).
        if args:
            buddy = args[0] if len(args) >= 1 else buddy

        validate_parent(parent, "CLabel")
        try:
            super().__init__(text, parent)
        except Exception:
            logger.exception("CLabel: QLabel initialization failed")
            raise

        self._prefix = prefix
        self._buddy_widget = None

        if buddy is not None:
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.setBuddy(buddy)
        else:
            # Enable focus to allow NVDA detection when no buddy is set.
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self._update_accessible_name(text)

    # ------------------------------------------------------------------ #
    # Private                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _clean_shortcut(text: str) -> str:
        """
        Removes keyboard shortcut markers (&) for NVDA announcement.

        Using a sentinel (\x00) preserves double ampersands (&&) which
        should be rendered as a literal '&' character.
        """
        sentinel = "\x00"
        result = text.replace("&&", sentinel)
        result = result.replace("&", "")
        result = result.replace(sentinel, "&")
        return result.strip()

    def _update_accessible_name(self, text: str) -> None:
        """Applies accessibleName to self (buddy-less mode)."""
        try:
            name = f"{self._prefix} {text}".strip() if self._prefix else text.strip()
            self.setAccessibleName(name)
        except Exception:
            logger.exception("CLabel._update_accessible_name: failed")

    def _sync_buddy(self) -> None:
        """
        Propagates the cleaned text as the buddy's accessibleName.
        _clean_shortcut removes the & mnemonic before NVDA announcement.
        """
        try:
            target = self._buddy_widget if self._buddy_widget else self.buddy()
            if target is not None:
                target.setAccessibleName(self._clean_shortcut(self.text()))
        except Exception:
            logger.exception("CLabel._sync_buddy: failed")

    # ------------------------------------------------------------------ #
    # Public                                                             #
    # ------------------------------------------------------------------ #

    def setBuddy(self, widget: QWidget) -> None:
        """
        Associates a buddy widget and synchronizes its accessibleName.
        Disables focus on self (the buddy handles navigation).
        """
        try:
            self._buddy_widget = widget
            super().setBuddy(widget)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self._sync_buddy()
        except Exception:
            logger.exception("CLabel.setBuddy: failed")

    def setText(self, text: str) -> None:
        """Updates the text and resynchronizes NVDA accessibility."""
        try:
            super().setText(text)
            if self._buddy_widget or self.buddy():
                self._sync_buddy()
            else:
                self._update_accessible_name(text)
        except Exception:
            logger.exception("CLabel.setText: failed")

    def setPrefix(self, prefix: str) -> None:
        """Modifies the prefix and recalculates the accessibleName (buddy-less mode)."""
        try:
            self._prefix = prefix
            self._update_accessible_name(self.text())
        except Exception:
            logger.exception("CLabel.setPrefix: failed")

# ###########################################################################
# CButton
# ###########################################################################

class CButton(QPushButton):
    """
    Push button (QPushButton) optimized for accessibility.

    Improvements:
    - Activation: Natively supports activation via Space, Enter, and Return keys,
      in addition to mouse clicks.
    - Logical state: Manages an internal activation state to remain visible to NVDA
      even when logically disabled, while blocking interactions and updating its
      accessible description.
    """

    def __init__(self, label: str = "", parent: QWidget = None):
        validate_parent(parent, "CButton")
        super().__init__(label, parent)
        self._enabled_state = True

    # ------------------------------------------------------------------ #
    # Private                                                            #
    # ------------------------------------------------------------------ #

    def _trigger(self) -> None:
        """Triggers the click only if the button is logically active."""
        if self._enabled_state:
            self.click()

    # ------------------------------------------------------------------ #
    # Events                                                             #
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Block all keyPress events if disabled
        if not self._enabled_state:
            event.accept()
            return
        # Enter and Return trigger the button like native Space
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._trigger()
        else:
            super().keyPressEvent(event)

    #def mousePressEvent(self, event):
        # Block mouse click if disabled
        #if self._enabled_state:
            #super().mousePressEvent(event)

    # ------------------------------------------------------------------ #
    # Public                                                             #
    # ------------------------------------------------------------------ #

    def setEnabled(self, enabled: bool) -> None:
        """
        Logically enables or disables the button while preserving accessibility.
        """
        self._enabled_state = enabled

        # Keep the widget enabled in Qt terms so it remains in the system
        # accessibility tree. If we called super().setEnabled(False), the widget
        # would become invisible to NVDA.
        super().setEnabled(True)

        if enabled:
            # Restore visual style and remove the unavailable description.
            self.setStyleSheet("")
            self.setAccessibleDescription("")
        else:
            # Apply a grayed-out visual style and update the description for NVDA.
            self.setStyleSheet(BUTTON_DISABLED_STYLE)
            self.setAccessibleDescription("unavailable")

    def isEnabled(self) -> bool:
        """Returns the logical state of the button."""
        return self._enabled_state

    def setDisabled(self, disabled: bool) -> None:
        """Overrides setDisabled for consistency with setEnabled."""
        self.setEnabled(not disabled)

# ###########################################################################
# CLineEdit
# ###########################################################################

class CLineEdit(QLineEdit):
    """
    Single-line text input field (LineEdit) optimized for NVDA.

    Improvements:
    - Validation: Emits the 'validated' signal with the field's content when
      Enter or Return keys are pressed.
    - Accessibility: Supports external labels via CLabel and properly announces
      the placeholder text when the field is empty.

    Usage:
    - Instantiation: `edit = CLineEdit(self, placeholderText="Enter your text")`
    - Signal: `edit.validated.connect(my_handler)`
    """

    validated = Signal(str)

    def __init__(self, parent: QWidget = None, text: str = "", placeholderText: str = ""):
        validate_parent(parent, "CLineEdit")
        super().__init__(text, parent)

        if placeholderText:
            self.setPlaceholderText(placeholderText)

    # ------------------------------------------------------------------ #
    # Events                                                             #
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in VALID_LINE_KEYS:
            # Emit the entered text for validation
            self.validated.emit(self.text())
            event.accept()
        else:
            super().keyPressEvent(event)

# ###########################################################################
# CComboBox
# ###########################################################################

class CComboBox(QComboBox):
    """
    Custom dropdown list (ComboBox) for optimal accessibility.

    Features:
    - Navigation: Uses arrow keys without immediate triggering.
    - Validation: Enter and Space keys validate the selection and emit the 'validated' signal.
    - Disabled state: The component remains visible to screen readers but announces
      "unavailable" and blocks interactions.

    Signal:
    - validated(str): Emitted when an item is validated, transmits the selected text.
    """

    validated = Signal(str)
    cleared = Signal()

    def __init__(self, parent: QWidget = None):
        validate_parent(parent, "CComboBox")
        super().__init__(parent)
        self._enabled_state = True

    # ------------------------------------------------------------------ #
    # Private                                                            #
    # ------------------------------------------------------------------ #

    def _emit_validation(self, row: int) -> None:
        if row < 0 or self.count() == 0:
            self.cleared.emit()
            return
        self.hidePopup()
        self.validated.emit(self.itemText(row))

    # ------------------------------------------------------------------ #
    # Events                                                             #
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self._enabled_state:
            event.accept()
            return
        if event.key() in VALID_KEYS:
            self._emit_validation(self.currentIndex())
            event.accept()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        # Block mouse click if disabled
        if self._enabled_state:
            super().mousePressEvent(event)

# ------------------------------------------------------------------ #
    # Public                                                             #
    # ------------------------------------------------------------------ #

    def setEnabled(self, enabled: bool) -> None:
        self._enabled_state = enabled
        # Keep Qt enabled so NVDA can detect the widget
        super().setEnabled(True)

        if enabled:
            self.setAccessibleDescription("")
        else:
            # NVDA announces "unavailable" when the combo is disabled
            self.setAccessibleDescription("unavailable")

    def isEnabled(self) -> bool:
        return self._enabled_state

    def setDisabled(self, disabled: bool) -> None:
        self.setEnabled(not disabled)

# ###########################################################################
# CListWidget
# ###########################################################################

class CListWidget(QListWidget):
    """
    List widget (ListWidget) adapted for accessible interaction.

    Features:
    - Navigation: Smooth movement between items using keyboard arrows.
    - Validation: Enter, Return, and Space keys activate the current item
      by emitting the native 'itemActivated' signal.
    - State management: In disabled mode, the widget informs the user of
      its unavailability while remaining visible for tactile or voice exploration.
    """

    def __init__(self, parent: QWidget = None):
        validate_parent(parent, "CListWidget")
        super().__init__(parent)
        self._enabled_state = True

    # ------------------------------------------------------------------ #
    # Events                                                             #
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self._enabled_state:
            event.accept()
            return
        if event.key() in VALID_KEYS:
            item = self.currentItem()
            if item is not None:
                # Emit the native Qt signal — developer connects as usual
                self.itemActivated.emit(item)
            event.accept()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        # Block mouse click if disabled
        if self._enabled_state:
            super().mousePressEvent(event)


    # ------------------------------------------------------------------ #
    # Public                                                             #
    # ------------------------------------------------------------------ #

    def setEnabled(self, enabled: bool) -> None:
        self._enabled_state = enabled
        # Keep Qt enabled so NVDA can detect the widget
        super().setEnabled(True)

        if enabled:
            self.setAccessibleDescription("")
        else:
            # NVDA announces "unavailable" when the list is disabled
            self.setAccessibleDescription("unavailable")

    def isEnabled(self) -> bool:
        return self._enabled_state

    def setDisabled(self, disabled: bool) -> None:
        self.setEnabled(not disabled)

# ###########################################################################
# CMessageBox
# ###########################################################################

class CMessageBox:
    """
    Modal or timed dialog box manager.

    This class provides static methods for displaying informational,
    warning, or critical error messages, with support for automatic
    closing (timeout) and audio signals for accessibility.
    """

    @staticmethod
    def _create(parent, title, text, icon, timeout, beep):
        validate_parent(parent, "CMessageBox")
        box = QMessageBox(parent)
        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(icon)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if beep:
            QApplication.beep()

        if timeout is None:
            box.setWindowModality(Qt.WindowModality.ApplicationModal)
            return box.exec()

        # Timed mode — auto-close after timeout ms
        box.setWindowModality(Qt.WindowModality.NonModal)
        box.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        )
        QTimer.singleShot(timeout, box.accept)
        box.show()
        return None

    @staticmethod
    def information(parent: QWidget, title: str, text: str, timeout: int = None):
        """Displays an informational dialog — optionally timed."""
        return CMessageBox._create(
            parent, title, text, QMessageBox.Icon.Information, timeout, beep=False
        )

    @staticmethod
    def warning(parent: QWidget, title: str, text: str, timeout: int = None):
        """Displays a warning dialog — optionally timed."""
        return CMessageBox._create(
            parent, title, text, QMessageBox.Icon.Warning, timeout, beep=False
        )

    @staticmethod
    def critical(parent: QWidget, title: str, text: str):
        """Displays a critical error dialog — modal + beep — manual close."""
        return CMessageBox._create(
            parent, title, text, QMessageBox.Icon.Critical, timeout=None, beep=True
        )
