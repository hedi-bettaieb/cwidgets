#User Guide - CWidgets Library V0.1.1:

## Introduction
CWidgets: Your Unlimited Programming Power
Turning Qt obstacles into creative opportunities
CWidgets is a specialized Python library that gives blind developers full control over PyQt6 and PySide6 interfaces.
The era of limitations with QTextEdit is over - from now on, you can design interfaces containing multi-line edit boxes with complete freedom and compatibility.
The library provides absolute compatibility for blind developers as all elements are designed to work seamlessly with the NVDA screen reader.
Continuity of creativity: No need to learn new tools - continue writing your familiar code while maintaining the same functions and features.
Smart engineering: Every element in CWidgets inherits properties from original Qt elements, ensuring standard performance with radical solutions for compatibility issues.
What will change when writing your PyQt6 and PySide6 window-based application code?
All you need is to replace just the first letter (C instead of Q):
CTextEdit instead of QTextEdit.
CButton instead of QPushButton.
Where C stands for Custom
Complete flexibility in work, as the library supports your preferred working environment with the same efficiency:
With PySide6:
from cwidgets.pyside6 import CButton, CLabel, CLineEdit


With PyQt6:

from cwidgets.pyqt6 import CButton, CLabel, CLineEdit

CWidgets: Code with confidence, design without limits.

## Available Components:
7 fully compatible custom elements provided by this library are:
1-CTextEdit
2-CButton
3-CLabel
4-CLineEdit
5-CComboBox
6-CListWidget
7-CMessageBox

## Installation
pip install cwidgets


## Accessing Help

After installation, start exploring the library, its components, properties, and usage through these functions:

import cwidgets

# List of all available components
cwidgets.widgets()

# List of all available sections
cwidgets.sections()

# Open the full guide in browser
cwidgets.show_help()
cwidgets.show_help(lang="ar")

# Open a specific component directly
cwidgets.show_help(lang="ar", goto="CButton")
cwidgets.show_help(lang="ar", goto="CTextEdit")

# Open a specific section directly
cwidgets.show_help(lang="ar", goto="introduction")
cwidgets.show_help(lang="ar", goto="installation")


## Common Problems Solved

#CTextEdit:
Multi-line edit box: CTextEdit solves the fundamental problem of QTextEdit, which is incompatible with NVDA.
#CComboBox & CListWidget:
Navigation-activation separation: Separating navigation actions (arrows) from activation actions (Enter/Space) to avoid unintended activations.
Available disabling: Maintaining NVDA announcement even when the component is disabled.
#CButton:
Activation with enter, return, space & mouse.
Compatibility even when disabled.
#CLabel
Enhanced compatibility for titles and labels
#CLineEdit:
Allows retrieving text from within the element by pressing enter without any additional code.
#CMessageBox:
Self-closing message dialogs.
You can specify a time after which the dialog disappears automatically.
#Except for CTextEdit, all other components inherit from QT and thus retain all their basic properties and functions.

## Component Details:
Definition, Creation, Properties, Usage.

## CTextEdit

### Definition
CTextEdit is a multi-line edit box fully compatible with NVDA.

### Why — The Fundamental Problem
- Original QTextEdit in Qt is incompatible with NVDA.
- Blind developers cannot read or write in this element.
This is the barrier preventing blind people from designing QT interfaces containing multi-line edit boxes.
Until this library appeared, no solutions were known to be used by blind people for this problem.

### Solution — Win32 RichEdit Embedded in Qt
The solution provided by this library is to embed a Win32 RichEdit control directly into the QT window.
Win32 RichEdit is natively fully compatible with NVDA.
The complex part of designing the solution was integrating it into the Qt window while maintaining this accessibility.
The library also ensured the default use of QT commands.
QTextEdit element structure:
-QTextEdit
-EditorStyle — Styles, font, color, alignment
-RichEdit Win32 — The original compatible engine

### Features
- Full NVDA accessibility: Reading, writing, navigation, selection.
- API compatible with QTextEdit: setText, toPlainText, append, clear, setReadOnly.
- Formatted text: Font, size, bold, italic, color, alignment.
- Asynchronous management: Styles and text are queued if the Win32 handle isn't available yet.
- Smart focus: Restores focus when returning to the application.

### Usage


# PySide6
from cwidgets.pyside6 import CTextEdit
# PyQt6
from cwidgets.pyqt6 import CTextEdit

# Creation
self.editor = CTextEdit(self, accessible_name="Box name")
layout.addWidget(self.editor)

# Insert text into the box
self.editor.setText("Hello!")
# Retrieve text from the box:
text = self.editor.text()
text = self.editor.toPlainText()
# Add text to original text
self.editor.append("New line.")
# Clear text to empty the box
self.editor.clear()

# Make the box read-only
self.editor.setReadOnly(True)
# Disable read-only to make the box writable
self.editor.setReadOnly(False)

# Font — QFont or (str, int, bool, bool)
self.editor.setFont("Arial", 12, True, False)  # Name, size, bold, italic

# Colors — name or RGB set
self.editor.setTextColor("red")
self.editor.setTextColor((255, 0, 0))
self.editor.setBackgroundColor("yellow")

# Alignment
self.editor.setAlignment("left")
self.editor.setAlignment("center")
self.editor.setAlignment("right")


### Available Colors


# Supported names
"black", "white", "red", "green", "blue", "yellow",
"cyan", "magenta", "gray", "darkgray", "lightgray",
"orange", "purple", "violet", "pink", "brown",
"navy", "teal", "lime", "olive", "maroon",
"coral", "salmon", "gold", "silver"

# Or RGB set
(255, 0, 0)    # red
(0, 128, 255)  # light blue


### Optional Visual Title
accessible_name is read by NVDA but not visually visible.
To add a visual title, add a CLabel to the layout before the editor:

self.editor = CTextEdit(self)
self.lbl    = CLabel("Edit box:", self, self.editor)

It's important to note that adding CLabel to the layout must precede adding the editor so the box name appears above the box, not below it.

layout.addWidget(self.lbl)
layout.addWidget(self.editor)


## CLabel

### Definition
CLabel is an NVDA-compatible label that replaces QLabel.

### Why?
Original QLabel is invisible to NVDA unless linked to a buddy - and only when that buddy has focus.

### Solution
Two modes:
- Single mode: NVDA-compatible and recognized even with tab navigation.
- Buddy mode: When CLabel is linked to another element.

### Features
- Shortcut cleanup: &Name → "Name" for NVDA, visual shortcut for Qt preserved.
- prefix: Additional text example when expressing status.

- Default synchronization:
Changing label content.
setText()
Changing additional text:
setPrefix()
They resynchronize without additional code.

### Usage


# PySide6
from cwidgets.pyside6 import CLabel, CLineEdit
# PyQt6
from cwidgets.pyqt6 import CLabel, CLineEdit

# Single mode — NVDA reads the text and is accessible via tab:
self.lbl = CLabel("File saved", self)

# With prefix — NVDA announces: "status file saved"
self.lbl = CLabel("File saved", self, prefix="status")

# Buddy mode — NVDA announces the label when the field gets focus
# The label must be added to the layout before the edit field to appear visually above it
self.edit = CLineEdit(self)
self.lbl  = CLabel("Name:", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# Dynamic update
self.lbl.setText("Processing")
self.lbl.setPrefix("error")


## CButton

### Definition
CButton is a button with additional features that make it usable without needing the original button's code lines to enable these features.

### Why?
- Original QPushButton only accepts Space for activation — Enter and Return are ignored.
- setEnabled(False) makes the button invisible to NVDA, even with setAccessibleDescription.

### Solution
- Activation includes Enter/Return.
- Disabling the button maintains compatibility.
The button remains visually "active" but doesn't work.
This is the solution: providing the ability to disable while maintaining compatibility, unlike QPushButton which disappears from NVDA when disabled.

### Features
- Extended activation: Space, Enter, Return, mouse click.
- Available disabling: Not clickable + NVDA announces "unavailable".
- API matching QPushButton.

### Usage


# PySide6
from cwidgets.pyside6 import CButton
# PyQt6
from cwidgets.pyqt6 import CButton

self.btn = CButton("Save", self)
self.btn.clicked.connect(self.on_click)

# Disable — NVDA announces "unavailable", button not clickable
self.btn.setEnabled(False)
self.btn.setEnabled(True)

# Change title — original Qt
self.btn.setText("New title")

# Check state
if self.btn.isEnabled():
    ...


## CLineEdit

### Definition
CLineEdit is a compatible text input field that replaces QLineEdit.

### Why?
QLineEdit requires an additional line of code to retrieve text.
CLineEdit makes this activation automatic via the validated signal.

### Features
- The validated signal emits with the current text on every Enter/Return.
- placeholderText as parameter — announced by NVDA when the field is empty.
- Title via CLabel with buddy.

### Usage


# PySide6
from cwidgets.pyside6 import CLineEdit, CLabel
# PyQt6
from cwidgets.pyqt6 import CLineEdit, CLabel

# Create the field first for buddy
self.edit = CLineEdit(self)
self.lbl  = CLabel("Name:", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# With initial text
self.edit = CLineEdit(self, "Cairo")

# With placeholder text
self.edit = CLineEdit(self, placeholderText="Enter your name...")

# validated signal
self.edit.validated.connect(self.on_validated)

def on_validated(self, text: str) -> None:
    text = self.edit.text()  # Original Qt retrieval
    print(text)

# Show/hide — original Qt
self.edit.hide()
self.edit.show()


## CComboBox

### Definition
CComboBox is a compatible dropdown list that replaces QComboBox.

### Why?
- Original QComboBox activation occurs internally with arrows.
This is problematic for blind users who navigate with arrows.

### Solution
Explicit separation between navigation and activation.
Maintaining compatibility even when the list is disabled.

### Features
- Free navigation: ↑ ↓ for navigation without activation.
- Explicit activation: Enter, Return, Space → via validated signal.
- cleared signal: Emitted when the user checks an empty list.
- Available disabling: NVDA announces "unavailable".
- Title via CLabel with buddy — using setAccessibleName is not recommended as it replaces the label.

### Usage


# PySide6
from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox, CButton
# PyQt6
from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox, CButton

# Create the list first for buddy
self.combo = CComboBox(self)
self.combo.addItems(["Egypt", "Tunisia", "Morocco"])
self.lbl = CLabel("Country list:", self, self.combo)
layout.addWidget(self.lbl)
layout.addWidget(self.combo)

self.combo.validated.connect(self.on_selection)
self.combo.cleared.connect(self.on_cleared)

# Button to empty the list
self.btn_clear = CButton("Clear", self)
self.btn_clear.clicked.connect(self.combo.clear)

def on_selection(self) -> None:
    text  = self.combo.currentText()
    index = self.combo.currentIndex()
    CMessageBox.information(self, "Selection", f"Country: {text}")

def on_cleared(self) -> None:
    CMessageBox.warning(self, "Warning", "No items available in the list.")

# Disable/re-enable
self.combo.setEnabled(False)
self.combo.setEnabled(True)


## CListWidget

### Definition
CListWidget is a compatible list that replaces QListWidget.

### Why?
Original QListWidget activation occurs immediately when navigating with arrows.
This is an obstacle for blind users, and disabling this activation with arrows requires additional code lines.

### Solution
- Separation between navigation and activation.
- Maintaining accessibility in disabled mode.

### Features
- Free navigation: ↑ ↓ for navigation without activation.
- Explicit activation: Enter, Return, Space.
- When disabled: NVDA announces "unavailable".
- Title via CLabel with buddy — using setAccessibleName is not recommended as it replaces the label.

### Usage


# PySide6
from cwidgets.pyside6 import CListWidget, CLabel
# PyQt6
from cwidgets.pyqt6 import CListWidget, CLabel

# Create the list
self.list = CListWidget(self)
self.list.addItems(["Iraq", "Saudi Arabia", "Kuwait"])
self.lbl = CLabel("Country list:", self, self.list)
layout.addWidget(self.lbl)
layout.addWidget(self.list)

# Original Qt signal — matches QListWidget
self.liste.itemActivated.connect(self.on_item)

def on_item(self, item) -> None:
    text = item.text()
    row  = self.liste.currentRow()
    print(row, text)

# Disable/re-enable
self.liste.setEnabled(False)
self.liste.setEnabled(True)

# Clear — original Qt
self.liste.clear()


## CMessageBox

### Definition
CMessageBox is a compatible message dialog.

### Why?
Original QMessageBox doesn't provide automatic closing.
We need it for messages that don't require user intervention.

### Solution
Adding a mode where the message closes after a specified time.

### Features
- information: Timed or untimed — no sound.
- warning: Timed or untimed — no sound.
- critical: Always untimed + system sound — manual closing required.
- Manual closing always possible before timeout ends.

### Usage


# PySide6
from cwidgets.pyside6 import CMessageBox
# PyQt6
from cwidgets.pyqt6 import CMessageBox

# Untimed information
CMessageBox.information(self, "Success", "File saved.")

# Timed information — auto-close after 3 seconds
CMessageBox.information(self, "Success", "File saved.", timeout=3000)

# Untimed warning
CMessageBox.warning(self, "Warning", "Insufficient disk space.")

# Timed warning
CMessageBox.warning(self, "Warning", "Unstable connection.", timeout=4000)

# Error — untimed + sound — manual closing required
CMessageBox.critical(self, "Error", "File not found.")

# Timeout is recommended only for information and warning
# Timeout not available for critical


## Best Practices

1 — Titles: Always use CLabel with buddy.


# Not recommended — replaces label
self.combo.setAccessibleName("...")

# Correct
self.lbl = CLabel("Country list:", self, self.combo)


2 — Disabling: setEnabled(False) is available by default on all C* components.

3 — Activation:
- CLineEdit and CComboBox → validated signal
- CListWidget → original Qt itemActivated signal

4 — Creation order with buddy: Always create the element before its CLabel.


# Correct — element created before label
self.combo = CComboBox(self)
self.lbl   = CLabel("Country:", self, self.combo)


## System Requirements

- PySide6 or PyQt6
- pywin32 — only for CTextEdit (Win32 RichEdit integration)

Provided by the library:
- validate_parent — Regular parent window check
- logger — Error logging (module "cwidgets")

## Library Limitations

- CTextEdit depends on Win32 RichEdit — Windows only compatibility.
- Using setAccessibleName with CComboBox and CListWidget is not recommended as it replaces the buddy CLabel.
- CButton: Gray shading via stylesheet — Windows doesn't automatically shade the button when keeping it active for NVDA.

## Developer:
Mohamed Hédi Bettaieb (Tunisia)
For communication and interaction:
Email: hedidouz@gmail.com
Library design date: May 2026.

## Conclusion

This project aims to make Qt applications 100% accessible to blind developers and users, without sacrificing productivity or Qt developers' habits.