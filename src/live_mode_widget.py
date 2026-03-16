"""
Live Mode Widget - Interface for real-time Arduino data acquisition.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QLabel, QPushButton, QTextEdit, QGroupBox, QScrollArea,
                           QLineEdit, QMessageBox, QSplitter, QSizePolicy, QSpinBox, QTabWidget)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QFont, QColor
import os

from serial_source import SerialSource
from csv_parser import parse_csv_line
from telemetry_manager import TelemetryManager
from csv_logger import CSVLogger
from telemetry_charts import TelemetryCharts
from temporal_analysis_widget import TemporalAnalysisWidget, CompactTrackMap
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
        self.track_map = CompactTrackMap()
        
        # Performance optimization settings
        self.update_counter = 0
        self.stats_update_counter = 0
        self.chart_batch_size = 5  # Update charts every 5 data points
        self.stats_batch_size = 30  # Update stats every 30 data points (much less frequent)
        self.is_stopping = False  # Flag to prevent crashes during stop
        self.is_live_mode = True   # Flag to identify live mode for optimizations
        
        # Add timer for chart updates to control frequency
        self.chart_timer = QTimer()
        self.chart_timer.timeout.connect(self.update_charts_from_buffer)
        self.chart_timer.start(200)  # Update charts every 200ms (5 FPS - even more stable)
        self.pending_data = None
        
        # Set parent references for track map access
        self.charts.parent_widget = self
        self.temporal_analysis.parent_widget = self
        
        # Enable batch mode for charts optimization
        self.charts._batch_mode = False  # Disable batch mode for real-time updates
        
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
        
        # Acceleration (plus petit)
        data_layout.addWidget(QLabel("Accel:"), 1, 0)
        self.accel_label = QLabel("-- m/s²")
        self.accel_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.accel_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.accel_label, 1, 1)
        
        # Injection (plus petit)
        data_layout.addWidget(QLabel("Inject:"), 1, 2)
        self.injection_label = QLabel("-- µs")
        self.injection_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.injection_label.setStyleSheet("color: #1e3a8a; background: #f0f9ff; padding: 6px; border-radius: 4px; min-width: 100px;")
        data_layout.addWidget(self.injection_label, 1, 3)
        
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
        
        stats_layout.addWidget(QLabel("Fuel Flow:"), 0, 0)
        self.max_speed_label = QLabel("-- L/h")
        self.max_speed_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.max_speed_label.setStyleSheet("color: #10b981; background: #f0fdf4; padding: 4px; border-radius: 3px;")
        stats_layout.addWidget(self.max_speed_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Fuel Total:"), 0, 2)
        self.avg_speed_label = QLabel("-- L")
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
        
        # Track map
        track_group = QGroupBox("🗺️ Track Map")
        track_layout = QVBoxLayout()
        track_layout.setContentsMargins(5, 5, 5, 5)
        track_layout.addWidget(self.track_map)
        track_group.setLayout(track_layout)
        left_layout.addWidget(track_group)
        
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
        
        # Complete reset for new acquisition
        self.charts.clear_data()
        self.temporal_analysis.clear_data()
        self.track_map.clear_data()
        
        # Reset displays only
        self.speed_label.setText("-- km/h")
        self.rpm_label.setText("--")
        self.accel_label.setText("-- m/s²")
        self.injection_label.setText("-- µs")
        self.max_speed_label.setText("-- L/h")
        self.avg_speed_label.setText("-- L")
        self.data_count_label.setText("0")
        
        # Reset performance counters
        self.update_counter = 0
        self.stats_update_counter = 0
        
        # Enable auto-zoom for live mode to see graphs progress
        self.charts.full_auto_zoom()
        
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
        """Stop data acquisition with improved crash protection."""
        # Set stopping flag to prevent new updates
        self.is_stopping = True
        
        try:
            # Stop thread safely
            if self.acquisition_thread:
                self.acquisition_thread.stop()
                # Wait for thread to finish with timeout
                if self.acquisition_thread.isRunning():
                    self.acquisition_thread.wait(2000)  # 2 second timeout
                    
                # Disconnect signals to prevent further updates
                try:
                    self.acquisition_thread.data_received.disconnect()
                    self.acquisition_thread.error_occurred.disconnect()
                    self.acquisition_thread.status_changed.disconnect()
                except Exception:
                    pass  # Ignore disconnect errors
                    
                self.acquisition_thread = None
        except Exception as e:
            # Log error but continue with cleanup
            if hasattr(self, 'log_text'):
                self.log_text.append(f"⚠️ Stop error: {str(e)[:50]}...")
        
        try:
            # Reset all displays to 0
            self.speed_label.setText("-- km/h")
            self.rpm_label.setText("--")
            self.accel_label.setText("-- m/s²")
            self.injection_label.setText("-- µs")
            self.max_speed_label.setText("-- L/h")
            self.avg_speed_label.setText("-- L")
            self.data_count_label.setText("0")
            
            # Reset performance counters
            self.update_counter = 0
            self.stats_update_counter = 0
            
        except Exception as e:
            # Log error but continue
            if hasattr(self, 'log_text'):
                self.log_text.append(f"⚠️ Cleanup error: {str(e)[:50]}...")
        
        # Reset UI state
        try:
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.port_input.setEnabled(True)
            self.baudrate_input.setEnabled(True)
            
            self.log_text.append("X Acquisition stopped")
        except Exception:
            pass  # Ignore UI errors
        
        # Reset stopping flag
        self.is_stopping = False
    
    def on_data_received(self, data):
        """Update GUI with received data - ultra-optimized for smooth performance."""
        # Skip updates if stopping to prevent crashes
        if self.is_stopping:
            return
            
        try:
            # Handle both dict and TelemetryData objects
            if hasattr(data, 'speed'):  # TelemetryData object
                # Always update labels (fast operation)
                self.speed_label.setText(f"{data.speed:.1f} km/h")
                self.rpm_label.setText(f"{data.rpm:.0f}")
                
                # Calculate and display fuel data
                acceleration = data.g_force_long * 9.81 if data.g_force_long is not None else 0
                self.accel_label.setText(f"{acceleration:.2f} m/s²")
                
                # Calculate injection
                injection_us = 800 + (data.rpm / 9500) * 6000 + data.throttle * 200 if data.rpm is not None and data.throttle is not None else 0
                self.injection_label.setText(f"{injection_us:.0f} µs")
                
                # Calculate fuel flow
                fuel_flow_lh = (injection_us / 1000000) * (data.rpm / 60) * 0.415 * 3600 / 1000 if data.rpm is not None else 0
                
                # Store data for timer-based chart updates
                self.pending_data = data
                
                # Update stats much less frequently
                self.stats_update_counter += 1
                if self.stats_update_counter >= self.stats_batch_size:
                    # Get current fuel volume from charts
                    current_fuel_volume = 0
                    if hasattr(self.charts, 'fuel_volume_data') and len(self.charts.fuel_volume_data) > 0:
                        current_fuel_volume = self.charts.fuel_volume_data[-1]
                    
                    # Update stats with correct data
                    self.max_speed_label.setText(f"{fuel_flow_lh:.2f} L/h")  # Current fuel flow
                    self.avg_speed_label.setText(f"{current_fuel_volume:.3f} L")  # Total fuel volume
                    self.data_count_label.setText(f"{len(self.manager.get_history())}")
                    self.stats_update_counter = 0
                    
            else:  # Dict object (backward compatibility)
                self.speed_label.setText(f"{data['speed']:.1f} km/h")
                self.rpm_label.setText(f"{data['rpm']:.0f}")
                self.throttle_label.setText(f"{data['throttle']:.0f}%")
                self.temp_label.setText(f"{data['battery_temp']:.1f}°C")
                
        except Exception as e:
            # Log error but don't crash
            if hasattr(self, 'log_text'):
                self.log_text.append(f"⚠️ Update error: {str(e)[:50]}...")
    
    def update_charts_from_buffer(self):
        """Update charts from pending data - called by timer for smooth updates."""
        if self.pending_data and not self.is_stopping:
            try:
                # Update charts immediately (highest priority)
                self.charts.update_data(self.pending_data)
                
                # Update track map at maximum speed (same as charts) - every timer call
                if hasattr(self, 'map_update_counter'):
                    self.map_update_counter += 1
                else:
                    self.map_update_counter = 1
                
                # Update every timer call to achieve 5 FPS (same as charts)
                if self.map_update_counter % 1 == 0:  # Every call = 5 FPS
                    if hasattr(self, 'track_map') and self.track_map:
                        self.track_map.update_data(self.pending_data)
                    
            except Exception as e:
                # Ignore chart errors to prevent crashes, but log them
                if hasattr(self, 'log_text'):
                    self.log_text.append(f"⚠️ Chart update error: {str(e)[:30]}...")
    
    def on_error(self, error_msg):
        """Handle acquisition errors."""
        self.log_text.append(f"X Error: {error_msg}")
        self.stop_acquisition()
    
    def on_status_changed(self, status):
        """Update status log."""
        self.log_text.append(f"- {status}")
    
    def update_chart_cursors(self, data, point_idx):
        """Update cursor points on telemetry charts - optimized for live mode."""
        try:
            if hasattr(self, 'charts') and self.charts:
                # Check if charts have data
                if not hasattr(self.charts, 'time_data') or len(self.charts.time_data) == 0:
                    return
                
                # Skip cursor updates in live mode for better performance
                # Only update if explicitly requested or in replay mode
                if hasattr(self, 'is_live_mode') and self.is_live_mode:
                    return  # Skip cursor updates in live mode for smoothness
                
                # Update cursor points for each chart
                for plot in [self.charts.rpm_plot, self.charts.acceleration_plot, 
                           self.charts.injection_plot, self.charts.fuel_flow_lh_plot, 
                           self.charts.fuel_volume_plot]:
                    # Create current_points if they don't exist
                    if not hasattr(plot, 'current_points'):
                        plot.current_points = [None]
                    
                    if plot.current_points:
                        # Get current data value for this plot
                        time_ms = getattr(data, 'time_ms', 0) / 1000.0
                        
                        # Update based on plot type
                        if plot == self.charts.rpm_plot:
                            value = getattr(data, 'rpm', 0)
                        elif plot == self.charts.acceleration_plot:
                            value = getattr(data, 'g_force_long', 0) * 9.81
                        elif plot == self.charts.injection_plot:
                            rpm = getattr(data, 'rpm', 0)
                            throttle = getattr(data, 'throttle', 0)
                            value = 800 + (rpm / 9500) * 6000 + throttle * 200
                        elif plot == self.charts.fuel_flow_lh_plot:
                            rpm = getattr(data, 'rpm', 0)
                            throttle = getattr(data, 'throttle', 0)
                            injection_us = 800 + (rpm / 9500) * 6000 + throttle * 200
                            value = (injection_us / 1000000) * (rpm / 60) * 0.415 * 3600 / 1000
                        elif plot == self.charts.fuel_volume_plot:
                            # Calculate current volume directly from current data
                            rpm = getattr(data, 'rpm', 0)
                            throttle = getattr(data, 'throttle', 0)
                            injection_us = 800 + (rpm / 9500) * 6000 + throttle * 200
                            fuel_flow_lh = (injection_us / 1000000) * (rpm / 60) * 0.415 * 3600 / 1000
                            
                            # Use the latest cumulative volume if available, otherwise calculate
                            if len(self.charts.fuel_volume_data) > 0:
                                # Add current fuel flow to the last cumulative volume
                                last_volume = self.charts.fuel_volume_data[-1]
                                value = last_volume + fuel_flow_lh / 3600  # Convert L/h to L/s for this instant
                            else:
                                # Fallback to simple calculation
                                value = fuel_flow_lh * point_idx / 3600
                        else:
                            value = 0
                        
                        # Update cursor point
                        if hasattr(plot, 'curves') and len(plot.curves) > 0:
                            # Remove old cursor point if exists
                            if plot.current_points[0] is not None:
                                plot.current_points[0].clear()
                            
                            # Create new cursor point
                            import pyqtgraph as pg
                            color = plot.curves[0].opts['pen'].color().name()
                            cursor_point = plot.plot([time_ms], [value], 
                                                    pen=None, 
                                                    symbol='o', 
                                                    symbolBrush=color, 
                                                    symbolSize=8, 
                                                    symbolPen=pg.mkPen(color='white', width=2))
                            plot.current_points[0] = cursor_point
                            
        except Exception as e:
            # Silently ignore cursor errors to not break main functionality
            pass
