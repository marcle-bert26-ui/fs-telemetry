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
if os.environ.get('CI') or not os.environ.get('DISPLAY', ''):
    sys.modules['PyQt5'] = MagicMock()
    sys.modules['PyQt5.QtWidgets'] = MagicMock()
    sys.modules['PyQt5.QtCore'] = MagicMock()
    sys.modules['PyQt5.QtGui'] = MagicMock()
    sys.modules['PyQt5.QtChart'] = MagicMock()
