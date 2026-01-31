"""
Live Mode Widget - Interface for real-time Arduino data acquisition.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QSpinBox, QGridLayout, QGroupBox, QTextEdit, QTabWidget, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import os

from serial_source import SerialSource
from csv_parser import parse_csv_line
from telemetry_manager import TelemetryManager
from csv_logger import CSVLogger
from telemetry_charts import TelemetryCharts
from temporal_analysis_widget import TemporalAnalysisWidget
import app_config as config


class AcquisitionThread(QThread):
    """Worker thread for handling Arduino data acquisition."""
    
    data_received = pyqtSignal(object)  # Emits TelemetryData objects
    error_occurred = pyqtSignal(str)  # Emits error messages
    status_changed = pyqtSignal(str)  # Emits status updates
    
    def __init__(self, port, baudrate):
        """Initialize acquisition thread."""
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = False
        self.source = None
        self.manager = TelemetryManager()
        self.logger = CSVLogger()
        self.charts = TelemetryCharts()
        # self.temporal_analysis = TemporalAnalysisWidget()  # Pas d'interface dans un thread
        
    def run(self):
        """Execute the acquisition loop."""
        try:
            # Initialize serial source
            self.source = SerialSource(self.port, self.baudrate)
            self.status_changed.emit(f"Connected to {self.port}")
            
            # Initialize logger
            self.logger = CSVLogger()
            if self.logger.filepath:
                self.status_changed.emit(f"Logging to {os.path.basename(self.logger.filepath)}")
            else:
                self.status_changed.emit("Logger initialized")
            
            self.running = True
            
            while self.running:
                line = self.source.read()
                
                if not line:
                    continue
                
                # Parse data
                data = parse_csv_line(line)
                if data is None:
                    continue
                
                # Update manager
                self.manager.update(data)
                
                # Log data
                if self.logger:
                    self.logger.log(data)
                
                # Emit data for GUI update
                self.data_received.emit(data)
        
        except Exception as e:
            self.error_occurred.emit(f"Acquisition error: {str(e)}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.running = False
        if self.source:
            self.source.close()
        if self.logger:
            self.logger.close()
        self.status_changed.emit("Acquisition stopped")
    
    def stop(self):
        """Stop the acquisition thread."""
        self.running = False
        self.wait()


class LiveModeWidget(QWidget):
    """Widget for live mode (Arduino data acquisition)."""
    
    def __init__(self):
        """Initialize live mode widget."""
        super().__init__()
        self.acquisition_thread = None
        self.manager = TelemetryManager()
        self.charts = TelemetryCharts()
        self.temporal_analysis = TemporalAnalysisWidget()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create main scroll area for global scrolling
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_scroll.setStyleSheet("""
            QScrollArea {
                background: #1a1a1a;
                border: none;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #4ecdc4;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create main widget to contain all content
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Configuration group
        config_group = QGroupBox("Serial Configuration")
        config_layout = QGridLayout()
        
        config_layout.addWidget(QLabel("Port:"), 0, 0)
        self.port_input = QLineEdit(config.SERIAL_PORT)
        config_layout.addWidget(self.port_input, 0, 1)
        
        config_layout.addWidget(QLabel("Baudrate:"), 0, 2)
        self.baudrate_input = QSpinBox()
        self.baudrate_input.setRange(300, 1000000)
        self.baudrate_input.setValue(9600)  # Force to 9600
        self.baudrate_input.setSingleStep(1)  # Step of 1
        config_layout.addWidget(self.baudrate_input, 0, 3)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Start Acquisition")
        self.start_btn.clicked.connect(self.start_acquisition)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Acquisition")
        self.stop_btn.clicked.connect(self.stop_acquisition)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
            }
        """)
        button_layout.addWidget(self.stop_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Create horizontal layout for parallel views
        main_layout = QHBoxLayout()
        main_layout.setSpacing(5)  # Réduit espacement
        
        # Left panel - Current Data
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(8)  # Réduit espacement
        
        # Current data group (plus compact)
        data_group = QGroupBox("📊 Current Data")
        data_group.setStyleSheet("""
            QGroupBox {
                font-size: 12px;
                font-weight: bold;
                border: 2px solid #1e3a8a;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                color: #1e3a8a;
            }
        """)
        data_layout = QGridLayout()
        data_layout.setSpacing(8)  # Plus compact
        
        # Speed (plus petit)
        data_layout.addWidget(QLabel("Speed:"), 0, 0)
        self.speed_label = QLabel("-- km/h")
        self.speed_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.speed_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.speed_label, 0, 1)
        
        # RPM (plus petit)
        data_layout.addWidget(QLabel("RPM:"), 0, 2)
        self.rpm_label = QLabel("--")
        self.rpm_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.rpm_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.rpm_label, 0, 3)
        
        # Throttle (plus petit)
        data_layout.addWidget(QLabel("Throttle:"), 1, 0)
        self.throttle_label = QLabel("--%")
        self.throttle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.throttle_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.throttle_label, 1, 1)
        
        # Temperature (plus petit)
        data_layout.addWidget(QLabel("Temp:"), 1, 2)
        self.temp_label = QLabel("--°C")
        self.temp_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.temp_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.temp_label, 1, 3)
        
        data_group.setLayout(data_layout)
        left_layout.addWidget(data_group)
        
        # Statistics group (plus compact)
        stats_group = QGroupBox("📈 Statistics")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-size: 12px;
                font-weight: bold;
                border: 2px solid #10b981;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                color: #10b981;
            }
        """)
        stats_layout = QGridLayout()
        stats_layout.setSpacing(6)  # Plus compact
        
        stats_layout.addWidget(QLabel("Max Speed:"), 0, 0)
        self.max_speed_label = QLabel("--")
        self.max_speed_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.max_speed_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.max_speed_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Avg Speed:"), 0, 2)
        self.avg_speed_label = QLabel("--")
        self.avg_speed_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.avg_speed_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.avg_speed_label, 0, 3)
        
        stats_layout.addWidget(QLabel("Data Points:"), 1, 0)
        self.data_count_label = QLabel("0")
        self.data_count_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.data_count_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.data_count_label, 1, 1)
        
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        # Log display (plus petit)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)  # Encore plus petit
        self.log_text.setFont(QFont("Arial", 8))  # Police encore plus petite
        left_layout.addWidget(QLabel("📝 Log:"))
        left_layout.addWidget(self.log_text)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel)
        
        # Right panel - Charts
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)  # Réduit espacement
        
        # Create tab widget for data views
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d1d5db;
                background: #f9fafb;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #e5e7eb;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #3b82f6;
                color: white;
            }
        """)
        
        # Charts tab (no individual scroll - using global scroll)
        tab_widget.addTab(self.charts, "📈 Charts")
        
        right_layout.addWidget(tab_widget)
        main_layout.addWidget(right_panel)
        
        # Configurer les proportions 50/50
        main_layout.setStretch(0, 1)  # Gauche : 1 partie
        main_layout.setStretch(1, 1)  # Droite : 1 partie (50/50)
        
        layout.addLayout(main_layout)
        
        # Set the main widget as the scroll area's widget
        main_scroll.setWidget(main_widget)
        
        # Add scroll area to the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_scroll)
    
    def start_acquisition(self):
        """Start data acquisition from Arduino."""
        port = self.port_input.text()
        baudrate = self.baudrate_input.value()
        
        # Quick reset for new acquisition (lightweight)
        self.charts.quick_clear()
        
        # Reset displays only
        self.speed_label.setText("-- km/h")
        self.rpm_label.setText("--")
        self.throttle_label.setText("--%")
        self.temp_label.setText("--°C")
        self.max_speed_label.setText("--")
        self.avg_speed_label.setText("--")
        self.data_count_label.setText("0")
        
        self.acquisition_thread = AcquisitionThread(port, baudrate)
        self.acquisition_thread.data_received.connect(self.on_data_received)
        self.acquisition_thread.error_occurred.connect(self.on_error)
        self.acquisition_thread.status_changed.connect(self.on_status_changed)
        
        self.acquisition_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.port_input.setEnabled(False)
        self.baudrate_input.setEnabled(False)
        
        self.log_text.append("+ Acquisition started")
    
    def stop_acquisition(self):
        """Stop data acquisition."""
        if self.acquisition_thread:
            self.acquisition_thread.stop()
        
        # Reset all displays to 0
        self.speed_label.setText("-- km/h")
        self.rpm_label.setText("--")
        self.throttle_label.setText("--%")
        self.temp_label.setText("--°C")
        self.max_speed_label.setText("--")
        self.avg_speed_label.setText("--")
        self.data_count_label.setText("0")
        
        # Reset charts to 0 - COMMENTED OUT to keep data for oscilloscope effect
        # self.charts.clear_data()
        
        # Reset temporal analysis
        self.temporal_analysis.clear_data()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.port_input.setEnabled(True)
        self.baudrate_input.setEnabled(True)
        
        self.log_text.append("X Acquisition stopped")
    
    def on_data_received(self, data):
        """Update GUI with received data."""
        # Handle both dict and TelemetryData objects
        if hasattr(data, 'speed'):  # TelemetryData object
            self.speed_label.setText(f"{data.speed:.1f} km/h")
            self.rpm_label.setText(f"{data.rpm:.0f}")
            self.throttle_label.setText(f"{data.throttle:.0f}%")
            self.temp_label.setText(f"{data.battery_temp:.1f}°C")
            
            # Update charts with TelemetryData
            self.charts.update_data(data)
            
            # Update temporal analysis
            self.temporal_analysis.update_data(data)
        else:  # Dict object (backward compatibility)
            self.speed_label.setText(f"{data['speed']:.1f} km/h")
            self.rpm_label.setText(f"{data['rpm']:.0f}")
            self.throttle_label.setText(f"{data['throttle']:.0f}%")
            self.temp_label.setText(f"{data['battery_temp']:.1f}°C")
        
        # Update statistics
        stats = self.acquisition_thread.manager.get_stats()
        if stats:
            self.max_speed_label.setText(f"{stats.get('max_speed', 0):.1f} km/h")
            self.avg_speed_label.setText(f"{stats.get('avg_speed', 0):.1f} km/h")
            self.data_count_label.setText(f"{stats.get('data_points', 0)}")
    
    def on_error(self, error_msg):
        """Handle acquisition errors."""
        self.log_text.append(f"X Error: {error_msg}")
        self.stop_acquisition()
    
    def on_status_changed(self, status):
        """Update status log."""
        self.log_text.append(f"- {status}")
