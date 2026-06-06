# -*- coding: utf-8 -*-
"""
CWidgets - Accessible Qt Widgets Library

CWidgets provides a comprehensive set of Qt widgets designed with accessibility
as a primary focus. This library offers enhanced components that work seamlessly
with screen readers like NVDA, while maintaining full compatibility with standard
Qt applications.

Key Features:
- Screen reader optimized components
- Keyboard navigation support
- High contrast and visual accessibility options
- ARIA attributes integration
- Focus management improvements
- Compatibility with Qt styling and theming

Available Components:
- CButton: Accessible push button with enhanced keyboard support
- CLabel: Accessible label with proper screen reader associations
- CLineEdit: Input field with validation and accessibility features
- CComboBox: Accessible dropdown list with proper focus management
- CListWidget: List widget optimized for screen reader navigation
- CMessageBox: Accessible dialog boxes with timeout support
- CTextEdit: Rich text editor with full screen reader support
"""

from cwidgets.pyqt6.widgets import (
    CButton,
    CLabel,
    CLineEdit,
    CComboBox,
    CListWidget,
    CMessageBox,
    CTextEdit,
)

# --------------------------------------------------

# Version actuelle de la bibliothèque
__version__ = "0.1.3.post1"

# --------------------------------------------------

# Exports de l'API publique
__all__ = [
    "CButton",
    "CLabel",
    "CLineEdit",
    "CComboBox",
    "CListWidget",
    "CMessageBox",
    "CTextEdit",
]