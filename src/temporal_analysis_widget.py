"""
Compact Temporal Analysis Widget - Smaller Track Map
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QGroupBox, QLabel, QGridLayout, QSlider, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import pyqtgraph as pg
import numpy as np

from spider_charts import GForcesSpiderWidget
from csv_parser import TelemetryData


class CompactTrackMap(QWidget):
    """Compact track map with smaller size."""
    
    position_changed = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.origin_lat = None
        self.origin_lon = None
        self.trail_points = []
        self.fixed_range = False  # Flag to track if range is fixed
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Compact title
        title = QLabel("🗺️ Track")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                padding: 1px;
                font-size: 12px;
                color: #3b82f6;
            }
        """)
        layout.addWidget(title)
        
        # Create compact plot widget
        self.plot = pg.PlotWidget()
        self.plot.setBackground('#1a1a1a')
        self.plot.setMinimumHeight(180)
        self.plot.setMaximumHeight(320)
        self.plot.setLabel('left', 'Y', units='m', size='8pt')
        self.plot.setLabel('bottom', 'X', units='m', size='8pt')
        self.plot.showGrid(x=True, y=True, alpha=0.2)
        
        # Style axes
        self.plot.getAxis('left').setPen('#4ecdc4')
        self.plot.getAxis('bottom').setPen('#4ecdc4')
        self.plot.getAxis('left').setTextPen('#4ecdc4')
        self.plot.getAxis('bottom').setTextPen('#4ecdc4')
        
        layout.addWidget(self.plot)
        
        # Create car position
        self.car_position = pg.ScatterPlotItem(
            size=15, brush=(255, 0, 0), pen=(255, 100, 100)
        )
        self.plot.addItem(self.car_position)
        
        # Create trail
        self.trail = pg.PlotDataItem(
            pen=pg.mkPen(color='#3b82f6', width=1),
            symbol='o', symbolSize=2, symbolBrush='#3b82f6'
        )
        self.plot.addItem(self.trail)
        
        # Set view range
        self.plot.setRange(xRange=[-10, 10], yRange=[-10, 10])
        
        # Compact info label
        self.info_label = QLabel("📍 (0, 0) m | 0 km/h")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 4px;
                font-family: monospace;
                font-size: 10px;
                color: #475569;
            }
        """)
        layout.addWidget(self.info_label)
    
    def update_data(self, data):
        """Update car position on track."""
        if not data:
            return

        if not (hasattr(data, 'gps_latitude') and hasattr(data, 'gps_longitude')):
            self.info_label.setText("📍 No GPS | -- km/h")
            self.position_changed.emit(data)
            return

        lat = data.gps_latitude
        lon = data.gps_longitude

        if self.origin_lat is None or self.origin_lon is None:
            self.origin_lat = lat
            self.origin_lon = lon

        meters_per_deg_lat = 111_320.0
        meters_per_deg_lon = 111_320.0 * float(np.cos(np.deg2rad(self.origin_lat)))

        x = (lon - self.origin_lon) * meters_per_deg_lon
        y = (lat - self.origin_lat) * meters_per_deg_lat

        self.car_position.setData([x], [y])

        self.trail_points.append((x, y))
        if len(self.trail_points) > 2000:
            self.trail_points = self.trail_points[-2000:]

        if len(self.trail_points) > 1:
            trail_x, trail_y = zip(*self.trail_points)
            self.trail.setData(trail_x, trail_y)

            min_x = min(trail_x)
            max_x = max(trail_x)
        speed = getattr(data, 'speed', None)
        if speed is None:
            self.info_label.setText(f"📍 ({x:.0f}, {y:.0f}) m | -- km/h")
        else:
            self.info_label.setText(f"📍 ({x:.0f}, {y:.0f}) m | {speed:.0f} km/h")
        
        # Emit signal
        self.position_changed.emit(data)
    
    def clear_data(self):
        """Clear track data."""
        self.car_position.setData([], [])
        self.trail.setData([], [])
        self.origin_lat = None
        self.origin_lon = None
        self.trail_points = []
        self.plot.setRange(xRange=[-10, 10], yRange=[-10, 10])
        self.info_label.setText("📍 No GPS | -- km/h")


class TemporalGraphs(QWidget):
    """Temporal graphs for telemetry data."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.time_data = []
        self.speed_data = []
        self.g_lat_data = []
        self.g_long_data = []
        self.g_vert_data = []
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Title
        title = QLabel("📈 Temporal Data")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #f0fdf4;
                border: 1px solid #22c55e;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
                font-weight: bold;
                color: #166534;
            }
        """)
        layout.addWidget(title)
        
        # Speed graph
        self.speed_plot = pg.PlotWidget()
        self.speed_plot.setBackground('#1a1a1a')
        self.speed_plot.setMinimumHeight(100)
        self.speed_plot.setMaximumHeight(120)
        self.speed_plot.setLabel('left', 'Speed', units='km/h', size='8pt')
        self.speed_plot.setLabel('bottom', 'Time', units='s', size='8pt')
        self.speed_plot.showGrid(x=True, y=True, alpha=0.2)
        self.speed_plot.getAxis('left').setPen('#22c55e')
        self.speed_plot.getAxis('bottom').setPen('#22c55e')
        self.speed_plot.getAxis('left').setTextPen('#22c55e')
        self.speed_plot.getAxis('bottom').setTextPen('#22c55e')
        self.speed_curve = self.speed_plot.plot(pen=pg.mkPen(color='#22c55e', width=2))
        layout.addWidget(self.speed_plot)
        
        # G-forces graph
        self.g_forces_plot = pg.PlotWidget()
        self.g_forces_plot.setBackground('#1a1a1a')
        self.g_forces_plot.setMinimumHeight(100)
        self.g_forces_plot.setMaximumHeight(120)
        self.g_forces_plot.setLabel('left', 'G-Forces', units='g', size='8pt')
        self.g_forces_plot.setLabel('bottom', 'Time', units='s', size='8pt')
        self.g_forces_plot.showGrid(x=True, y=True, alpha=0.2)
        self.g_forces_plot.getAxis('left').setPen('#f59e0b')
        self.g_forces_plot.getAxis('bottom').setPen('#f59e0b')
        self.g_forces_plot.getAxis('left').setTextPen('#f59e0b')
        self.g_forces_plot.getAxis('bottom').setTextPen('#f59e0b')
        self.g_lat_curve = self.g_forces_plot.plot(pen=pg.mkPen(color='#ef4444', width=1.5), name='Lat')
        self.g_long_curve = self.g_forces_plot.plot(pen=pg.mkPen(color='#3b82f6', width=1.5), name='Long')
        self.g_vert_curve = self.g_forces_plot.plot(pen=pg.mkPen(color='#22c55e', width=1.5), name='Vert')
        self.g_forces_plot.addLegend()
        layout.addWidget(self.g_forces_plot)
    
    def update_data(self, data_list, current_point_idx=None):
        """Update graphs with filtered data and highlight current point."""
        if not data_list:
            return
        
        # Clear previous data
        self.time_data.clear()
        self.speed_data.clear()
        self.g_lat_data.clear()
        self.g_long_data.clear()
        self.g_vert_data.clear()
        
        # Extract data from filtered list
        for i, data in enumerate(data_list):
            time_ms = getattr(data, 'time_ms', i * 100)  # Fallback time
            self.time_data.append(time_ms / 1000.0)  # Convert to seconds
            
            self.speed_data.append(getattr(data, 'speed', 0))
            self.g_lat_data.append(getattr(data, 'g_force_lat', 0))
            self.g_long_data.append(getattr(data, 'g_force_long', 0))
            self.g_vert_data.append(getattr(data, 'g_force_vert', 0))
        
        # Clear plots completely
        self.speed_plot.clear()
        self.g_forces_plot.clear()
        
        if self.time_data:
            # Re-create curves
            self.speed_curve = self.speed_plot.plot(pen=pg.mkPen(color='#22c55e', width=2))
            self.g_lat_curve = self.g_forces_plot.plot(pen=pg.mkPen(color='#ef4444', width=1.5), name='Lat')
            self.g_long_curve = self.g_forces_plot.plot(pen=pg.mkPen(color='#3b82f6', width=1.5), name='Long')
            self.g_vert_curve = self.g_forces_plot.plot(pen=pg.mkPen(color='#22c55e', width=1.5), name='Vert')
            
            # Set data
            self.speed_curve.setData(self.time_data, self.speed_data)
            self.g_lat_curve.setData(self.time_data, self.g_lat_data)
            self.g_long_curve.setData(self.time_data, self.g_long_data)
            self.g_vert_curve.setData(self.time_data, self.g_vert_data)
            
            # Add current point indicator if specified
            if current_point_idx is not None and 0 <= current_point_idx < len(self.time_data):
                current_time = self.time_data[current_point_idx]
                current_speed = self.speed_data[current_point_idx]
                current_g_lat = self.g_lat_data[current_point_idx]
                current_g_long = self.g_long_data[current_point_idx]
                current_g_vert = self.g_vert_data[current_point_idx]
                
                # Current point markers - larger and more visible (skip during loading)
                is_loading = getattr(self, '_loading_data', False)
                if not is_loading:
                    self.speed_plot.plot([current_time], [current_speed], pen=None, symbol='o', symbolSize=10, symbolBrush='red', symbolPen='darkred')
                    self.g_forces_plot.plot([current_time], [current_g_lat], pen=None, symbol='o', symbolSize=8, symbolBrush='red', symbolPen='darkred')
                    self.g_forces_plot.plot([current_time], [current_g_long], pen=None, symbol='o', symbolSize=8, symbolBrush='red', symbolPen='darkred')
                    self.g_forces_plot.plot([current_time], [current_g_vert], pen=None, symbol='o', symbolSize=8, symbolBrush='red', symbolPen='darkred')
            
            # Re-add legend
            self.g_forces_plot.addLegend()
    
    def clear_data(self):
        """Clear all data."""
        self.time_data.clear()
        self.speed_data.clear()
        self.g_lat_data.clear()
        self.g_long_data.clear()
        self.g_vert_data.clear()
        self.speed_curve.setData([], [])
        self.g_lat_curve.setData([], [])
        self.g_long_curve.setData([], [])
        self.g_vert_curve.setData([], [])


class CompactDataSelector(QWidget):
    """Compact data selection widget."""
    
    range_changed = pyqtSignal(int, int)
    
    def __init__(self, range_slider):
        super().__init__()
        self.data_count = 0
        self.range_slider = range_slider  # Store reference to global slider
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Compact title
        title = QLabel("📊 Data")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #fef3c7;
                border: 1px solid #f59e0b;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
                font-weight: bold;
                color: #92400e;
            }
        """)
        layout.addWidget(title)
        
        # Compact info
        self.info_label = QLabel("📈 100 points")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 4px;
                font-size: 10px;
                color: #475569;
            }
        """)
        layout.addWidget(self.info_label)
        
        # Compact buttons
        button_layout = QHBoxLayout()
        
        self.auto_btn = QPushButton("🔄 Auto")
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        self.auto_btn.clicked.connect(self.start_auto_replay)
        button_layout.addWidget(self.auto_btn)
        
        self.recent_btn = QPushButton("🕐 50")
        self.recent_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.recent_btn.clicked.connect(lambda: self.range_slider.setValue(max(0, self.range_slider.maximum() - min(49, self.range_slider.maximum()))))
        button_layout.addWidget(self.recent_btn)
        
        self.all_btn = QPushButton("📋 All")
        self.all_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.all_btn.clicked.connect(lambda: self.range_slider.setValue(self.range_slider.maximum()))
        button_layout.addWidget(self.all_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def on_range_changed(self, value):
        """Handle range change."""
        self.info_label.setText(f"📈 Temps {value}s / {self.range_slider.maximum()}s")
        self.range_changed.emit(0, value)
    
    def update_telemetry_charts(self, charts, point_idx):
        """Update existing TelemetryCharts with current point."""
        if not charts or not hasattr(charts, 'time_data') or not charts.time_data:
            return
        
        # Mapper le temps du curseur à l'index
        time_value = point_idx  # Le curseur donne un temps en secondes
        max_time = charts.time_data[-1]
        max_index = len(charts.time_data) - 1
        
        # Calculer l'index proportionnel
        if max_time > 0:
            # Mapper le temps à l'index : temps/max_time = index/max_index
            point_idx = int((time_value / max_time) * max_index)
            # Limiter entre 0 et max_index
            point_idx = max(0, min(point_idx, max_index))
        else:
            point_idx = 0
        
        if point_idx < len(charts.time_data):
            current_time = charts.time_data[point_idx]
            
            # Update Speed & RPM plot - use all data
            if hasattr(charts, 'speed_rpm_plot') and charts.speed_rpm_plot:
                if len(charts.speed_data) > 0 and point_idx < len(charts.speed_data):
                    # Create point if it doesn't exist
                    if charts.speed_rpm_plot.current_points[0] is None:
                        charts.speed_rpm_plot.current_points[0] = charts.speed_rpm_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#22c55e', symbolPen='darkred'
                        )
                    charts.speed_rpm_plot.current_points[0].setData([current_time], [charts.speed_data[point_idx]])
                if len(charts.rpm_data) > 0 and point_idx < len(charts.rpm_data):
                    if charts.speed_rpm_plot.current_points[1] is None:
                        charts.speed_rpm_plot.current_points[1] = charts.speed_rpm_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#f59e0b', symbolPen='darkred'
                        )
                    charts.speed_rpm_plot.current_points[1].setData([current_time], [charts.rpm_data[point_idx]])
            
            # Update Throttle & Battery Temperature plot - use all data
            if hasattr(charts, 'throttle_temp_plot') and charts.throttle_temp_plot:
                if len(charts.throttle_data) > 0 and point_idx < len(charts.throttle_data):
                    if charts.throttle_temp_plot.current_points[0] is None:
                        charts.throttle_temp_plot.current_points[0] = charts.throttle_temp_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#3b82f6', symbolPen='darkred'
                        )
                    charts.throttle_temp_plot.current_points[0].setData([current_time], [charts.throttle_data[point_idx]])
                if len(charts.battery_temp_data) > 0 and point_idx < len(charts.battery_temp_data):
                    if charts.throttle_temp_plot.current_points[1] is None:
                        charts.throttle_temp_plot.current_points[1] = charts.throttle_temp_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#ef4444', symbolPen='darkred'
                        )
                    charts.throttle_temp_plot.current_points[1].setData([current_time], [charts.battery_temp_data[point_idx]])
            
            # Update G-Forces plot - use all data
            if hasattr(charts, 'g_force_plot') and charts.g_force_plot:
                if len(charts.g_force_lat_data) > 0 and point_idx < len(charts.g_force_lat_data):
                    if charts.g_force_plot.current_points[0] is None:
                        charts.g_force_plot.current_points[0] = charts.g_force_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#ef4444', symbolPen='darkred'
                        )
                    charts.g_force_plot.current_points[0].setData([current_time], [charts.g_force_lat_data[point_idx]])
                if len(charts.g_force_long_data) > 0 and point_idx < len(charts.g_force_long_data):
                    if charts.g_force_plot.current_points[1] is None:
                        charts.g_force_plot.current_points[1] = charts.g_force_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#3b82f6', symbolPen='darkred'
                        )
                    charts.g_force_plot.current_points[1].setData([current_time], [charts.g_force_long_data[point_idx]])
                if len(charts.g_force_vert_data) > 0 and point_idx < len(charts.g_force_vert_data):
                    if charts.g_force_plot.current_points[2] is None:
                        charts.g_force_plot.current_points[2] = charts.g_force_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#22c55e', symbolPen='darkred'
                        )
                    charts.g_force_plot.current_points[2].setData([current_time], [charts.g_force_vert_data[point_idx]])
            
            # Update Acceleration plot - use all data
            if hasattr(charts, 'accel_plot') and charts.accel_plot:
                if len(charts.accel_x_data) > 0 and point_idx < len(charts.accel_x_data):
                    if charts.accel_plot.current_points[0] is None:
                        charts.accel_plot.current_points[0] = charts.accel_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#8b5cf6', symbolPen='darkred'
                        )
                    charts.accel_plot.current_points[0].setData([current_time], [charts.accel_x_data[point_idx]])
                if len(charts.accel_y_data) > 0 and point_idx < len(charts.accel_y_data):
                    if charts.accel_plot.current_points[1] is None:
                        charts.accel_plot.current_points[1] = charts.accel_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#14b8a6', symbolPen='darkred'
                        )
                    charts.accel_plot.current_points[1].setData([current_time], [charts.accel_y_data[point_idx]])
                if len(charts.accel_z_data) > 0 and point_idx < len(charts.accel_z_data):
                    if charts.accel_plot.current_points[2] is None:
                        charts.accel_plot.current_points[2] = charts.accel_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#f59e0b', symbolPen='darkred'
                        )
                    charts.accel_plot.current_points[2].setData([current_time], [charts.accel_z_data[point_idx]])
            
            # Update Tire Temperatures plot - use all data
            if hasattr(charts, 'tire_temp_plot') and charts.tire_temp_plot:
                if len(charts.tire_fl_data) > 0 and point_idx < len(charts.tire_fl_data):
                    if charts.tire_temp_plot.current_points[0] is None:
                        charts.tire_temp_plot.current_points[0] = charts.tire_temp_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#ef4444', symbolPen='darkred'
                        )
                    charts.tire_temp_plot.current_points[0].setData([current_time], [charts.tire_fl_data[point_idx]])
                if len(charts.tire_fr_data) > 0 and point_idx < len(charts.tire_fr_data):
                    if charts.tire_temp_plot.current_points[1] is None:
                        charts.tire_temp_plot.current_points[1] = charts.tire_temp_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#f59e0b', symbolPen='darkred'
                        )
                    charts.tire_temp_plot.current_points[1].setData([current_time], [charts.tire_fr_data[point_idx]])
                if len(charts.tire_rl_data) > 0 and point_idx < len(charts.tire_rl_data):
                    if charts.tire_temp_plot.current_points[2] is None:
                        charts.tire_temp_plot.current_points[2] = charts.tire_temp_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#3b82f6', symbolPen='darkred'
                        )
                    charts.tire_temp_plot.current_points[2].setData([current_time], [charts.tire_rl_data[point_idx]])
                if len(charts.tire_rr_data) > 0 and point_idx < len(charts.tire_rr_data):
                    if charts.tire_temp_plot.current_points[3] is None:
                        charts.tire_temp_plot.current_points[3] = charts.tire_temp_plot.plot(
                            pen=None, symbol='o', symbolSize=8, symbolBrush='#22c55e', symbolPen='darkred'
                        )
                    charts.tire_temp_plot.current_points[3].setData([current_time], [charts.tire_rr_data[point_idx]])
    
    def start_auto_replay(self):
        """Start automatic replay through all data points."""
        if hasattr(self, 'parent_widget') and self.parent_widget and self.parent_widget.all_data:
            # Start from beginning
            self.range_slider.setValue(0)
            self.auto_replay_index = 0
            self.auto_replay_active = True
            self.auto_replay_step()
    
    def auto_replay_step(self):
        """Execute one step of auto replay."""
        if not self.auto_replay_active or not hasattr(self, 'parent_widget') or not self.parent_widget:
            return
        
        if self.auto_replay_index >= len(self.parent_widget.all_data):
            self.auto_replay_active = False
            return
        
        # Update slider and all components
        self.range_slider.setValue(self.auto_replay_index)
        if self.parent_widget:
            self.parent_widget.update_all_components(self.auto_replay_index)
        
        self.auto_replay_index += 1
        
        # Schedule next step (50ms delay for smooth animation)
        if self.auto_replay_active:
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(50, self.auto_replay_step)
    
    def update_count(self, count):
        """Update total data count."""
        self.data_count = max(count, 1)
        # Update global slider directly
        self.range_slider.setMaximum(self.data_count - 1)


class TemporalAnalysisWidget(QWidget):
    """Compact temporal analysis widget with smaller components."""
    
    data_sync_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.data_count = 0
        self.all_data = []  # Store all data points
        
        # Créer le curseur d'abord
        self.range_slider = QSlider(Qt.Horizontal)
        self.range_slider.setMinimum(0)
        self.range_slider.setMaximum(0)
        self.range_slider.setValue(0)
        self.range_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #d1d5db;
                height: 8px;
                background: #f3f4f6;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3b82f6;
                border: 2px solid #1e40af;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Initialiser les widgets d'abord
        self.track_map = CompactTrackMap()
        self.spider_chart = GForcesSpiderWidget()
        self.temporal_graphs = TemporalGraphs()
        self.data_selector = CompactDataSelector(self.range_slider)
        self.data_selector.parent_widget = self  # Set reference to parent
        
        # Ajouter un affichage des données actuelles
        self.current_data_label = QLabel("📊 Données Actuelles")
        self.current_data_label.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 2px solid #64748b;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                color: #1e293b;
            }
        """)
        self.current_data_label.setWordWrap(True)
        
        # Titre principal
        title = QLabel("📊 Analyse Temporelle Complète")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                color: #166534;
            }
        """)
        layout.addWidget(title)
        
        # Layout principal - seulement la colonne gauche avec tous les widgets
        main_layout = QVBoxLayout()
        
        # Spider Chart (en haut)
        spider_group = QGroupBox("🕸️ Forces G")
        spider_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #f59e0b;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #d97706;
            }
        """)
        spider_layout = QVBoxLayout(spider_group)
        spider_layout.setContentsMargins(5, 15, 5, 5)
        spider_layout.addWidget(self.spider_chart)
        main_layout.addWidget(spider_group)
        
        # Temporal Graphs
        temporal_group = QGroupBox("📈 Données Temporelles")
        temporal_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #8b5cf6;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #6d28d9;
            }
        """)
        temporal_layout = QVBoxLayout(temporal_group)
        temporal_layout.setContentsMargins(5, 15, 5, 5)
        temporal_layout.addWidget(self.temporal_graphs)
        main_layout.addWidget(temporal_group)
        
        # Data Selector
        data_group = QGroupBox("⚙️ Contrôle des Données")
        data_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #22c55e;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #166534;
            }
        """)
        data_layout = QVBoxLayout(data_group)
        data_layout.setContentsMargins(5, 15, 5, 5)
        data_layout.addWidget(self.data_selector)
        main_layout.addWidget(data_group)
        
        # Track Map (en bas)
        track_group = QGroupBox("🗺️ Carte de Piste")
        track_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3b82f6;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #1e40af;
            }
        """)
        track_layout = QVBoxLayout(track_group)
        track_layout.setContentsMargins(5, 15, 5, 5)
        track_layout.addWidget(self.track_map)
        main_layout.addWidget(track_group)
        
        main_layout.addStretch()  # Espace flexible en bas
        
        layout.addLayout(main_layout)
        layout.addWidget(self.current_data_label)  # Données actuelles
        layout.addWidget(self.range_slider)  # Curseur en bas
        
        # Connect signals
        self.track_map.position_changed.connect(self.spider_chart.update_position)
        self.range_slider.valueChanged.connect(self.update_all_components)
        self.data_selector.range_changed.connect(self.update_all_components)
        
        # Connecter le curseur directement au spider chart pour une mise à jour immédiate
        def update_spider_from_slider(value):
            if value < len(self.all_data):
                current_data = self.all_data[value]
                if hasattr(current_data, 'g_force_lat'):
                    self.spider_chart.update_data(current_data)
        
        self.range_slider.valueChanged.connect(update_spider_from_slider)
        
        # Connecter le curseur aux données actuelles
        def update_current_data_display(value):
            if value < len(self.all_data):
                data = self.all_data[value]
                text = f"""📊 Données Actuelles (Point {value + 1})
⏱️ Temps: {getattr(data, 'time_ms', 0) / 1000:.1f}s
🏎️ Vitesse: {getattr(data, 'speed', 0):.1f} km/h
🔧 RPM: {getattr(data, 'rpm', 0):.0f}
🚦 Accélérateur: {getattr(data, 'throttle', 0):.1f}%
🌡️ Température: {getattr(data, 'battery_temp', 0):.1f}°C
➡️ G-Latéral: {getattr(data, 'g_force_lat', 0):.3f}g
⬇️ G-Longitudinal: {getattr(data, 'g_force_long', 0):.3f}g
⬆️ G-Vertical: {getattr(data, 'g_force_vert', 0):.3f}g"""
                self.current_data_label.setText(text)
        
        self.range_slider.valueChanged.connect(update_current_data_display)
    
    def update_data(self, data):
        """Update all components."""
        if not data:
            return
        
        self.data_count += 1
        self.all_data.append(data)  # Store all data
        
        # Update slider maximum - FORCER l'utilisation des données des graphiques
        old_max = self.range_slider.maximum()
        
        # TOUJOURS vérifier les données des graphiques après chaque mise à jour
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'charts') and self.parent_widget.charts.time_data:
            max_points = len(self.parent_widget.charts.time_data)
            if max_points > 0:  # Seulement si on a des données
                self.range_slider.setMaximum(max_points - 1)
        else:
            # Fallback sur all_data seulement si pas de données dans les graphiques
            max_points = len(self.all_data)
            self.range_slider.setMaximum(max_points - 1)
        
        # Check if we're in loading mode (skip auto-follow and point updates)
        is_loading = getattr(self, '_loading_data', False)
        
        # Only set slider value if it was at the previous maximum (auto-follow mode)
        if not is_loading and (old_max == 0 or self.range_slider.value() == old_max):
            self.range_slider.setValue(max_points - 1)  # Show latest point
        
        # Update all components with latest point if auto-following (skip during loading)
        if not is_loading and self.range_slider.value() == max_points - 1:
            self.update_all_components(max_points - 1)
        
        # Update data selector
        self.data_selector.update_count(self.data_count)
        
        # Emit sync signal
        self.data_sync_signal.emit(data)
    
    def update_all_components(self, point_idx):
        """Update all components with data up to specified point."""
        # Utiliser les données des graphiques si disponibles, sinon self.all_data
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'charts') and self.parent_widget.charts.time_data:
            max_points = len(self.parent_widget.charts.time_data)
        else:
            max_points = len(self.all_data)
        
        if point_idx >= max_points:
            return
        
        # Update data selector display with current point info
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'charts') and self.parent_widget.charts.time_data:
            max_time = int(self.parent_widget.charts.time_data[-1])
            self.data_selector.info_label.setText(f"📈 Temps {point_idx}s / {max_time}s")
        else:
            self.data_selector.info_label.setText(f"📈 Point {point_idx + 1}/{max_points}")
        
        # Clear and update track map with all points up to current point
        self.track_map.clear_data()
        
        # Utiliser les mêmes données que le curseur
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'charts') and self.parent_widget.charts.time_data:
            # Utiliser les données des graphiques (synchronisées avec le curseur)
            for i in range(point_idx + 1):
                if i < len(self.parent_widget.charts.time_data):
                    # Créer un objet TelemetryData avec les données du point i
                    class TempPoint:
                        def __init__(self, time_ms, speed, rpm, throttle, battery_temp, g_force_lat, g_force_long, g_force_vert):
                            self.time_ms = time_ms
                            self.speed = speed
                            self.rpm = rpm
                            self.throttle = throttle
                            self.battery_temp = battery_temp
                            self.g_force_lat = g_force_lat
                            self.g_force_long = g_force_long
                            self.g_force_vert = g_force_vert
                    
                    # Récupérer les données du point i depuis les graphiques
                    time_ms = int(self.parent_widget.charts.time_data[i] * 1000) if i < len(self.parent_widget.charts.time_data) else 0
                    speed = self.parent_widget.charts.speed_data[i] if i < len(self.parent_widget.charts.speed_data) else 0
                    rpm = self.parent_widget.charts.rpm_data[i] * 100 if i < len(self.parent_widget.charts.rpm_data) else 0
                    throttle = self.parent_widget.charts.throttle_data[i] if i < len(self.parent_widget.charts.throttle_data) else 0
                    battery_temp = self.parent_widget.charts.battery_temp_data[i] if i < len(self.parent_widget.charts.battery_temp_data) else 0
                    g_force_lat = self.parent_widget.charts.g_force_lat_data[i] if i < len(self.parent_widget.charts.g_force_lat_data) else 0
                    g_force_long = self.parent_widget.charts.g_force_long_data[i] if i < len(self.parent_widget.charts.g_force_long_data) else 0
                    g_force_vert = self.parent_widget.charts.g_force_vert_data[i] if i < len(self.parent_widget.charts.g_force_vert_data) else 0
                    
                    temp_point = TempPoint(time_ms, speed, rpm, throttle, battery_temp, g_force_lat, g_force_long, g_force_vert)
                    self.track_map.update_data(temp_point)
        else:
            # Fallback sur all_data
            for i in range(point_idx + 1):
                self.track_map.update_data(self.all_data[i])
        
        # Update spider chart with current point
        current_data = self.all_data[point_idx]
        if hasattr(current_data, 'g_force_lat'):
            self.spider_chart.update_data(current_data)
        
        # Update temporal graphs with all data and current point index
        self.temporal_graphs.update_data(self.all_data, point_idx)
        
        # Update TelemetryCharts if available (from replay/live pages)
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'charts'):
            self.data_selector.update_telemetry_charts(self.parent_widget.charts, point_idx)
    
    def clear_data(self):
        """Clear all data."""
        self.track_map.clear_data()
        self.spider_chart.clear_data()
        self.temporal_graphs.clear_data()
        self.data_count = 0
        self.all_data.clear()  # Clear stored data
        self.range_slider.setValue(0)
