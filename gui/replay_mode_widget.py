"""
Replay Mode Widget - Interface for CSV file replay and analysis.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QGridLayout, QGroupBox, QTextEdit, QFileDialog, QTabWidget, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from acquisition.csv_source import CSVSource
from parsing.csv_parser import parse_csv_line
from data.telemetry_manager import TelemetryManager
from visualization.telemetry_charts import TelemetryCharts
from gui.temporal_analysis_widget import TemporalAnalysisWidget
from gui.file_selector import FileSelectorWidget


class ReplayThread(QThread):
    """Worker thread for CSV file replay."""
    
    data_received = pyqtSignal(object)
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
                self.data_received.emit(data)
            
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
        # Initialize components
        self.charts = TelemetryCharts()
        self.temporal_analysis = TemporalAnalysisWidget()
        self.manager = TelemetryManager()
        self.replay_thread = None
        self.current_file = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # File selection group
        file_group = QGroupBox("📁 CSV File Selection")
        file_layout = QVBoxLayout()
        
        # Create file selector widget
        self.file_selector = FileSelectorWidget()
        self.file_selector.file_selected.connect(self.on_file_selected)
        
        file_layout.addWidget(self.file_selector)
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
        
        # Create horizontal layout for parallel views
        main_layout = QHBoxLayout()
        main_layout.setSpacing(5)  # Réduit espacement
        
        # Left panel - Current Data (plus petit)
        left_panel = QWidget()
        left_panel.setMaximumWidth(350)  # Limite largeur du panneau gauche
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
        self.temp_label.setStyleSheet("color: #dc2626; background: #fef2f2; padding: 6px; border-radius: 4px; min-width: 100px;")  # Rouge pour température
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
        
        stats_layout.addWidget(QLabel("Max RPM:"), 1, 0)
        self.max_rpm_label = QLabel("--")
        self.max_rpm_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.max_rpm_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.max_rpm_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Avg Temp:"), 1, 2)
        self.avg_temp_label = QLabel("--")
        self.avg_temp_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.avg_temp_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.avg_temp_label, 1, 3)
        
        stats_layout.addWidget(QLabel("Data Points:"), 2, 0)
        self.data_count_label = QLabel("0")
        self.data_count_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.data_count_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.data_count_label, 2, 1)
        
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        # Log display (plus petit)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)  # Encore plus petit
        self.log_text.setFont(QFont("Arial", 8))  # Police encore plus petite
        left_layout.addWidget(QLabel("📝 Log :"))
        left_layout.addWidget(self.log_text)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel)  # Pas de ratio fixe, largeur limitée
        
        # Right panel - Charts (tout le reste)
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
        
        # Charts tab (sans scroll area double)
        tab_widget.addTab(self.charts, "📈 Charts")
        
        # Temporal analysis tab
        tab_widget.addTab(self.temporal_analysis, "⏱️ Temporal Analysis")
        
        right_layout.addWidget(tab_widget)
        main_layout.addWidget(right_panel)  # Prend tout le reste de l'espace
        
        layout.addLayout(main_layout)
        
        layout.addStretch()
    
    def on_file_selected(self, file_path):
        """Handle file selection from file selector."""
        self.current_file = file_path
    
    def browse_file(self):
        """Open file dialog to select CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "tests",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.on_file_selected(file_path)
    
    def start_replay(self):
        """Start CSV file replay."""
        if not self.current_file:
            return
        
        self.replay_thread = ReplayThread(self.current_file)
        self.replay_thread.data_received.connect(self.on_data_received)
        self.replay_thread.error_occurred.connect(self.on_error)
        self.replay_thread.status_changed.connect(self.on_status_changed)
        self.replay_thread.finished.connect(self.on_replay_finished)
        
        self.replay_thread.start()
        
        self.play_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_text.append("+ Replay started")
    
    def stop_replay(self):
        """Stop CSV file replay."""
        if self.replay_thread:
            self.replay_thread.stop()
        
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self.log_text.append("- Replay stopped")
    
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
        stats = self.replay_thread.manager.get_stats()
        if stats:
            self.max_speed_label.setText(f"{stats.get('max_speed', 0):.1f} km/h")
            self.avg_speed_label.setText(f"{stats.get('avg_speed', 0):.1f} km/h")
            self.max_rpm_label.setText(f"{stats.get('max_rpm', 0):.0f}")
            self.avg_temp_label.setText(f"{stats.get('avg_temp', 0):.1f}°C")
            self.data_count_label.setText(f"{stats.get('data_points', 0)}")
    
    def on_error(self, error_msg):
        """Handle replay errors."""
        self.log_text.append(f"X Error: {error_msg}")
        self.stop_replay()
    
    def on_status_changed(self, status):
        """Update status log."""
        self.log_text.append(f"- {status}")
    
    def on_replay_finished(self):
        """Handle replay completion."""
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
