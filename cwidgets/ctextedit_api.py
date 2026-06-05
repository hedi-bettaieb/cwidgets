# -*- coding: utf-8 -*-

#ctextedit_api.py
"""
ctextedit_api.py - API reference for CTextEdit
Provides a single function show_api() that prints all public methods
of CTextEdit with their descriptions, readable line by line via NVDA.
"""

# Ordered dictionary of public methods for CTextEdit
# Key   : method signature
# Value : short description
CTEXTEDIT_API = {
    "Content": {
        "append(text)"           : "Appends text to the end",
        "clear()"                : "Clears all content",
        "insertHtml(html)"       : "Inserts text extracted from HTML at cursor position",
        "insertPlainText(text)"  : "Inserts plain text at cursor position",
        "setText(text)"          : "Replaces all content",
        "text()"                 : "Alias for toPlainText()",
        "toPlainText()"          : "Returns content as plain text",
    },
    "Selection": {
        "selectAll()"            : "Selects all text",
        "selectedText()"         : "Returns the selected text",
    },
    "Properties": {
        "isReadOnly()"           : "Returns True if read-only",
        "lineCount()"            : "Returns the number of lines",
        "setReadOnly(bool)"      : "Enables or disables read-only mode",
    },
    "Formatting": {
        "setAlignment(...)"      : "Alignment: left, center, right",
        "setBackgroundColor(...)" : "Background color: name or (R, G, B)",
        "setFont(...)"           : "Font: QFont or (name, size, bold, italic)",
        "setTextColor(...)"      : "Text color: name or (R, G, B)",
    },
    "Clipboard": {
        "copy()"                 : "Copies selection to clipboard",
        "cut()"                  : "Cuts the selection",
        "paste()"                : "Pastes clipboard content",
        "redo()"                 : "Redoes the last undone action",
        "undo()"                 : "Undoes the last action",
    },
    "Focus": {
        "setFocus()"             : "Sets focus to the editor",
    },
    "Signals": {
        "cursorPositionChanged"  : "Signal — emitted when cursor moves",
        "selectionChanged"       : "Signal — emitted when selection changes",
        "textChanged"            : "Signal — emitted when text is modified",
    },
    "Utility": {
        "api()"                  : "Displays this list",
    },
}

def get_api_count() -> int:
    """
    Returns the total number of methods across all categories.

    Returns:
        int: Total number of methods
    """
    return sum(len(methods) for methods in CTEXTEDIT_API.values())

def get_api_keys() -> list:
    """
    Returns the list of category names only.

    Returns:
        list: List of category names
    """
    return list(CTEXTEDIT_API.keys())

def get_methods_by_category(category: str) -> dict:
    """
    Returns all methods for a specific category.

    Args:
        category (str): Category name (e.g., "Content", "Selection")

    Returns:
        dict: Dictionary of methods in the specified category

    Raises:
        KeyError: If the category doesn't exist
    """
    if category not in CTEXTEDIT_API:
        raise KeyError(
            f"Category '{category}' not found. "
            f"Available categories: {list(CTEXTEDIT_API.keys())}"
        )
    return CTEXTEDIT_API[category]

def show_api():
    """
    Prints all public methods of CTextEdit with descriptions.
    Readable line by line via NVDA.

    Usage:
        from cwidgets.pyside6 import CTextEdit
        CTextEdit.api()
    """
    print("\n" + "=" * 55)
    print(f"  CTextEdit — {get_api_count()} public methods available")
    print("=" * 55)

    for category, methods in CTEXTEDIT_API.items():
        print(f"\n  [{category}]")
        for method, description in methods.items():
            print(f"    {method:<30} {description}")

    print("\n" + "=" * 55 + "\n")