"""
Replay Mode Widget - Interface for CSV file replay and analysis.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QGridLayout, QGroupBox, QTextEdit, QFileDialog, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from csv_source import CSVSource
from csv_parser import parse_csv_line
from telemetry_manager import TelemetryManager
from telemetry_charts import TelemetryCharts
from temporal_analysis_widget import TemporalAnalysisWidget
from file_selector_widget import FileSelectorWidget


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
        
        # Set parent references for track map access
        self.charts.parent_widget = self
        self.temporal_analysis.parent_widget = self
        
        # Connect temporal analysis sync signal to charts
        self.temporal_analysis.data_sync_signal.connect(self.charts.update_data)
        
        # Connect temporal analysis slider directly to charts for cursor control
        self.temporal_analysis.range_slider.valueChanged.connect(self.update_charts_cursor_direct)
        
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
        
        self.stop_btn = QPushButton(" Stop Replay")
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
        main_layout.setSpacing(5)
        
        # Left panel - Current Data
        left_panel = QWidget()
        
        # Create scroll area for left panel
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget for scroll area
        left_content = QWidget()
        left_layout = QVBoxLayout(left_content)
        left_layout.setSpacing(8)
        
        # Current data group
        data_group = QGroupBox(" Current Data")
        data_layout = QGridLayout()
        data_layout.setSpacing(8)
        
        # Speed
        data_layout.addWidget(QLabel("Speed:"), 0, 0)
        self.speed_label = QLabel("-- km/h")
        self.speed_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.speed_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.speed_label, 0, 1)
        
        # RPM
        data_layout.addWidget(QLabel("RPM:"), 0, 2)
        self.rpm_label = QLabel("--")
        self.rpm_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.rpm_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.rpm_label, 0, 3)
        
        # Throttle
        data_layout.addWidget(QLabel("Throttle:"), 1, 0)
        self.throttle_label = QLabel("--%")
        self.throttle_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.throttle_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.throttle_label, 1, 1)
        
        # Temperature
        data_layout.addWidget(QLabel("Temp:"), 1, 2)
        self.temp_label = QLabel("--°C")
        self.temp_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.temp_label.setStyleSheet("color: #dc2626; background: #fef2f2; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.temp_label, 1, 3)
        
        data_group.setLayout(data_layout)
        left_layout.addWidget(data_group)
        
        # Statistics group
        stats_group = QGroupBox(" Statistics")
        stats_layout = QGridLayout()
        stats_layout.setSpacing(6)
        
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
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setFont(QFont("Arial", 8))
        left_layout.addWidget(QLabel("📝 Log :"))
        left_layout.addWidget(self.log_text)
        
        # Add temporal analysis widget in scrollable area
        temporal_group = QGroupBox("🕒 Temporal Analysis")
        temporal_layout = QVBoxLayout()
        temporal_layout.addWidget(self.temporal_analysis)
        temporal_group.setLayout(temporal_layout)
        left_layout.addWidget(temporal_group)
        
        left_content.setLayout(left_layout)
        left_scroll.setWidget(left_content)
        main_layout.addWidget(left_scroll)
        
        # Right panel - Charts
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        
        # Add charts widget
        right_layout.addWidget(self.charts)
        
        right_panel.setLayout(right_layout)
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
        
        # Clear existing data
        self.charts.clear_data()
        self.temporal_analysis.clear_data()
        
        # Load all data from file for initial display
        self.load_all_data_for_charts(self.current_file)
        
        self.replay_thread = ReplayThread(self.current_file)
        self.replay_thread.data_received.connect(self.on_data_received)
        self.replay_thread.error_occurred.connect(self.on_error)
        self.replay_thread.status_changed.connect(self.on_status_changed)
        self.replay_thread.finished.connect(self.on_replay_finished)
        
        self.replay_thread.start()
        
        self.play_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_text.append("+ Replay started")
    
    def load_all_data_for_charts(self, file_path):
        """Load all data from CSV file for initial chart display (curves only, no points)."""
        try:
            from csv_parser import parse_csv_line
            import csv
            
            # Collect all data first
            all_data = []
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    data = parse_csv_line(";".join(row))
                    if data:
                        all_data.append(data)
            
            # Load data into charts without triggering point updates
            for data in all_data:
                # Temporarily disable point updates in charts
                if hasattr(self.charts, '_loading_data'):
                    self.charts._loading_data = True
                else:
                    self.charts._loading_data = True
                
                # Update charts with data (curves only)
                self.charts.update_data(data)
                
                # Update temporal analysis with all data (disable points during loading)
                if hasattr(self.temporal_analysis, 'temporal_graphs'):
                    self.temporal_analysis.temporal_graphs._loading_data = True
                self.temporal_analysis._loading_data = True  # Also disable in TemporalAnalysis
                self.temporal_analysis.update_data(data)
                self.temporal_analysis._loading_data = False  # Re-enable after
                if hasattr(self.temporal_analysis, 'temporal_graphs'):
                    self.temporal_analysis.temporal_graphs._loading_data = False
            
            # Re-enable point updates
            self.charts._loading_data = False
            
            # FORCER la mise à jour du curseur après le chargement
            if hasattr(self.temporal_analysis, 'parent_widget') and self.temporal_analysis.parent_widget and hasattr(self.temporal_analysis.parent_widget, 'charts') and self.temporal_analysis.parent_widget.charts.time_data:
                time_data = self.temporal_analysis.parent_widget.charts.time_data
                max_time = int(time_data[-1])  # Durée max en secondes (arrondie)
                self.temporal_analysis.range_slider.setMaximum(max_time)
            else:
                # Solution de secours : utiliser directement les données des charts
                if self.charts and hasattr(self.charts, 'time_data') and self.charts.time_data:
                    time_data = self.charts.time_data
                    max_time = int(time_data[-1])  # Durée max en secondes (arrondie)
                    self.temporal_analysis.range_slider.setMaximum(max_time)
                        
        except Exception as e:
            print(f"Error loading data for charts: {e}")
    
    def stop_replay(self):
        """Stop CSV file replay and reset all data."""
        if self.replay_thread:
            self.replay_thread.stop()
        
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Reset all data and displays
        self.reset_all_data()
        
        self.log_text.append("- Replay stopped - All data reset")
    
    def reset_all_data(self):
        """Reset all charts, statistics, and displays to initial state."""
        # Clear charts data
        self.charts.clear_data()
        
        # Clear temporal analysis data
        self.temporal_analysis.clear_data()
        
        # Reset current data labels to default
        self.speed_label.setText("-- km/h")
        self.rpm_label.setText("--")
        self.throttle_label.setText("--%")
        self.temp_label.setText("--°C")
        
        # Reset statistics labels to default
        self.max_speed_label.setText("--")
        self.avg_speed_label.setText("--")
        self.max_rpm_label.setText("--")
        self.avg_temp_label.setText("--")
        self.data_count_label.setText("0")
        
        # Reset telemetry manager
        self.manager.reset_stats()
    
    def on_data_received(self, data):
        """Update GUI with received data."""
        # Handle both dict and TelemetryData objects
        if hasattr(data, "speed"):  # TelemetryData object
            self.speed_label.setText(f"{data.speed:.1f} km/h")
            self.rpm_label.setText(f"{data.rpm:.0f}")
            self.throttle_label.setText(f"{data.throttle:.0f}%")
            self.temp_label.setText(f"{data.battery_temp:.1f}°C")
            
            # Update charts with TelemetryData (skip automatic points during replay)
            self.charts._loading_data = True  # Skip automatic points
            self.charts.update_data(data)
            self.charts._loading_data = False  # Re-enable for cursor
            
            # Update temporal analysis
            self.temporal_analysis.update_data(data)
        else:  # Dict object (backward compatibility)
            self.speed_label.setText(f"{data['speed']:.1f} km/h")
            self.rpm_label.setText(f"{data['rpm']:.0f}")
            self.throttle_label.setText(f"{data['throttle']:.0f}%")
            self.temp_label.setText(f"{data['battery_temp']:.1f}°C")
        
        # Update statistics
        if self.replay_thread and hasattr(self.replay_thread, 'manager'):
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
    
    def update_charts_cursor_direct(self, value):
        """Update charts cursor position directly from slider value."""
        if not self.charts or not hasattr(self.charts, 'time_data') or not self.charts.time_data:
            return
        
        if value >= len(self.charts.time_data):
            return
        
        current_time = self.charts.time_data[value]
        
        # Remove only previous cursor markers (items with symbols)
        for plot_name in ['speed_rpm_plot', 'throttle_temp_plot', 'g_force_plot', 'accel_plot']:
            plot = getattr(self.charts, plot_name, None)
            if plot:
                items_to_remove = []
                for item in plot.listDataItems():
                    if hasattr(item, 'symbol') and item.symbol is not None:
                        items_to_remove.append(item)
                for item in items_to_remove:
                    plot.removeItem(item)
        
        # Add current point markers to all charts plots
        plots_to_mark = [
            (self.charts.speed_rpm_plot, 'speed_data', 'rpm_data', '#22c55e', '#f59e0b'),
            (self.charts.throttle_temp_plot, 'throttle_data', 'battery_temp_data', '#3b82f6', '#ef4444'),
            (self.charts.g_force_plot, 'g_force_lat_data', 'g_force_long_data', '#ef4444', '#3b82f6'),
            (self.charts.accel_plot, 'accel_x_data', 'accel_y_data', '#8b5cf6', '#14b8a6'),
        ]
        
        for plot, data1_attr, data2_attr, color1, color2 in plots_to_mark:
            if plot and hasattr(self.charts, data1_attr) and hasattr(self.charts, data2_attr):
                data1 = getattr(self.charts, data1_attr)
                data2 = getattr(self.charts, data2_attr)
                
                if value < len(data1) and value < len(data2):
                    # Add current point markers without clearing the plot - COMMENTED TO REMOVE EXTRA POINTS
                    # plot.plot([current_time], [data1[value]], pen=None, symbol='o', symbolSize=12, symbolBrush=color1, symbolPen='darkred')
                    # plot.plot([current_time], [data2[value]], pen=None, symbol='s', symbolSize=12, symbolBrush=color2, symbolPen='darkorange')
                    pass  # No action needed - points are handled by update_telemetry_charts
        
        # Also call the temporal analysis update_telemetry_charts function
        if hasattr(self.temporal_analysis, 'data_selector'):
            self.temporal_analysis.data_selector.update_telemetry_charts(self.charts, value)
    
    def update_charts_cursor(self, min_val, max_val):
        """Update charts cursor position based on temporal analysis slider."""
        if not self.charts or not hasattr(self.charts, 'time_data') or not self.charts.time_data:
            return
        
        # Use max_val as the current point index
        point_idx = max_val
        if point_idx >= len(self.charts.time_data):
            return
        
        current_time = self.charts.time_data[point_idx]
        
        # Remove only previous cursor markers (items with symbols)
        for plot_name in ['speed_rpm_plot', 'throttle_temp_plot', 'g_force_plot', 'accel_plot']:
            plot = getattr(self.charts, plot_name, None)
            if plot:
                items_to_remove = []
                for item in plot.listDataItems():
                    if hasattr(item, 'symbol') and item.symbol is not None:
                        items_to_remove.append(item)
                for item in items_to_remove:
                    plot.removeItem(item)
        
        # Add current point markers to all charts plots
        plots_to_mark = [
            (self.charts.speed_rpm_plot, 'speed_data', 'rpm_data', '#22c55e', '#f59e0b'),
            (self.charts.throttle_temp_plot, 'throttle_data', 'battery_temp_data', '#3b82f6', '#ef4444'),
            (self.charts.g_force_plot, 'g_force_lat_data', 'g_force_long_data', '#ef4444', '#3b82f6'),
            (self.charts.accel_plot, 'accel_x_data', 'accel_y_data', '#8b5cf6', '#14b8a6'),
        ]
        
        for plot, data1_attr, data2_attr, color1, color2 in plots_to_mark:
            if plot and hasattr(self.charts, data1_attr) and hasattr(self.charts, data2_attr):
                data1 = getattr(self.charts, data1_attr)
                data2 = getattr(self.charts, data2_attr)
                
                if point_idx < len(data1) and point_idx < len(data2):
                    # Add current point markers without clearing the plot - COMMENTED TO REMOVE EXTRA POINTS
                    # plot.plot([current_time], [data1[point_idx]], pen=None, symbol='o', symbolSize=10, symbolBrush=color1, symbolPen='darkred')
                    # plot.plot([current_time], [data2[point_idx]], pen=None, symbol='s', symbolSize=10, symbolBrush=color2, symbolPen='darkorange')
                    pass  # No action needed - points are handled by update_telemetry_charts
    
    def on_status_changed(self, status):
        """Update status log."""
        self.log_text.append(f"- {status}")
    
    def on_replay_finished(self):
        """Handle replay completion."""
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
