"""
Configuration pytest pour les tests CI/CD.
Mock les dépendances GUI pour éviter les erreurs d'import.
"""

import sys
import os
from unittest.mock import Mock, MagicMock

# Mock PyQt5
pyqt5_mock = MagicMock()
pyqt5_mock.QtCore = MagicMock()
pyqt5_mock.QtWidgets = MagicMock()
pyqt5_mock.QtGui = MagicMock()
pyqt5_mock.QtCore.Qt = MagicMock()
pyqt5_mock.QtCore.QThread = MagicMock()
pyqt5_mock.QtCore.pyqtSignal = MagicMock()
pyqt5_mock.QtWidgets.QApplication = MagicMock()
pyqt5_mock.QtWidgets.QWidget = MagicMock()
pyqt5_mock.QtWidgets.QVBoxLayout = MagicMock()
pyqt5_mock.QtWidgets.QHBoxLayout = MagicMock()
pyqt5_mock.QtWidgets.QLabel = MagicMock()
pyqt5_mock.QtWidgets.QPushButton = MagicMock()
pyqt5_mock.QtWidgets.QLineEdit = MagicMock()
pyqt5_mock.QtWidgets.QSpinBox = MagicMock()
pyqt5_mock.QtWidgets.QGridLayout = MagicMock()
pyqt5_mock.QtWidgets.QGroupBox = MagicMock()
pyqt5_mock.QtWidgets.QTextEdit = MagicMock()
pyqt5_mock.QtWidgets.QFileDialog = MagicMock()
pyqt5_mock.QtWidgets.QScrollArea = MagicMock()
pyqt5_mock.QtWidgets.QTabWidget = MagicMock()
pyqt5_mock.QtWidgets.QSlider = MagicMock()
pyqt5_mock.QtGui.QFont = MagicMock()
pyqt5_mock.QtGui.QColor = MagicMock()
pyqt5_mock.QtGui.QPainter = MagicMock()
pyqt5_mock.QtGui.QPen = MagicMock()
pyqt5_mock.QtGui.QBrush = MagicMock()
pyqt5_mock.QtGui.QPolygonF = MagicMock()
pyqt5_mock.QtCore.QPointF = MagicMock()
pyqt5_mock.QtCore.QRectF = MagicMock()

sys.modules['PyQt5'] = pyqt5_mock
sys.modules['PyQt5.QtCore'] = pyqt5_mock.QtCore
sys.modules['PyQt5.QtWidgets'] = pyqt5_mock.QtWidgets
sys.modules['PyQt5.QtGui'] = pyqt5_mock.QtGui

# Mock pyqtgraph
pg_mock = MagicMock()
pg_mock.setConfigOptions = Mock()
pg_mock.PlotWidget = Mock
pg_mock.ViewBox = Mock
pg_mock.AxisItem = Mock
pg_mock.LegendItem = Mock
pg_mock.PlotDataItem = Mock
pg_mock.InfiniteLine = Mock
pg_mock.Qt = pyqt5_mock
sys.modules['pyqtgraph'] = pg_mock

# Mock serial pour les tests sans hardware
serial_mock = MagicMock()
serial_mock.Serial = MagicMock()
sys.modules['serial'] = serial_mock
sys.modules['serial.tools'] = MagicMock()
sys.modules['serial.tools.list_ports'] = MagicMock()

# Détecter si nous sommes dans un environnement CI/CD
def is_ci_environment():
    """Détecte si nous sommes dans un environnement CI/CD."""
    return (
        os.getenv('CI') == 'true' or
        os.getenv('GITHUB_ACTIONS') == 'true' or
        os.getenv('TRAVIS') == 'true' or
        os.getenv('CIRCLECI') == 'true' or
        'DISPLAY' not in os.environ  # Pas de display X
    )

# Appliquer les mocks seulement en CI
if is_ci_environment():
    print("🤖 CI Environment detected - Applying GUI mocks")
    
    # Marquer les tests GUI pour les exclure
    import pytest
    
    def pytest_collection_modifyitems(config, items):
        """Exclure les tests GUI en CI."""
        skip_gui = pytest.mark.skip(reason="GUI test skipped in CI environment")
        for item in items:
            if "gui" in item.nodeid.lower() or "temporal" in item.nodeid.lower():
                item.add_marker(skip_gui)
    
    # Hook pytest
    pytest_collection_modifyitems = pytest_collection_modifyitems
