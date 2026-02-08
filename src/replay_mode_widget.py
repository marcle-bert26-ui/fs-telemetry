"""
Replay Mode Widget - Interface for CSV file replay and analysis.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QLineEdit, QGridLayout, QGroupBox, QTextEdit, QFileDialog, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .csv_source import CSVSource
from .csv_parser import TelemetryData, parse_csv_line
from .telemetry_manager import TelemetryManager
from .telemetry_charts import TelemetryCharts
from .temporal_analysis_widget import TemporalAnalysisWidget
from .file_selector_widget import FileSelectorWidget
from .replay_thread import ReplayThread


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
        
        # Connect temporal analysis sync signal to charts - DISABLED for replay mode to avoid double loading and auto-scroll
        # self.temporal_analysis.data_sync_signal.connect(self.charts.update_data)
        
        # Connect temporal analysis slider directly to charts for cursor control - DISABLED for replay mode
        # self.temporal_analysis.range_slider.valueChanged.connect(self.update_charts_cursor_direct)
        
        # Définir stop_replay avant de l'utiliser dans init_ui
        self.stop_replay = self.stop_replay_method
        
        self.init_ui()
    
    def stop_replay_method(self):
        """Stop the current replay and clear all data."""
        # Arrêter le replay thread s'il existe
        if self.replay_thread and self.replay_thread.isRunning():
            self.replay_thread.stop()
            self.replay_thread.wait(1000)  # Attendre max 1 seconde
        
        # Effacer toutes les données
        self.reset_all_data()
        
        # Réinitialiser l'interface
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Réinitialiser le curseur au début
        if hasattr(self.temporal_analysis, 'range_slider'):
            self.temporal_analysis.range_slider.setValue(0)
    
    def stop_replay(self):
        """Stop the current replay."""
        return self.stop_replay_method()
    
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
        layout.setSpacing(10)  # Réduit l'espacement
        layout.setContentsMargins(10, 10, 10, 10)  # Réduit les marges
        
        # File selection group
        file_group = QGroupBox("📁 CSV File")
        file_group.setMaximumHeight(250)  # 250px pour une visibilité maximale
        file_layout = QVBoxLayout()
        file_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create file selector widget
        self.file_selector = FileSelectorWidget()
        self.file_selector.file_selected.connect(self.on_file_selected)
        
        file_layout.addWidget(self.file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        self.play_btn = QPushButton("▶ Start")
        self.play_btn.clicked.connect(self.start_replay)
        self.play_btn.setFixedHeight(35)  # Hauteur fixe
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
            }
        """)
        button_layout.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.stop_replay)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setFixedHeight(35)  # Hauteur fixe comme le play
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
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
        
        # G-Forces row
        data_layout.addWidget(QLabel("G-Lat:"), 2, 0)
        self.g_lat_label = QLabel("--g")
        self.g_lat_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.g_lat_label.setStyleSheet("color: #8b5cf6; background: #f3f4f6; padding: 4px; border-radius: 4px; min-width: 80px;")
        data_layout.addWidget(self.g_lat_label, 2, 1)
        
        data_layout.addWidget(QLabel("G-Long:"), 2, 2)
        self.g_long_label = QLabel("--g")
        self.g_long_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.g_long_label.setStyleSheet("color: #8b5cf6; background: #f3f4f6; padding: 4px; border-radius: 4px; min-width: 80px;")
        data_layout.addWidget(self.g_long_label, 2, 3)
        
        data_layout.addWidget(QLabel("G-Vert:"), 2, 4)
        self.g_vert_label = QLabel("--g")
        self.g_vert_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.g_vert_label.setStyleSheet("color: #8b5cf6; background: #f3f4f6; padding: 4px; border-radius: 4px; min-width: 80px;")
        data_layout.addWidget(self.g_vert_label, 2, 5)
        
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
        
        # Arrêter le replay précédent s'il existe
        if self.replay_thread and self.replay_thread.isRunning():
            self.replay_thread.stop()
            self.replay_thread.wait(1000)  # Attendre max 1 seconde
        
        # Clear existing data completely
        self.charts.clear_data()
        self.temporal_analysis.clear_data()
        self.manager.clear_history()  # Vider l'historique du manager
        
        # Réinitialiser le slider
        if hasattr(self.temporal_analysis, 'range_slider'):
            self.temporal_analysis.range_slider.setValue(0)
            self.temporal_analysis.range_slider.setMaximum(0)  # Sera mis à jour après chargement
        
        # Reset current data labels
        self.speed_label.setText("-- km/h")
        self.rpm_label.setText("--")
        self.throttle_label.setText("--%")
        self.temp_label.setText("--°C")
        self.g_lat_label.setText("--g")
        self.g_long_label.setText("--g")
        self.g_vert_label.setText("--g")
        
        # Clear log text
        self.log_text.clear()
        
        # Load all data from file for initial display (curves only, no cursor points)
        self.load_all_data_for_charts(self.current_file)
        
        # Créer le replay thread mais ne PAS le démarrer automatiquement
        self.replay_thread = ReplayThread(self.current_file)
        
        # Autozoom the telemetry charts
        self.charts.full_auto_zoom()
        # Connecter les signaux
        self.replay_thread.data_received.connect(self.on_data_received)
        self.replay_thread.error_occurred.connect(self.on_error)
        self.replay_thread.status_changed.connect(self.on_status_changed)
        self.replay_thread.finished.connect(self.on_replay_finished)
        
        # NE PAS démarrer le thread automatiquement - attendre le clic sur Play
        # MAINTENANT on démarre le thread car c'est la fonction start_replay appelée par le bouton Play
        self.replay_thread.start()
        
        # Mettre à jour les boutons pour l'état de lecture
        self.play_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def on_error(self, error_message):
        """Handle replay errors."""
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        # Write to log
        self.log_text.append(f"Error: {error_message}")
    
    def on_status_changed(self, status):
        """Handle status updates."""
        # Write to log
        self.log_text.append(f"Error: {error_message}")

    
    def on_replay_finished(self):
        """Handle replay completion."""
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        # Write to log
        self.log_text.append("Replay finished")
        # Force auto-zoom on all charts after replay is complete
        self.charts.full_auto_zoom()
    
    def load_all_data_for_charts(self, file_path):
        """Load all data from CSV file for initial chart display (curves only, no points)."""
        try:
            from .csv_parser import TelemetryData, parse_csv_line
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
            self.charts._loading_data = True  # Disable point updates during loading
            
            # Load all data into charts at once - filter invalid data
            valid_data = []
            for data in all_data:
                # Filter out data with invalid or missing values that could cause diagonals
                if (hasattr(data, 'time_ms') and data.time_ms is not None and
                    hasattr(data, 'speed') and data.speed is not None and
                    hasattr(data, 'rpm') and data.rpm is not None):
                    valid_data.append(data)
            
            # Load only valid data into charts
            for data in valid_data:
                self.charts.update_data(data)
            
            # Load all data into temporal analysis at once
            self.temporal_analysis._loading_data = True  # Disable cursor updates during loading
            for data in all_data:
                self.temporal_analysis.update_data(data)
            self.temporal_analysis._loading_data = False
            
            # Set slider to show all data
            if all_data:
                max_time = int(all_data[-1].time_ms / 1000.0)  # Convert to seconds
                self.temporal_analysis.range_slider.setMaximum(len(all_data) - 1)
                self.temporal_analysis.range_slider.setValue(0)  # Garder au début pour éviter le lag
            
            # Re-enable point updates
            self.charts._loading_data = False
            
        except Exception as e:
            print(f"Error loading data for charts: {e}")
            self.log_text.append(f"⚠️ Error loading data: {e}")
    
    def reset_all_data(self):
        """Reset all charts, statistics, and displays to initial state."""
        # Clear charts data
        self.charts.clear_data()
        
        # Clear temporal analysis data
        self.temporal_analysis.clear_data()
        
        # Réinitialiser le slider
        if hasattr(self.temporal_analysis, 'range_slider'):
            self.temporal_analysis.range_slider.setValue(0)
            self.temporal_analysis.range_slider.setMaximum(0)
        
        # Reset current data labels to default
        self.speed_label.setText("-- km/h")
        self.rpm_label.setText("--")
        self.throttle_label.setText("--%")
        self.temp_label.setText("--°C")
        self.g_lat_label.setText("--g")
        self.g_long_label.setText("--g")
        self.g_vert_label.setText("--g")
        
        # Reset statistics labels to default
        self.max_speed_label.setText("--")
        self.avg_speed_label.setText("--")
        self.max_rpm_label.setText("--")
        self.avg_temp_label.setText("--")
        self.data_count_label.setText("0")
        
        # Reset telemetry manager
        self.manager.reset_stats()
    
    def on_data_received(self, data_or_index):
        """Update GUI with received data during replay."""
        # Si c'est un entier (index), utiliser pour le curseur
        if isinstance(data_or_index, int):
            point_idx = data_or_index
            # Mettre à jour le curseur des graphiques
            self.update_charts_cursor_direct(point_idx)
            
            # Mettre à jour l'analyse temporelle
            if hasattr(self.temporal_analysis, 'all_data') and self.temporal_analysis.all_data:
                if point_idx < len(self.temporal_analysis.all_data):
                    # Mettre à jour les labels avec les données actuelles
                    data = self.temporal_analysis.all_data[point_idx]
                    if hasattr(data, "speed"):
                        self.speed_label.setText(f"{data.speed:.1f} km/h")
                        self.rpm_label.setText(f"{data.rpm:.0f}")
                        self.throttle_label.setText(f"{data.throttle:.0f} %")
                        self.temp_label.setText(f"{data.battery_temp:.1f} °C")
                        self.g_lat_label.setText(f"{data.g_force_lat:.2f} g")
                        self.g_long_label.setText(f"{data.g_force_long:.2f} g")
                        self.g_vert_label.setText(f"{data.g_force_vert:.2f} g")
                    
                    # Mettre à jour les composants d'analyse temporelle
                    self.temporal_analysis.update_all_components(point_idx)
        
        # Si c'est un objet TelemetryData, l'utiliser directement
        elif hasattr(data_or_index, "speed"):
            data = data_or_index
            self.speed_label.setText(f"{data.speed:.1f} km/h")
            self.rpm_label.setText(f"{data.rpm:.0f}")
            self.throttle_label.setText(f"{data.throttle:.0f}%")
            self.temp_label.setText(f"{data.battery_temp:.1f}°C")
            self.g_lat_label.setText(f"{data.g_force_lat:.2f}g")
            self.g_long_label.setText(f"{data.g_force_long:.2f}g")
            self.g_vert_label.setText(f"{data.g_force_vert:.2f}g")
        
        # Update statistics
        if self.replay_thread and hasattr(self.replay_thread, 'manager'):
            stats = self.replay_thread.manager.get_stats()
            if stats:
                self.max_speed_label.setText(f"{stats.get('max_speed', 0):.1f} km/h")
                self.avg_speed_label.setText(f"{stats.get('avg_speed', 0):.1f} km/h")
                self.max_rpm_label.setText(f"{stats.get('max_rpm', 0):.0f}")
                self.avg_temp_label.setText(f"{stats.get('avg_temp', 0):.1f} °C")
                self.data_count_label.setText(f"{stats.get('data_points', 0)} ")
    
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
        
        # Points are disabled - no cursor markers needed
        # Skip point creation to avoid visual clutter and performance issues
        
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
