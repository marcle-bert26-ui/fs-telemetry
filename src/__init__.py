"""
FS Telemetry - Formula Student Telemetry System

Main package for telemetry data processing, visualization, and analysis.
"""

# Core modules
from .core import TelemetryManager, TelemetrySource

# Data handling
from .data import TelemetryData, CSV_HEADER, parse_csv_line, CSVLogger, CSVSource

# External sources
from .sources import SerialSource

# GUI components
from .gui import MainWindow, LiveModeWidget, ReplayModeWidget, TemporalAnalysisWidget, FileSelectorWidget

# Visualization
from .visualization import TelemetryCharts, SpiderChartWidget

# Utilities
from .utils import ConsoleDisplay, ConsoleHandler, ReplayThread

__all__ = [
    # Core
    'TelemetryManager',
    'TelemetrySource',
    
    # Data
    'TelemetryData',
    'CSV_HEADER',
    'parse_csv_line', 
    'CSVLogger',
    'CSVSource',
    
    # Sources
    'SerialSource',
    
    # GUI
    'MainWindow',
    'LiveModeWidget',
    'ReplayModeWidget', 
    'TemporalAnalysisWidget',
    'FileSelectorWidget',
    
    # Visualization
    'TelemetryCharts',
    'SpiderChartWidget',
    
    # Utils
    'ConsoleDisplay',
    'ConsoleHandler',
    'ReplayThread'
]
