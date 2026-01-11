"""
Pytest configuration and shared fixtures for all tests.
"""

import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock PyQt5 modules for headless testing (CI/CD environments)
# Detect if we're in CI or headless environment
is_ci = os.environ.get('CI') == 'true'
has_display = os.environ.get('DISPLAY', '') != ''
is_headless = (not has_display) or is_ci

if is_headless:
    # Create mocks before any imports
    qt_widgets = MagicMock()
    qt_core = MagicMock()
    qt_gui = MagicMock()
    qt_chart = MagicMock()
    
    sys.modules['PyQt5'] = MagicMock()
    sys.modules['PyQt5.QtWidgets'] = qt_widgets
    sys.modules['PyQt5.QtCore'] = qt_core
    sys.modules['PyQt5.QtGui'] = qt_gui
    sys.modules['PyQt5.QtChart'] = qt_chart
    
    # Make sure common attributes exist
    qt_core.Qt = MagicMock()
    qt_core.QThread = MagicMock()
    qt_core.pyqtSignal = MagicMock(return_value=MagicMock())
    qt_core.QTimer = MagicMock()
    
    qt_gui.QFont = MagicMock()
    qt_gui.QColor = MagicMock()
