# -*- coding: utf-8 -*-
"""
cwidgets - Custom accessible widgets for Qt6 (PyQt6/PySide6).

This library provides GUI components optimized for accessibility with screen readers
like NVDA, while maintaining an API similar to standard Qt widgets.
"""

import webbrowser
import os

__author__ = "Mohamed Hédi Bettaieb"
__email__ = "hedidouz@gmail.com"
__version__ = "0.1.0a1"
__license__ = "GPL-3.0-or-later"

# List of available widgets in the module
WIDGETS = [
    "CButton",
    "CLabel",
    "CLineEdit",
    "CComboBox",
    "CListWidget",
    "CMessageBox",
    "CTextEdit",
]

def widgets():
    """
    Display the list of available widgets in the cwidgets module.

    Example usage:
        >>> import cwidgets
        >>> cwidgets.widgets()
        cwidgets — available widgets:
          - CButton
          - CLabel
          - CLineEdit
          - CComboBox
          - CListWidget
          - CMessageBox
          - CTextEdit
    """
    print("\ncwidgets — available widgets:")
    for w in WIDGETS:
        print(f"  - {w}")
    print()

def show_help(lang="en", widget=None):
    """
    Open the module's HTML documentation in the default browser.

    Args:
        lang (str): Documentation language ("en", "fr" or "ar").
        widget (str, optional): Widget name to directly access its section.
                               If None, opens the home page.

    Raises:
        Displays an error message if the language or widget is invalid.
    """
    # Language validation
    if lang not in ("fr", "en", "ar"):
        print('lang must be "en", "fr" or "ar"')
        return

    # Build path to documentation file
    filename = f"Guide_{lang}.html"
    guide = os.path.join(os.path.dirname(__file__), "Docs/Help", filename)
    url = f"file:///{Guide}"

    # Add URL fragment to directly access widget section
    if widget:
        if widget not in WIDGETS:
            print(f'Unknown widget: "{widget}"')
            widgets()
            return
        url += f"#{widget.lower()}"

    webbrowser.open(url)
