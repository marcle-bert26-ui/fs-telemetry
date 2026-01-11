"""
Live Mode Widget - Interface for real-time Arduino data acquisition.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QSpinBox, QGridLayout, QGroupBox, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from acquisition.serial_source import SerialSource
from parsing.csv_parser import parse_csv_line
from data.telemetry_manager import TelemetryManager
from log_handlers.csv_logger import CSVLogger
import config


class AcquisitionThread(QThread):
    """Worker thread for handling Arduino data acquisition."""
    
    data_received = pyqtSignal(dict)  # Emits processed data
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
        self.logger = None
    
    def run(self):
        """Execute the acquisition loop."""
        try:
            # Initialize serial source
            self.source = SerialSource(self.port, self.baudrate)
            self.status_changed.emit(f"Connected to {self.port}")
            
            # Initialize logger
            self.logger = CSVLogger()
            self.status_changed.emit(f"Logging to {self.logger.filepath.name}")
            
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
                self.data_received.emit({
                    'time_ms': data.time_ms,
                    'speed': data.speed,
                    'rpm': data.rpm,
                    'throttle': data.throttle,
                    'battery_temp': data.battery_temp,
                })
        
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
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
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
        self.baudrate_input.setValue(config.SERIAL_BAUDRATE)
        self.baudrate_input.setMaximum(1000000)
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
        
        # Data display group
        data_group = QGroupBox("Real-time Telemetry Data")
        data_layout = QGridLayout()
        
        # Speed
        data_layout.addWidget(QLabel("Speed:"), 0, 0)
        self.speed_label = QLabel("-- km/h")
        self.speed_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.speed_label.setStyleSheet("color: #1e3a8a;")
        data_layout.addWidget(self.speed_label, 0, 1)
        
        # RPM
        data_layout.addWidget(QLabel("RPM:"), 0, 2)
        self.rpm_label = QLabel("--")
        self.rpm_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.rpm_label.setStyleSheet("color: #1e3a8a;")
        data_layout.addWidget(self.rpm_label, 0, 3)
        
        # Throttle
        data_layout.addWidget(QLabel("Throttle:"), 1, 0)
        self.throttle_label = QLabel("--%")
        self.throttle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.throttle_label.setStyleSheet("color: #1e3a8a;")
        data_layout.addWidget(self.throttle_label, 1, 1)
        
        # Temperature
        data_layout.addWidget(QLabel("Temperature:"), 1, 2)
        self.temp_label = QLabel("--°C")
        self.temp_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.temp_label.setStyleSheet("color: #1e3a8a;")
        data_layout.addWidget(self.temp_label, 1, 3)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # Statistics group
        stats_group = QGroupBox("Session Statistics")
        stats_layout = QGridLayout()
        
        stats_layout.addWidget(QLabel("Max Speed:"), 0, 0)
        self.max_speed_label = QLabel("--")
        stats_layout.addWidget(self.max_speed_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Avg Speed:"), 0, 2)
        self.avg_speed_label = QLabel("--")
        stats_layout.addWidget(self.avg_speed_label, 0, 3)
        
        stats_layout.addWidget(QLabel("Data Points:"), 1, 0)
        self.data_count_label = QLabel("0")
        stats_layout.addWidget(self.data_count_label, 1, 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Status Log:"))
        layout.addWidget(self.log_text)
        
        layout.addStretch()
    
    def start_acquisition(self):
        """Start data acquisition from Arduino."""
        port = self.port_input.text()
        baudrate = self.baudrate_input.value()
        
        self.acquisition_thread = AcquisitionThread(port, baudrate)
        self.acquisition_thread.data_received.connect(self.on_data_received)
        self.acquisition_thread.error_occurred.connect(self.on_error)
        self.acquisition_thread.status_changed.connect(self.on_status_changed)
        
        self.acquisition_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.port_input.setEnabled(False)
        self.baudrate_input.setEnabled(False)
        
        self.log_text.append("✓ Acquisition started")
    
    def stop_acquisition(self):
        """Stop data acquisition."""
        if self.acquisition_thread:
            self.acquisition_thread.stop()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.port_input.setEnabled(True)
        self.baudrate_input.setEnabled(True)
        
        self.log_text.append("⏹ Acquisition stopped")
    
    def on_data_received(self, data):
        """Update GUI with received data."""
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
        self.log_text.append(f"✗ Error: {error_msg}")
        self.stop_acquisition()
    
    def on_status_changed(self, status):
        """Update status log."""
        self.log_text.append(f"• {status}")
