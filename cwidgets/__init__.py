# -*- coding: utf-8 -*-
"""
cwidgets - Custom accessible widgets for Qt6 (PyQt6/PySide6).
This library provides GUI components optimized for accessibility with screen readers
like NVDA, while maintaining an API similar to standard Qt widgets.
"""
import logging
import os
import re
import tempfile
import webbrowser

__author__ = "Mohamed Hédi Bettaieb (Tunisia)"
__email__ = "hedidouz@gmail.com"
__version__ = "0.1.2"
__license__ = "GPL-3.0-or-later"

# ------------------------------------------------------------------ #
#  Logger configuration                                               #
# ------------------------------------------------------------------ #
_logger = logging.getLogger("cwidgets")
_logger.setLevel(logging.DEBUG)

if not _logger.handlers:
    _log_file = None
    _file_handler = None

    appdata_dir = os.environ.get("APPDATA", "")
    if appdata_dir:
        _cwidgets_dir = os.path.join(appdata_dir, "cwidgets")
        try:
            os.makedirs(_cwidgets_dir, exist_ok=True)
            _log_file = os.path.join(_cwidgets_dir, "cwidgets.log")
            _file_handler = logging.FileHandler(_log_file, mode="w", encoding="utf-8")
        except Exception:
            _log_file = None

    if not _log_file:
        try:
            _log_file = os.path.join(tempfile.gettempdir(), "cwidgets.log")
            _file_handler = logging.FileHandler(_log_file, mode="w", encoding="utf-8")
        except Exception:
            _file_handler = None

    if _file_handler:
        _file_handler.setLevel(logging.DEBUG)
        _file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        _logger.addHandler(_file_handler)
        _logger.propagate = False
        _logger.debug(f"Log file: {_log_file}")

# ------------------------------------------------------------------ #
#  Available widgets and sections                                     #
# ------------------------------------------------------------------ #
WIDGETS = [
    "CTextEdit",    
    "CButton",
    "CLabel",
    "CLineEdit",
    "CComboBox",
    "CListWidget",
    "CMessageBox",
]

SECTIONS = [
    "introduction",
    "widgets-list",
    "installation",
    "show-help",
    "common-issues",
    "widgets-details",
    "best-practices",
    "requirements",
    "limits",
    "developer",
    "conclusion",
]

# ------------------------------------------------------------------ #
#  Public functions                                                   #
# ------------------------------------------------------------------ #

def widgets():
    """
    Display the list of available widgets in the cwidgets module.

    Example usage:
        >>> import cwidgets
        >>> cwidgets.widgets()
        cwidgets — available widgets:
          - CButton
          - CLabel
          ...
    """
    print("\ncwidgets — available widgets:")
    for w in WIDGETS:
        print(f"  - {w}")
    print()


def sections():
    """
    Display the list of available sections in the help guide.

    Example usage:
        >>> import cwidgets
        >>> cwidgets.sections()
        cwidgets — available sections:
          - introduction
          - installation
          ...
    """
    print("\ncwidgets — available sections:")
    for s in SECTIONS:
        print(f"  - {s}")
    print()


def show_help(lang="en", goto=None):
    """
    Open the module's HTML documentation in the default browser.

    Args:
        lang (str): Documentation language — "en", "fr" or "ar". Default: "en".
        goto (str, optional): Widget name or section id to directly access.
                              If None, opens the full guide.

    Example usage:
        >>> import cwidgets
        >>> cwidgets.show_help()
        >>> cwidgets.show_help(lang="fr")
        >>> cwidgets.show_help(lang="fr", goto="CButton")
        >>> cwidgets.show_help(lang="ar", goto="introduction")
    """
    if lang not in ("fr", "en", "ar"):
        print('lang must be "en", "fr" or "ar"')
        return

    filename = f"Guide_{lang}.html"
    guide = os.path.join(os.path.dirname(__file__), "Docs", "Help", filename)

    if not os.path.exists(guide):
        print(f'Guide not found: {filename}')
        return

    try:
        with open(guide, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f'Failed to read guide: {e}')
        return

    if goto:
        # normaliser — widget ou section
        goto_id = goto.lower()
        # vérifier si c'est un widget ou une section
        all_ids = [w.lower() for w in WIDGETS] + SECTIONS
        if goto_id not in all_ids:
            print(f'Unknown target: "{goto}"')
            widgets()
            sections()
            return

        # extraire la section — h1 ou h2 avec cet id
        pattern = rf'(<(?:h1|h2)[^>]*id="{goto_id}".*?)(?=<h1|<h2|$)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if not match:
            print(f'Section "{goto}" not found in guide.')
            return

        section_content = match.group(1)
        head_match = re.search(r'<head>.*?</head>', content, re.DOTALL)
        head = head_match.group(0) if head_match else "<head><meta charset='UTF-8'></head>"
        content = f"<!DOCTYPE html><html lang='{lang}'>{head}<body>{section_content}</body></html>"

    try:
        tmp_name = f"cwidgets_help_{lang}.html"
        tmp_path = os.path.join(tempfile.gettempdir(), tmp_name)

        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)

        url = f"file:///{tmp_path.replace(chr(92), '/')}"
        webbrowser.open(url)

    except Exception as e:
        print(f'Failed to open help: {e}')

