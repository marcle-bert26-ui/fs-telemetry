"""
Pytest configuration and shared fixtures for all tests.
"""

import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

# Detect if we're in CI or headless environment FIRST, before any other imports
is_ci = os.environ.get('CI') == 'true'
has_display = os.environ.get('DISPLAY', '') != ''
is_headless = (not has_display) or is_ci

# Mock PyQt5 IMMEDIATELY if headless - before any module imports
if is_headless or 'pytest' in sys.modules:
    # Create comprehensive mocks for all PyQt5 modules
    def create_mock():
        mock = MagicMock()
        # Ensure common attributes exist to prevent AttributeError
        mock.QWidget = MagicMock()
        mock.QVBoxLayout = MagicMock()
        mock.QHBoxLayout = MagicMock()
        mock.QLabel = MagicMock()
        mock.QPushButton = MagicMock()
        mock.QLineEdit = MagicMock()
        mock.QGridLayout = MagicMock()
        mock.QGroupBox = MagicMock()
        mock.QTextEdit = MagicMock()
        mock.QFileDialog = MagicMock()
        mock.QApplication = MagicMock()
        mock.QMainWindow = MagicMock()
        return mock
    
    # Mock all PyQt5 modules
    sys.modules['PyQt5'] = MagicMock()
    sys.modules['PyQt5.QtWidgets'] = create_mock()
    sys.modules['PyQt5.QtCore'] = create_mock()
    sys.modules['PyQt5.QtGui'] = create_mock()
    sys.modules['PyQt5.QtChart'] = create_mock()
