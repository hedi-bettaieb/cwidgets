# -*- coding: utf-8 -*-
"""
QWidget parent validation module for all CWidgets components.

This module provides parent widget validation functionality that is called
as the first operation in every CWidgets component constructor to ensure
proper widget hierarchy and accessibility compliance.
"""

import sys
import logging
from PyQt6.QtWidgets import QWidget

# Logger for CWidgets components
logger = logging.getLogger("cwidgets")

class CWidgetError(TypeError):
    """Exception raised when an invalid parent widget is provided to a CWidget component."""
    pass

def validate_parent(parent, widget_name: str = "CWidget"):
    """
    Validates that the provided parent is either None or a valid QWidget instance.

    When validation fails, this function:
    1. Logs the error with detailed information
    2. Prints a formatted error message to stderr
    3. Raises a CWidgetError to prevent widget creation

    Args:
        parent: The parent widget instance to validate
        widget_name: Name of the CWidget component being created

    Returns:
        The original parent if valid, or None if parent was None

    Raises:
        CWidgetError: If parent is neither None nor a QWidget instance

    Note:
        This validation is critical for:
        - Proper widget hierarchy management
        - Accessibility features integration
        - Qt signal/slot connections
    """
    if parent is None:
        return None

    if not isinstance(parent, QWidget):
        # Formatted error message with solution example
        error_msg = (
            f"\n{'=' * 60}\n"
            f"  [CWIDGETS VALIDATION ERROR] {widget_name}\n"
            f"{'=' * 60}\n"
            f"  Invalid parent type: {type(parent).__name__}\n"
            f"  Required type:       QWidget (QMainWindow, QDialog, QWidget, etc.)\n"
            f"\n"
            f"  SOLUTION:\n"
            f"    class MainWindow(QMainWindow):\n"
            f"        def __init__(self):\n"
            f"            super().__init__()\n"
            f"            self.ui = {widget_name}(parent=self)  # Correct usage\n"
            f"{'=' * 60}\n"
        )

        logger.error(error_msg)
        print(error_msg, file=sys.stderr)

        raise CWidgetError(
            f"{widget_name} creation failed: expected QWidget parent, "
            f"got {type(parent).__name__} instead."
        )

    return parent
