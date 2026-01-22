"""
Telemetry Charts Module
Provides real-time and historical charts for Formula Student telemetry data.
"""

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QScrollArea
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg
# Configuration safe pour éviter les erreurs de version PyQt5
try:
    pg.setConfigOptions({
        'useOpenGL': False,
        'enableExperimental': False,
        'leftButtonPan': False
    })
except:
    # Fallback si setConfigOptions n'est pas disponible
    pass
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
        layout.setContentsMargins(10, 10, 10, 10)  # Ajouter des marges
        
        # Set minimum size for the entire charts widget
        self.setMinimumSize(800, 600)
        # Set size policy for better resizing
        from PyQt5.QtWidgets import QSizePolicy
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        
        # Title avec plus d'espace et meilleure position
        title = QLabel("📊 Real-time Telemetry Charts")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a; margin: 15px 10px 5px 10px; padding: 10px; background: white; border-radius: 8px; border: 1px solid #e5e7eb;")
        layout.addWidget(title)
        
        # Create scroll area for charts
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(False)  # Prevent resizing issues
        
        # Create charts container
        charts_container = QWidget()
        chart_layout = QVBoxLayout()  # Changé de QGridLayout à QVBoxLayout
        chart_layout.setSpacing(15)
        chart_layout.setContentsMargins(10, 10, 10, 10)  # Ajouter des marges intérieures
        
        # Speed and RPM chart
        self.speed_rpm_plot = self.create_plot("Speed & RPM", "Time (s)", ["Speed (km/h)", "RPM/100"])
        chart_layout.addWidget(self.speed_rpm_plot)
        
        # Throttle and Battery Temperature chart
        self.throttle_temp_plot = self.create_plot("Throttle & Battery Temp", "Time (s)", ["Throttle (%)", "Temp (°C)"])
        chart_layout.addWidget(self.throttle_temp_plot)
        
        # G-Forces chart
        self.g_force_plot = self.create_plot("G-Forces", "Time (s)", ["Lateral (g)", "Longitudinal (g)", "Vertical (g)"])
        chart_layout.addWidget(self.g_force_plot)
        
        # Acceleration chart
        self.accel_plot = self.create_plot("Acceleration", "Time (s)", ["X (m/s²)", "Y (m/s²)", "Z (m/s²)"])
        chart_layout.addWidget(self.accel_plot)
        
        # Tire Temperatures chart
        self.tire_temp_plot = self.create_plot("Tire Temperatures", "Time (s)", ["FL (°C)", "FR (°C)", "RL (°C)", "RR (°C)"])
        chart_layout.addWidget(self.tire_temp_plot)
        
        charts_container.setLayout(chart_layout)
        scroll_area.setWidget(charts_container)
        layout.addWidget(scroll_area)
    
    def create_plot(self, title, x_label, y_labels):
        """Create a plot widget with specified configuration."""
        plot_widget = pg.PlotWidget(title=title)
        
        # Configuration améliorée pour une meilleure apparence
        plot_widget.setLabel('left', y_labels[0], units='', **{'font-size': '11pt', 'color': '#374151'})
        plot_widget.setLabel('bottom', x_label, units='', **{'font-size': '11pt', 'color': '#374151'})
        plot_widget.showGrid(x=True, y=True, alpha=0.2)
        plot_widget.setBackground('#ffffff')
        
        # Configuration des bordures et marges
        plot_widget.getViewBox().setContentsMargins(10, 10, 10, 10)
        
        # Set minimum size pour une meilleure visibilité
        plot_widget.setMinimumSize(400, 300)
        
        # Améliorer la légende
        legend = plot_widget.addLegend()
        legend.setPos(0.98, 0.98)  # Position en haut à droite
        
        # Create curves for each y-axis label
        curves = []
        colors = ['#2563eb', '#dc2626', '#16a34a', '#ca8a04', '#7c3aed', '#db2777']
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
        
        current_points = []  # Store current points separately
        
        for i, y_label in enumerate(y_labels):
            color = colors[i % len(colors)]
            legend_name = legend_names.get(y_label, y_label)
            try:
                curve = plot_widget.plot(pen=pg.mkPen(color=color, width=2.5), name=legend_name)
            except Exception as e:
                print(f"! Error creating curve: {e}")
                curve = plot_widget.plot(pen={'color': color, 'width': 2.5}, name=legend_name)
            curves.append(curve)
            
            # Add red point for each curve
            current_point = plot_widget.plot(
                pen=None, 
                symbol='o', 
                symbolBrush='r', 
                symbolSize=10, 
                symbolPen='r',
                name=f'Current {legend_name}'
            )
            current_points.append(current_point)
        
        # Store curves and current points with plot for later updates
        plot_widget.curves = curves
        plot_widget.current_points = current_points  # Store all current points
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
        current_time = time_array[-1]  # Get the most recent time
        
        try:
            # Update Speed & RPM plot
            if len(self.speed_data) > 0:
                self.speed_rpm_plot.curves[0].setData(time_array, np.array(self.speed_data))
                # Update red point for speed
                self.speed_rpm_plot.current_points[0].setData([current_time], [self.speed_data[-1]])
            if len(self.rpm_data) > 0:
                self.speed_rpm_plot.curves[1].setData(time_array, np.array(self.rpm_data))
                # Update red point for RPM
                self.speed_rpm_plot.current_points[1].setData([current_time], [self.rpm_data[-1]])
            
            # Update Throttle & Battery Temperature plot
            if len(self.throttle_data) > 0:
                self.throttle_temp_plot.curves[0].setData(time_array, np.array(self.throttle_data))
                # Update red point for throttle
                self.throttle_temp_plot.current_points[0].setData([current_time], [self.throttle_data[-1]])
            if len(self.battery_temp_data) > 0:
                self.throttle_temp_plot.curves[1].setData(time_array, np.array(self.battery_temp_data))
                # Update red point for temperature
                self.throttle_temp_plot.current_points[1].setData([current_time], [self.battery_temp_data[-1]])
            
            # Update G-Forces plot
            if len(self.g_force_lat_data) > 0:
                self.g_force_plot.curves[0].setData(time_array, np.array(self.g_force_lat_data))
                # Update red point for lateral G
                self.g_force_plot.current_points[0].setData([current_time], [self.g_force_lat_data[-1]])
            if len(self.g_force_long_data) > 0:
                self.g_force_plot.curves[1].setData(time_array, np.array(self.g_force_long_data))
                # Update red point for longitudinal G
                self.g_force_plot.current_points[1].setData([current_time], [self.g_force_long_data[-1]])
            if len(self.g_force_vert_data) > 0:
                self.g_force_plot.curves[2].setData(time_array, np.array(self.g_force_vert_data))
                # Update red point for vertical G
                self.g_force_plot.current_points[2].setData([current_time], [self.g_force_vert_data[-1]])
            
            # Update Acceleration plot
            if len(self.accel_x_data) > 0:
                self.accel_plot.curves[0].setData(time_array, np.array(self.accel_x_data))
                # Update red point for accel X
                self.accel_plot.current_points[0].setData([current_time], [self.accel_x_data[-1]])
            if len(self.accel_y_data) > 0:
                self.accel_plot.curves[1].setData(time_array, np.array(self.accel_y_data))
                # Update red point for accel Y
                self.accel_plot.current_points[1].setData([current_time], [self.accel_y_data[-1]])
            if len(self.accel_z_data) > 0:
                self.accel_plot.curves[2].setData(time_array, np.array(self.accel_z_data))
                # Update red point for accel Z
                self.accel_plot.current_points[2].setData([current_time], [self.accel_z_data[-1]])
            
            # Update Tire Temperatures plot
            if len(self.tire_fl_data) > 0:
                self.tire_temp_plot.curves[0].setData(time_array, np.array(self.tire_fl_data))
                # Update red point for front left tire
                self.tire_temp_plot.current_points[0].setData([current_time], [self.tire_fl_data[-1]])
            if len(self.tire_fr_data) > 0:
                self.tire_temp_plot.curves[1].setData(time_array, np.array(self.tire_fr_data))
                # Update red point for front right tire
                self.tire_temp_plot.current_points[1].setData([current_time], [self.tire_fr_data[-1]])
            if len(self.tire_rl_data) > 0:
                self.tire_temp_plot.curves[2].setData(time_array, np.array(self.tire_rl_data))
                # Update red point for rear left tire
                self.tire_temp_plot.current_points[2].setData([current_time], [self.tire_rl_data[-1]])
            if len(self.tire_rr_data) > 0:
                self.tire_temp_plot.curves[3].setData(time_array, np.array(self.tire_rr_data))
                # Update red point for rear right tire
                self.tire_temp_plot.current_points[3].setData([current_time], [self.tire_rr_data[-1]])
                
        except Exception as e:
            print(f"! Error updating plots: {e}")
    
    def clear_data(self):
        """Clear all chart data and reset points to origin."""
        # Clear all data arrays
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
        
        # Clear and reset all plots
        plots_to_clear = [
            (self.speed_rpm_plot, "Speed & RPM"),
            (self.throttle_temp_plot, "Throttle & Battery Temp"), 
            (self.g_force_plot, "G-Forces"),
            (self.accel_plot, "Acceleration"),
            (self.tire_temp_plot, "Tire Temperatures")
        ]
        
        for plot, plot_name in plots_to_clear:
            if plot is not None:
                # Clear all curves
                for curve in plot.curves:
                    curve.clear()
                
                # Reset red points to origin (0,0)
                if hasattr(plot, 'current_points'):
                    for current_point in plot.current_points:
                        current_point.setData([0], [0])
                
                # Reset plot view to show origin with appropriate ranges
                view_box = plot.getViewBox()
                if "Speed" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-10, 200], padding=0)
                elif "Throttle" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-10, 110], padding=0)
                elif "G-Forces" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-3, 3], padding=0)
                elif "Acceleration" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-10, 10], padding=0)
                elif "Tire" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-10, 100], padding=0)
                else:
                    view_box.setRange(xRange=[-1, 5], yRange=[-10, 10], padding=0)
                
                # Force plot update
                plot.update()
