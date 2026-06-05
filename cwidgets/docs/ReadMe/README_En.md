# User Guide - CWidgets Library V0.1.3

## Introduction

CWidgets is a specialized Python library that gives blind developers
full control over PyQt6 and PySide6 interfaces.

The era of limitations with QTextEdit is over — you can now design
interfaces containing multi-line edit areas with complete freedom and
full compatibility with NVDA.

All you need to do is replace the first letter (C instead of Q):
- CTextEdit instead of QTextEdit
- CButton instead of QPushButton
- Where C stands for Custom

The library supports both Qt environments:

# PySide6
from cwidgets.pyside6 import CButton, CLabel, CLineEdit

# PyQt6
from cwidgets.pyqt6 import CButton, CLabel, CLineEdit

CWidgets: Code with confidence, design without limits.

## Available Components

7 fully NVDA-compatible custom components:

1. CTextEdit
2. CButton
3. CLabel
4. CLineEdit
5. CComboBox
6. CListWidget
7. CMessageBox

## Installation

pip install cwidgets

## Accessing Help

import cwidgets

# List of all available components
cwidgets.widgets()

# List of all available sections
cwidgets.sections()

# Open the complete guide in the browser
cwidgets.show_help()
cwidgets.show_help(lang="fr")
cwidgets.show_help(lang="ar")

# Open a specific component directly
cwidgets.show_help(lang="fr", goto="CButton")
cwidgets.show_help(lang="fr", goto="CTextEdit")

# Open a specific section directly
cwidgets.show_help(lang="fr", goto="introduction")
cwidgets.show_help(lang="fr", goto="installation")

# CTextEdit API — display from terminal
cwidgets.ctextedit.show()          # names only
cwidgets.ctextedit.show_details()  # names + descriptions

## Common Issues Solved

**CTextEdit** — Multi-line edit area: resolves QTextEdit's incompatibility with NVDA.

**CComboBox & CListWidget** — Separation of navigation/activation: prevents
unintentional activations during arrow key navigation. NVDA accessibility maintained
even in disabled mode.

**CButton** — Activation via Enter, Return, Space and click. NVDA compatibility
even when disabled.

**CLabel** — Enhanced compatibility for titles and labels.

**CLineEdit** — Text retrieval via Enter without additional code.

**CMessageBox** — Auto-closing dialog boxes with configurable delay.

With the exception of CTextEdit, all components inherit from Qt and retain
all their original properties and functions.

## Component Details

## CTextEdit

### Definition
CTextEdit is a fully NVDA-accessible multi-line edit area,
based on the native Win32 RichEdit engine.

### Why — The Fundamental Problem
- Qt's native QTextEdit is incompatible with NVDA.
- Blind developers cannot read or write in this element.
- Until this library appeared, no known solution existed.

### Solution — Win32 RichEdit Integrated into Qt
The solution directly integrates a Win32 RichEdit control into the Qt window.
Win32 RichEdit is natively compatible with NVDA.

Internal structure:
- CTextEdit — Public Qt interface
- EditorStyle — Styles, font, color, alignment
- Win32 RichEdit — NVDA-compatible native engine

### Features
- Full NVDA accessibility: reading, writing, navigation, selection.
- Extended API: 25 public methods available.
- Formatted text: font, size, bold, italic, color, alignment.
- Signals: textChanged, selectionChanged, cursorPositionChanged.
- Asynchronous management: styles and text queued before initialization.
- Smart focus: automatically restored after Alt+Tab.

### Import

# PySide6
from cwidgets.pyside6 import CTextEdit
# PyQt6
from cwidgets.pyqt6 import CTextEdit

### Creation

self.editor = CTextEdit(self, accessible_name="Edit area name")
layout.addWidget(self.editor)

### Available API

# Display all methods from terminal
import cwidgets
cwidgets.ctextedit.show()          # names only
cwidgets.ctextedit.show_details()  # names + descriptions

# From code
CTextEdit.api()

### Content

# Set content
self.editor.setText("Hello!")

# Get content
text = self.editor.toPlainText()
text = self.editor.text()          # alias for toPlainText()

# Add text at the end
self.editor.append("New line.")

# Insert at cursor position
self.editor.insertPlainText("Inserted text\n")

# Insert HTML at cursor position
# Tags are removed, <br> and <p> become line breaks
self.editor.insertHtml("<p>Hello <b>world</b></p>")  # inserts: "Hello world"
self.editor.insertHtml("<p>Line 1</p><br/>Line 2")   # inserts: "Line 1\nLine 2"

# Clear content
self.editor.clear()

### Selection

# Select all
self.editor.selectAll()

# Get selected text (returns "" if no selection)
text = self.editor.selectedText()

# Combined example — get all text
self.editor.selectAll()
text = self.editor.selectedText()

### Properties

# Line count
count = self.editor.lineCount()

# Read-only
self.editor.setReadOnly(True)    # enable
self.editor.setReadOnly(False)   # disable
state = self.editor.isReadOnly() # check

### Formatting

# Font — QFont or (name, size, bold, italic)
self.editor.setFont("Arial", 12, True, False)

# Text color — name or (R, G, B)
self.editor.setTextColor("red")
self.editor.setTextColor((255, 0, 0))

# Background color
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

# Or RGB
(255, 0, 0)    # red
(0, 128, 255)  # light blue

### Clipboard

# Shortcuts Ctrl+C/X/V/Z/Y work natively via keyboard.
# These methods allow programmatic use (e.g., via a button).

self.editor.copy()   # copy selection
self.editor.cut()    # cut selection
self.editor.paste()  # paste
self.editor.undo()   # undo
self.editor.redo()   # redo

### Signals

# React to real-time changes
self.editor.textChanged.connect(self.on_text_changed)
self.editor.cursorPositionChanged.connect(self.on_cursor_changed)
self.editor.selectionChanged.connect(self.on_selection_changed)

def on_text_changed(self):
    print(self.editor.toPlainText())

def on_cursor_changed(self):
    print("Cursor moved")

def on_selection_changed(self):
    print(self.editor.selectedText())

### Behavior in Layouts

CTextEdit has a minimum size of 50x50 pixels to ensure visibility.

**Case 1 — QVBoxLayout (editor alone on its line)**
layout.addWidget(self.editor)

**Case 2 — QHBoxLayout shared with QListWidget or QComboBox**
Without `stretch=1`, other widgets take all space.
layout = QHBoxLayout()
layout.addWidget(self.list_widget, 1)
layout.addWidget(self.editor, 1)

**Case 3 — Fixed dimensions**
self.editor = CTextEdit(self, width=400, height=200)

**Case 4 — Hide / Show**
self.editor.hide()  # hides without destroying content
self.editor.show()  # redisplays with content intact

### Optional Visual Title

accessible_name is read by NVDA but not visually visible.
To add a visual title, use CLabel before the editor in the layout:

self.editor = CTextEdit(self)
self.lbl    = CLabel("Edit area:", self, self.editor)
layout.addWidget(self.lbl)
layout.addWidget(self.editor)



### CLabel

#### Definition
CLabel is an NVDA-compatible label that replaces `QLabel`.

#### Why?

QLabel is invisible to NVDA unless linked to a buddy, and only when that buddy has focus.

#### Solution

**Simple mode (individual)** :  
NVDA-compatible, recognized directly via tab navigation (Strong focus).

**Buddy mode** :  
Linked to another component, invisible to tab navigation (no focus) to avoid cluttering the reading.  
Its cleaned text is automatically read when the linked component takes focus.

#### Features

- **Shortcut cleanup** : `&Name` becomes `"Name"` for NVDA. The visual shortcut remains preserved for the system.
- **prefix** : Additional text to express a status (e.g., "error", "status").
- **Automatic synchronization** via `setText()` and `setPrefix()`.

#### Usage

# PySide6
from cwidgets.pyside6 import CLabel, CLineEdit
# PyQt6
from cwidgets.pyqt6 import CLabel, CLineEdit

# Simple mode (individual)
self.lbl = CLabel("File saved", self, prefix="status")
# NVDA announces: "status file saved"
layout.addWidget(self.lbl)

# Buddy mode — add the label ABOVE the buddy in the layout
self.edit = CLineEdit(self)
self.lbl  = CLabel("&Name:", self, self.edit)
layout.addWidget(self.lbl)   # label first → appears above
layout.addWidget(self.edit)

# Dynamic update
self.lbl.setText("Processing")
self.lbl.setPrefix("error")


## CButton

### Definition
CButton is an accessible button that replaces QPushButton.

### Why?
- QPushButton only accepts the space bar — Enter and Return are ignored.
- setEnabled(False) makes the button invisible to NVDA.

### Solution
- Activation via Enter, Return, Space and mouse click.
- Disabled mode: not clickable but visible to NVDA ("unavailable").

### Features
- Extended activation: Space, Enter, Return, mouse click.
- Accessible deactivation: NVDA announces "unavailable".
- API identical to QPushButton.

### Usage

# PySide6
from cwidgets.pyside6 import CButton
# PyQt6
from cwidgets.pyqt6 import CButton

self.btn = CButton("Save", self)
self.btn.clicked.connect(self.on_click)

# Disable / re-enable
self.btn.setEnabled(False)
self.btn.setEnabled(True)

# Check state
if self.btn.isEnabled():
    ...

## CLineEdit

### Definition
CLineEdit is a compatible input field that replaces QLineEdit.

### Why?
QLineEdit requires additional code to retrieve text on validation.
CLineEdit automates this via the `validated` signal.

### Features
- `validated` signal: emits text on each Enter/Return.
- `placeholderText` as parameter, announced by NVDA when the field is empty.
- Title via CLabel with buddy.

### Usage

# PySide6
from cwidgets.pyside6 import CLineEdit, CLabel
# PyQt6
from cwidgets.pyqt6 import CLineEdit, CLabel

self.edit = CLineEdit(self)
self.lbl  = CLabel("Name:", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# With initial text
self.edit = CLineEdit(self, "Cairo")

# With placeholder
self.edit = CLineEdit(self, placeholderText="Enter your name...")

# validated signal
self.edit.validated.connect(self.on_validated)

def on_validated(self, text: str) -> None:
    print(text)

## CComboBox

### Definition
CComboBox is an accessible dropdown list that replaces QComboBox.

### Why?
QComboBox activates the item during arrow key navigation —
problematic for blind users.

### Solution
Explicit separation between navigation (arrows) and activation (Enter/Space).
NVDA accessibility maintained in disabled mode.

### Features
- Free navigation: ↑↓ without activation.
- Explicit activation: Enter, Return, Space → `validated` signal.
- `cleared` signal: emitted if user interacts with an empty list.
- Accessible deactivation: NVDA announces "unavailable".

### Usage

# PySide6
from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox
# PyQt6
from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox

self.combo = CComboBox(self)
self.combo.addItems(["Egypt", "Tunisia", "Morocco"])
self.lbl = CLabel("Country:", self, self.combo)
layout.addWidget(self.lbl)
layout.addWidget(self.combo)

self.combo.validated.connect(self.on_selection)
self.combo.cleared.connect(self.on_cleared)

def on_selection(self) -> None:
    text  = self.combo.currentText()
    index = self.combo.currentIndex()
    CMessageBox.information(self, "Selection", f"Country: {text}")

def on_cleared(self) -> None:
    CMessageBox.warning(self, "Warning", "Empty list.")

# Disable / re-enable
self.combo.setEnabled(False)
self.combo.setEnabled(True)

## CListWidget

### Definition
CListWidget is an accessible list that replaces QListWidget.

### Why?
QListWidget activates the item immediately during navigation —
an obstacle for blind users.

### Solution
Separation between navigation and activation. NVDA accessibility in disabled mode.

### Features
- Free navigation: ↑↓ without activation.
- Explicit activation: Enter, Return, Space.
- Accessible deactivation: NVDA announces "unavailable".

### Usage

# PySide6
from cwidgets.pyside6 import CListWidget, CLabel
# PyQt6
from cwidgets.pyqt6 import CListWidget, CLabel

self.liste = CListWidget(self)
self.liste.addItems(["Iraq", "Saudi Arabia", "Kuwait"])
self.lbl = CLabel("Country:", self, self.liste)
layout.addWidget(self.lbl)
layout.addWidget(self.liste)

self.liste.itemActivated.connect(self.on_item)

def on_item(self, item) -> None:
    text = item.text()
    row  = self.liste.currentRow()
    print(row, text)

# Disable / re-enable
self.liste.setEnabled(False)
self.liste.setEnabled(True)

# Clear
self.liste.clear()

## CMessageBox

### Definition
CMessageBox is an accessible dialog box that replaces QMessageBox.

### Why?
QMessageBox doesn't offer automatic closing.

### Solution
Addition of a timed mode with automatic closing after a delay.

### Features
- `information`: timed or not, without sound.
- `warning`: timed or not, without sound.
- `critical`: always non-timed + system sound, manual closing required.
- Manual closing always possible before timeout ends.

### Usage

# PySide6
from cwidgets.pyside6 import CMessageBox
# PyQt6
from cwidgets.pyqt6 import CMessageBox

# Information
CMessageBox.information(self, "Success", "File saved.")
CMessageBox.information(self, "Success", "File saved.", timeout=3000)

# Warning
CMessageBox.warning(self, "Warning", "Insufficient disk space.")
CMessageBox.warning(self, "Warning", "Unstable connection.", timeout=4000)

# Error — manual closing + sound
CMessageBox.critical(self, "Error", "File not found.")

## Best Practices

**1 — Titles: always use CLabel with buddy**
# Not recommended
self.combo.setAccessibleName("...")

# Correct
self.lbl = CLabel("Country:", self, self.combo)

**2 — Disabling**: `setEnabled(False)` available on all C* components.

**3 — Activation**
- CLineEdit and CComboBox → `validated` signal
- CListWidget → `itemActivated` signal

**4 — Creation order with buddy**: always create the element before its CLabel.
self.combo = CComboBox(self)
self.lbl   = CLabel("Country:", self, self.combo)

## System Requirements

- PySide6 or PyQt6
- pywin32 — only for CTextEdit (Win32 RichEdit integration)
- Windows only for CTextEdit

## Limitations

- CTextEdit: Windows only (depends on Win32 RichEdit).
- CComboBox and CListWidget: `setAccessibleName` not recommended — replaces the CLabel buddy.
- CButton: gray shadow via stylesheet — Windows doesn't automatically shadow
  the button when kept active for NVDA.

## Developer

Mohamed Hédi Bettaieb (Tunisia)
Email: hedidouz@gmail.com
Design date: May 2026

## Conclusion

CWidgets aims to make Qt applications 100% accessible to blind
developers and users, without sacrificing productivity or Qt habits.