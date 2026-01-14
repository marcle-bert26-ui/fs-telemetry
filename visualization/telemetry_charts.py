"""
Telemetry Charts Module
Provides real-time and historical charts for Formula Student telemetry data.
"""

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QScrollArea
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from collections import deque
from parsing.csv_parser import TelemetryData


class TelemetryCharts(QWidget):
    """
    Widget containing multiple real-time telemetry charts.
    """
    
    def __init__(self, max_points=500):
        """Initialize telemetry charts."""
        super().__init__()
        self.max_points = max_points
        
        # Data storage for charts
        self.time_data = deque(maxlen=max_points)
        self.speed_data = deque(maxlen=max_points)
        self.rpm_data = deque(maxlen=max_points)
        self.throttle_data = deque(maxlen=max_points)
        self.battery_temp_data = deque(maxlen=max_points)
        
        # G-Force data
        self.g_force_lat_data = deque(maxlen=max_points)
        self.g_force_long_data = deque(maxlen=max_points)
        self.g_force_vert_data = deque(maxlen=max_points)
        
        # Acceleration data
        self.accel_x_data = deque(maxlen=max_points)
        self.accel_y_data = deque(maxlen=max_points)
        self.accel_z_data = deque(maxlen=max_points)
        
        # Tire temperature data
        self.tire_fl_data = deque(maxlen=max_points)
        self.tire_fr_data = deque(maxlen=max_points)
        self.tire_rl_data = deque(maxlen=max_points)
        self.tire_rr_data = deque(maxlen=max_points)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface with charts."""
        # Configure pyqtgraph for better appearance and stability
        pg.setConfigOptions(antialias=True, background='#f8f9fa', foreground='#1f2937', enableExperimental=True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Set minimum size for the entire charts widget
        self.setMinimumSize(800, 600)
        # Set size policy for better resizing
        from PyQt5.QtWidgets import QSizePolicy
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        
        # Title
        title = QLabel("📊 Real-time Telemetry Charts")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a; margin: 10px;")
        layout.addWidget(title)
        
        # Create scroll area for charts
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(False)  # Prevent resizing issues
        
        # Create charts container
        charts_container = QWidget()
        chart_layout = QGridLayout()
        chart_layout.setSpacing(15)
        
        # Speed and RPM chart
        self.speed_rpm_plot = self.create_plot("Speed & RPM", "Time (s)", ["Speed (km/h)", "RPM/100"])
        chart_layout.addWidget(self.speed_rpm_plot, 0, 0)
        
        # Throttle and Battery Temperature chart
        self.throttle_temp_plot = self.create_plot("Throttle & Battery Temp", "Time (s)", ["Throttle (%)", "Temp (°C)"])
        chart_layout.addWidget(self.throttle_temp_plot, 0, 1)
        
        # G-Forces chart
        self.g_force_plot = self.create_plot("G-Forces", "Time (s)", ["Lateral (g)", "Longitudinal (g)", "Vertical (g)"])
        chart_layout.addWidget(self.g_force_plot, 1, 0)
        
        # Acceleration chart
        self.accel_plot = self.create_plot("Acceleration", "Time (s)", ["X (m/s²)", "Y (m/s²)", "Z (m/s²)"])
        chart_layout.addWidget(self.accel_plot, 1, 1)
        
        # Tire Temperatures chart
        self.tire_temp_plot = self.create_plot("Tire Temperatures", "Time (s)", ["FL (°C)", "FR (°C)", "RL (°C)", "RR (°C)"])
        chart_layout.addWidget(self.tire_temp_plot, 2, 0, 1, 2)  # Span 2 columns
        
        charts_container.setLayout(chart_layout)
        scroll_area.setWidget(charts_container)
        layout.addWidget(scroll_area)
    
    def create_plot(self, title, x_label, y_labels):
        """Create a plot widget with specified configuration."""
        plot_widget = pg.PlotWidget(title=title)
        plot_widget.setLabel('left', y_labels[0])
        plot_widget.setLabel('bottom', x_label)
        plot_widget.showGrid(x=True, y=True, alpha=0.3)
        plot_widget.setBackground('#f8f9fa')
        
        # Set minimum size for better visibility
        plot_widget.setMinimumSize(500, 300)
        
        # Add legend
        plot_widget.addLegend()
        
        # Create curves for each y-axis label
        curves = []
        colors = ['#1e3a8a', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
        legend_names = {
            "Speed (km/h)": "Speed",
            "RPM/100": "RPM/100", 
            "Throttle (%)": "Throttle",
            "Temp (°C)": "Battery Temp",
            "Lateral (g)": "Lateral G",
            "Longitudinal (g)": "Longitudinal G", 
            "Vertical (g)": "Vertical G",
            "X (m/s²)": "Accel X",
            "Y (m/s²)": "Accel Y",
            "Z (m/s²)": "Accel Z",
            "FL (°C)": "Front Left",
            "FR (°C)": "Front Right", 
            "RL (°C)": "Rear Left",
            "RR (°C)": "Rear Right"
        }
        
        for i, y_label in enumerate(y_labels):
            color = colors[i % len(colors)]
            legend_name = legend_names.get(y_label, y_label)
            try:
                curve = plot_widget.plot(pen=pg.mkPen(color=color, width=2), name=legend_name)
            except Exception as e:
                print(f"! Error creating curve: {e}")
                curve = plot_widget.plot(pen={'color': color, 'width': 2}, name=legend_name)
            curves.append(curve)
        
        # Store curves with plot for later updates
        plot_widget.curves = curves
        plot_widget.y_labels = y_labels
        
        return plot_widget
    
    def update_data(self, data: TelemetryData):
        """Update all charts with new telemetry data."""
        if not isinstance(data, TelemetryData):
            return
        
        # Convert time to seconds for better display
        time_seconds = data.time_ms / 1000.0
        
        # Update data storage
        self.time_data.append(time_seconds)
        self.speed_data.append(data.speed)
        self.rpm_data.append(data.rpm / 100)  # Scale RPM for better visualization
        self.throttle_data.append(data.throttle)
        self.battery_temp_data.append(data.battery_temp)
        
        self.g_force_lat_data.append(data.g_force_lat)
        self.g_force_long_data.append(data.g_force_long)
        self.g_force_vert_data.append(data.g_force_vert)
        
        self.accel_x_data.append(data.acceleration_x)
        self.accel_y_data.append(data.acceleration_y)
        self.accel_z_data.append(data.acceleration_z)
        
        self.tire_fl_data.append(data.tire_temp_fl)
        self.tire_fr_data.append(data.tire_temp_fr)
        self.tire_rl_data.append(data.tire_temp_rl)
        self.tire_rr_data.append(data.tire_temp_rr)
        
        # Update plots
        self.update_plots()
    
    def update_plots(self):
        """Update all plot curves with current data."""
        if not self.time_data:
            return
        
        time_array = np.array(self.time_data)
        
        try:
            # Update Speed & RPM plot
            if len(self.speed_data) > 0:
                self.speed_rpm_plot.curves[0].setData(time_array, np.array(self.speed_data))
            if len(self.rpm_data) > 0:
                self.speed_rpm_plot.curves[1].setData(time_array, np.array(self.rpm_data))
            
            # Update Throttle & Temperature plot
            if len(self.throttle_data) > 0:
                self.throttle_temp_plot.curves[0].setData(time_array, np.array(self.throttle_data))
            if len(self.battery_temp_data) > 0:
                self.throttle_temp_plot.curves[1].setData(time_array, np.array(self.battery_temp_data))
            
            # Update G-Forces plot
            if len(self.g_force_lat_data) > 0:
                self.g_force_plot.curves[0].setData(time_array, np.array(self.g_force_lat_data))
            if len(self.g_force_long_data) > 0:
                self.g_force_plot.curves[1].setData(time_array, np.array(self.g_force_long_data))
            if len(self.g_force_vert_data) > 0:
                self.g_force_plot.curves[2].setData(time_array, np.array(self.g_force_vert_data))
            
            # Update Acceleration plot
            if len(self.accel_x_data) > 0:
                self.accel_plot.curves[0].setData(time_array, np.array(self.accel_x_data))
            if len(self.accel_y_data) > 0:
                self.accel_plot.curves[1].setData(time_array, np.array(self.accel_y_data))
            if len(self.accel_z_data) > 0:
                self.accel_plot.curves[2].setData(time_array, np.array(self.accel_z_data))
            
            # Update Tire Temperatures plot
            if len(self.tire_fl_data) > 0:
                self.tire_temp_plot.curves[0].setData(time_array, np.array(self.tire_fl_data))
            if len(self.tire_fr_data) > 0:
                self.tire_temp_plot.curves[1].setData(time_array, np.array(self.tire_fr_data))
            if len(self.tire_rl_data) > 0:
                self.tire_temp_plot.curves[2].setData(time_array, np.array(self.tire_rl_data))
            if len(self.tire_rr_data) > 0:
                self.tire_temp_plot.curves[3].setData(time_array, np.array(self.tire_rr_data))
                
        except Exception as e:
            print(f"! Error updating plots: {e}")
    
    def clear_data(self):
        """Clear all chart data."""
        self.time_data.clear()
        self.speed_data.clear()
        self.rpm_data.clear()
        self.throttle_data.clear()
        self.battery_temp_data.clear()
        self.g_force_lat_data.clear()
        self.g_force_long_data.clear()
        self.g_force_vert_data.clear()
        self.accel_x_data.clear()
        self.accel_y_data.clear()
        self.accel_z_data.clear()
        self.tire_fl_data.clear()
        self.tire_fr_data.clear()
        self.tire_rl_data.clear()
        self.tire_rr_data.clear()
        
        # Clear plots
        for plot in [self.speed_rpm_plot, self.throttle_temp_plot, self.g_force_plot, 
                     self.accel_plot, self.tire_temp_plot]:
            for curve in plot.curves:
                curve.clear()
