"""
Replay Mode Widget - Interface for CSV file replay and analysis.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QGridLayout, QGroupBox, QTextEdit, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from acquisition.csv_source import CSVSource
from parsing.csv_parser import parse_csv_line
from data.telemetry_manager import TelemetryManager


class ReplayThread(QThread):
    """Worker thread for CSV file replay."""
    
    data_received = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, csv_file):
        """Initialize replay thread."""
        super().__init__()
        self.csv_file = csv_file
        self.running = False
        self.manager = TelemetryManager()
    
    def run(self):
        """Execute the replay loop."""
        try:
            source = CSVSource(self.csv_file)
            self.status_changed.emit(f"Opened: {self.csv_file}")
            
            self.running = True
            
            # Skip header
            source.read()
            
            while self.running:
                line = source.read()
                
                if not line:
                    break
                
                # Parse data
                data = parse_csv_line(line)
                if data is None:
                    continue
                
                # Update manager
                self.manager.update(data)
                
                # Emit data for GUI update
                self.data_received.emit({
                    'time_ms': data.time_ms,
                    'speed': data.speed,
                    'rpm': data.rpm,
                    'throttle': data.throttle,
                    'battery_temp': data.battery_temp,
                })
            
            source.close()
            self.status_changed.emit("Replay finished")
            self.finished.emit()
        
        except Exception as e:
            self.error_occurred.emit(f"Replay error: {str(e)}")
    
    def stop(self):
        """Stop the replay thread."""
        self.running = False
        self.wait()


class ReplayModeWidget(QWidget):
    """Widget for replay mode (CSV file analysis)."""
    
    def __init__(self):
        """Initialize replay mode widget."""
        super().__init__()
        self.replay_thread = None
        self.current_file = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # File selection group
        file_group = QGroupBox("Select CSV File")
        file_layout = QHBoxLayout()
        
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select a CSV file to replay...")
        file_layout.addWidget(self.file_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        file_layout.addWidget(browse_btn)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶ Start Replay")
        self.play_btn.clicked.connect(self.start_replay)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
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
        button_layout.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Replay")
        self.stop_btn.clicked.connect(self.stop_replay)
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
        data_group = QGroupBox("Current Data Point")
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
        
        stats_layout.addWidget(QLabel("Max RPM:"), 1, 0)
        self.max_rpm_label = QLabel("--")
        stats_layout.addWidget(self.max_rpm_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Avg Temperature:"), 1, 2)
        self.avg_temp_label = QLabel("--")
        stats_layout.addWidget(self.avg_temp_label, 1, 3)
        
        stats_layout.addWidget(QLabel("Data Points:"), 2, 0)
        self.data_count_label = QLabel("0")
        stats_layout.addWidget(self.data_count_label, 2, 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Replay Log:"))
        layout.addWidget(self.log_text)
        
        layout.addStretch()
    
    def browse_file(self):
        """Open file dialog to select CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.file_input.setText(file_path)
            self.current_file = file_path
    
    def start_replay(self):
        """Start CSV file replay."""
        if not self.current_file:
            self.log_text.append("✗ Please select a CSV file")
            return
        
        self.replay_thread = ReplayThread(self.current_file)
        self.replay_thread.data_received.connect(self.on_data_received)
        self.replay_thread.error_occurred.connect(self.on_error)
        self.replay_thread.status_changed.connect(self.on_status_changed)
        self.replay_thread.finished.connect(self.on_replay_finished)
        
        self.replay_thread.start()
        
        self.play_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.file_input.setEnabled(False)
        
        self.log_text.append("✓ Replay started")
    
    def stop_replay(self):
        """Stop CSV file replay."""
        if self.replay_thread:
            self.replay_thread.stop()
        
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.file_input.setEnabled(True)
        
        self.log_text.append("⏹ Replay stopped")
    
    def on_data_received(self, data):
        """Update GUI with received data."""
        self.speed_label.setText(f"{data['speed']:.1f} km/h")
        self.rpm_label.setText(f"{data['rpm']:.0f}")
        self.throttle_label.setText(f"{data['throttle']:.0f}%")
        self.temp_label.setText(f"{data['battery_temp']:.1f}°C")
        
        # Update statistics
        stats = self.replay_thread.manager.get_stats()
        if stats:
            self.max_speed_label.setText(f"{stats.get('max_speed', 0):.1f} km/h")
            self.avg_speed_label.setText(f"{stats.get('avg_speed', 0):.1f} km/h")
            self.max_rpm_label.setText(f"{stats.get('max_rpm', 0):.0f}")
            self.avg_temp_label.setText(f"{stats.get('avg_temp', 0):.1f}°C")
            self.data_count_label.setText(f"{stats.get('data_points', 0)}")
    
    def on_error(self, error_msg):
        """Handle replay errors."""
        self.log_text.append(f"✗ Error: {error_msg}")
        self.stop_replay()
    
    def on_status_changed(self, status):
        """Update status log."""
        self.log_text.append(f"• {status}")
    
    def on_replay_finished(self):
        """Handle replay completion."""
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.file_input.setEnabled(True)
