"""
Unit tests for GUI components.
Tests PyQt5 widgets and UI interactions.
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock

# Mock pyqtgraph avant l'import des modules GUI
pg_mock = MagicMock()
pg_mock.setConfigOptions = Mock()
pg_mock.PlotWidget = Mock
pg_mock.ViewBox = Mock
pg_mock.AxisItem = Mock
pg_mock.LegendItem = Mock
pg_mock.PlotDataItem = Mock
pg_mock.InfiniteLine = Mock
sys.modules['pyqtgraph'] = pg_mock


class TestGUIComponents:
    """Test GUI components functionality."""
    
    def test_gui_imports(self):
        """Test that GUI modules can be imported."""
        try:
            from gui.replay_mode_widget import ReplayModeWidget
            from gui.file_selector import FileSelectorWidget
            assert True  # Imports successful
        except ImportError as e:
            pytest.fail(f"Failed to import GUI modules: {e}")
    
    def test_telemetry_charts_import(self):
        """Test that telemetry charts can be imported."""
        try:
            from visualization.telemetry_charts import TelemetryCharts
            assert TelemetryCharts is not None
        except ImportError as e:
            pytest.fail(f"Failed to import TelemetryCharts: {e}")
    
    def test_telemetry_data_creation(self):
        """Test TelemetryData creation for GUI tests."""
        from parsing.csv_parser import TelemetryData
        
        # Create test data
        test_data = TelemetryData(
            time_ms=1000,
            speed=50.0,
            rpm=5000,
            throttle=75.0,
            battery_temp=60.0,
            g_force_lat=0.0,
            g_force_long=0.0,
            g_force_vert=1.0,
            acceleration_x=0.0,
            acceleration_y=0.0,
            acceleration_z=0.0,
            gps_latitude=0.0,
            gps_longitude=0.0,
            gps_altitude=0.0,
            tire_temp_fl=0.0,
            tire_temp_fr=0.0,
            tire_temp_rl=0.0,
            tire_temp_rr=0.0
        )
        
        # Verify data
        assert test_data.time_ms == 1000
        assert test_data.speed == 50.0
        assert test_data.rpm == 5000
        assert test_data.throttle == 75.0
        assert test_data.battery_temp == 60.0
    
    def test_main_window_import(self):
        """Test that main window can be imported."""
        try:
            from gui.main_window import MainWindow
            assert MainWindow is not None
        except ImportError as e:
            pytest.fail(f"Failed to import MainWindow: {e}")
    
    def test_gui_module_structure(self):
        """Test that GUI modules have correct structure."""
        import gui
        import visualization
        
        # Check main modules exist
        assert hasattr(gui, 'replay_mode_widget')
        assert hasattr(gui, 'main_window')
        assert hasattr(visualization, 'telemetry_charts')
        assert hasattr(visualization, 'spider_charts')
    
    def test_pyqtgraph_mock_works(self):
        """Test that pyqtgraph mock is working correctly."""
        import pyqtgraph as pg
        
        # Should be able to call setConfigOptions without error
        pg.setConfigOptions({'useOpenGL': False})
        
        # Should have mocked classes
        assert pg.PlotWidget is not None
        assert pg.ViewBox is not None
    
    def test_gui_components_classes_exist(self):
        """Test that GUI component classes exist."""
        from gui.replay_mode_widget import ReplayModeWidget
        from gui.file_selector import FileSelectorWidget
        from gui.main_window import MainWindow
        from visualization.telemetry_charts import TelemetryCharts
        
        # Check classes exist
        assert ReplayModeWidget is not None
        assert FileSelectorWidget is not None
        assert MainWindow is not None
        assert TelemetryCharts is not None
