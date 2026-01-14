"""
Temporal Analysis Widget
Combines track map and spider charts for time-based analysis.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QGroupBox, QLabel, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from visualization.track_map import TrackMapWidget
from visualization.spider_charts import GForcesSpiderWidget
from parsing.csv_parser import TelemetryData


class TemporalAnalysisWidget(QWidget):
    """
    Widget for temporal analysis combining track map and spider charts.
    """
    
    def __init__(self):
        """Initialize temporal analysis widget."""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("⏱️ Temporal Analysis & Position Tracking")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a; margin: 10px; background: #f0f9ff; padding: 10px; border-radius: 8px;")
        layout.addWidget(title)
        
        # Create tab widget for different analysis views
        tab_widget = QTabWidget()
        
        # Combined analysis tab
        combined_tab = QWidget()
        combined_layout = QVBoxLayout(combined_tab)
        
        # Create widgets
        self.track_map = TrackMapWidget()
        self.spider_chart = GForcesSpiderWidget()
        
        # Connect position change signal
        self.track_map.position_changed.connect(self.spider_chart.update_position)
        
        # Add widgets to combined layout
        combined_layout.addWidget(self.track_map)
        combined_layout.addWidget(self.spider_chart)
        
        tab_widget.addTab(combined_tab, "🗺️ Combined Analysis")
        
        # Track map only tab
        track_tab = QWidget()
        track_layout = QVBoxLayout(track_tab)
        track_layout.addWidget(self.track_map)
        tab_widget.addTab(track_tab, "📍 Track Map Only")
        
        # Spider charts only tab
        spider_tab = QWidget()
        spider_layout = QVBoxLayout(spider_tab)
        spider_layout.addWidget(self.spider_chart)
        tab_widget.addTab(spider_tab, "🕷️ G-Forces Only")
        
        # Data summary tab
        summary_tab = QWidget()
        summary_layout = QScrollArea()
        summary_layout.setWidgetResizable(True)
        
        summary_widget = QWidget()
        summary_content = QVBoxLayout(summary_widget)
        
        # Create data summary groups
        self.create_summary_groups(summary_content)
        
        summary_layout.setWidget(summary_widget)
        tab_widget.addTab(summary_layout, "📊 Data Summary")
        
        layout.addWidget(tab_widget)
    
    def create_summary_groups(self, layout):
        """Create summary data groups."""
        # Position summary
        position_group = QGroupBox("Position Summary")
        position_layout = QGridLayout()
        
        self.current_time_label = QLabel("--")
        self.current_lat_label = QLabel("--")
        self.current_lon_label = QLabel("--")
        self.current_alt_label = QLabel("--")
        self.current_speed_label = QLabel("--")
        
        position_layout.addWidget(QLabel("Current Time:"), 0, 0)
        position_layout.addWidget(self.current_time_label, 0, 1)
        position_layout.addWidget(QLabel("Latitude:"), 0, 2)
        position_layout.addWidget(self.current_lat_label, 0, 3)
        position_layout.addWidget(QLabel("Longitude:"), 1, 0)
        position_layout.addWidget(self.current_lon_label, 1, 1)
        position_layout.addWidget(QLabel("Altitude:"), 1, 2)
        position_layout.addWidget(self.current_alt_label, 1, 3)
        position_layout.addWidget(QLabel("Speed:"), 2, 0)
        position_layout.addWidget(self.current_speed_label, 2, 1)
        
        position_group.setLayout(position_layout)
        layout.addWidget(position_group)
        
        # G-forces summary
        gforces_group = QGroupBox("G-Forces Summary")
        gforces_layout = QGridLayout()
        
        self.current_lat_g_label = QLabel("--")
        self.current_long_g_label = QLabel("--")
        self.current_vert_g_label = QLabel("--")
        
        gforces_layout.addWidget(QLabel("Lateral G:"), 0, 0)
        gforces_layout.addWidget(self.current_lat_g_label, 0, 1)
        gforces_layout.addWidget(QLabel("Longitudinal G:"), 0, 2)
        gforces_layout.addWidget(self.current_long_g_label, 0, 3)
        gforces_layout.addWidget(QLabel("Vertical G:"), 0, 4)
        gforces_layout.addWidget(self.current_vert_g_label, 0, 5)
        
        gforces_group.setLayout(gforces_layout)
        layout.addWidget(gforces_group)
        
        # Vehicle status
        status_group = QGroupBox("Vehicle Status")
        status_layout = QGridLayout()
        
        self.current_rpm_label = QLabel("--")
        self.current_throttle_label = QLabel("--")
        self.current_temp_label = QLabel("--")
        
        status_layout.addWidget(QLabel("RPM:"), 0, 0)
        status_layout.addWidget(self.current_rpm_label, 0, 1)
        status_layout.addWidget(QLabel("Throttle:"), 0, 2)
        status_layout.addWidget(self.current_throttle_label, 0, 3)
        status_layout.addWidget(QLabel("Battery Temp:"), 0, 4)
        status_layout.addWidget(self.current_temp_label, 0, 5)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Acceleration data
        accel_group = QGroupBox("Acceleration Data")
        accel_layout = QGridLayout()
        
        self.current_accel_x_label = QLabel("--")
        self.current_accel_y_label = QLabel("--")
        self.current_accel_z_label = QLabel("--")
        
        accel_layout.addWidget(QLabel("Accel X:"), 0, 0)
        accel_layout.addWidget(self.current_accel_x_label, 0, 1)
        accel_layout.addWidget(QLabel("Accel Y:"), 0, 2)
        accel_layout.addWidget(self.current_accel_y_label, 0, 3)
        accel_layout.addWidget(QLabel("Accel Z:"), 0, 4)
        accel_layout.addWidget(self.current_accel_z_label, 0, 5)
        
        accel_group.setLayout(accel_layout)
        layout.addWidget(accel_group)
        
        # Tire temperatures
        tire_group = QGroupBox("Tire Temperatures")
        tire_layout = QGridLayout()
        
        self.tire_fl_label = QLabel("--")
        self.tire_fr_label = QLabel("--")
        self.tire_rl_label = QLabel("--")
        self.tire_rr_label = QLabel("--")
        
        tire_layout.addWidget(QLabel("Front Left:"), 0, 0)
        tire_layout.addWidget(self.tire_fl_label, 0, 1)
        tire_layout.addWidget(QLabel("Front Right:"), 0, 2)
        tire_layout.addWidget(self.tire_fr_label, 0, 3)
        tire_layout.addWidget(QLabel("Rear Left:"), 1, 0)
        tire_layout.addWidget(self.tire_rl_label, 1, 1)
        tire_layout.addWidget(QLabel("Rear Right:"), 1, 2)
        tire_layout.addWidget(self.tire_rr_label, 1, 3)
        
        tire_group.setLayout(tire_layout)
        layout.addWidget(tire_group)
    
    def update_data(self, data: TelemetryData):
        """Update all analysis widgets with new data."""
        # Update track map
        self.track_map.update_data(data)
        
        # Update spider chart
        self.spider_chart.update_data(data)
        
        # Update summary labels
        self.update_summary(data)
    
    def update_summary(self, data: TelemetryData):
        """Update summary display with current data."""
        # Position
        self.current_time_label.setText(f"{data.time_ms/1000:.1f}s")
        self.current_lat_label.setText(f"{data.gps_latitude:.6f}°")
        self.current_lon_label.setText(f"{data.gps_longitude:.6f}°")
        self.current_alt_label.setText(f"{data.gps_altitude:.1f}m")
        self.current_speed_label.setText(f"{data.speed:.1f} km/h")
        
        # G-forces
        self.current_lat_g_label.setText(f"{data.g_force_lat:.2f}g")
        self.current_long_g_label.setText(f"{data.g_force_long:.2f}g")
        self.current_vert_g_label.setText(f"{data.g_force_vert:.2f}g")
        
        # Vehicle status
        self.current_rpm_label.setText(f"{data.rpm}")
        self.current_throttle_label.setText(f"{data.throttle:.1f}%")
        self.current_temp_label.setText(f"{data.battery_temp:.1f}°C")
        
        # Acceleration
        self.current_accel_x_label.setText(f"{data.acceleration_x:.2f} m/s²")
        self.current_accel_y_label.setText(f"{data.acceleration_y:.2f} m/s²")
        self.current_accel_z_label.setText(f"{data.acceleration_z:.2f} m/s²")
        
        # Tire temperatures
        self.tire_fl_label.setText(f"{data.tire_temp_fl:.1f}°C")
        self.tire_fr_label.setText(f"{data.tire_temp_fr:.1f}°C")
        self.tire_rl_label.setText(f"{data.tire_temp_rl:.1f}°C")
        self.tire_rr_label.setText(f"{data.tire_temp_rr:.1f}°C")
    
    def clear_data(self):
        """Clear all data from analysis widgets."""
        self.track_map.clear_data()
        self.spider_chart.clear_data()
        
        # Reset summary labels
        self.current_time_label.setText("--")
        self.current_lat_label.setText("--")
        self.current_lon_label.setText("--")
        self.current_alt_label.setText("--")
        self.current_speed_label.setText("--")
        
        self.current_lat_g_label.setText("--")
        self.current_long_g_label.setText("--")
        self.current_vert_g_label.setText("--")
        
        self.current_rpm_label.setText("--")
        self.current_throttle_label.setText("--")
        self.current_temp_label.setText("--")
        
        self.current_accel_x_label.setText("--")
        self.current_accel_y_label.setText("--")
        self.current_accel_z_label.setText("--")
        
        self.tire_fl_label.setText("--")
        self.tire_fr_label.setText("--")
        self.tire_rl_label.setText("--")
        self.tire_rr_label.setText("--")
