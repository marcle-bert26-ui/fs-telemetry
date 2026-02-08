"""
Telemetry Charts Module
Provides real-time and historical charts for Formula Student telemetry data.
"""

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QScrollArea, QPushButton
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
from csv_parser import TelemetryData


class TelemetryCharts(QWidget):
    """
    Widget containing multiple real-time telemetry charts.
    """
    
    def __init__(self, parent=None):
        """Initialize telemetry charts."""
        super().__init__(parent)
        
        # Data storage with deque for performance
        max_points = 1000
        self.time_data = deque(maxlen=max_points)
        self.speed_data = deque(maxlen=max_points)
        self.rpm_data = deque(maxlen=max_points)
        self.throttle_data = deque(maxlen=max_points)
        self.battery_temp_data = deque(maxlen=max_points)
        
        self.g_force_lat_data = deque(maxlen=max_points)
        self.g_force_long_data = deque(maxlen=max_points)
        self.g_force_vert_data = deque(maxlen=max_points)
        
        self.accel_x_data = deque(maxlen=max_points)
        self.accel_y_data = deque(maxlen=max_points)
        self.accel_z_data = deque(maxlen=max_points)
        
        self.tire_fl_data = deque(maxlen=max_points)
        self.tire_fr_data = deque(maxlen=max_points)
        self.tire_rl_data = deque(maxlen=max_points)
        self.tire_rr_data = deque(maxlen=max_points)
        
        # Display offset for oscilloscope effect
        self.display_offset = 0.0
        
        self.init_ui()
    
    def reset_auto_zoom(self):
        """Reset auto-zoom to show last 2 minutes (120 seconds) of data."""
        plots_to_reset = [
            (self.speed_rpm_plot, "Speed"),
            (self.throttle_temp_plot, "Throttle"), 
            (self.g_force_plot, "G-Forces"),
            (self.accel_plot, "Acceleration"),
            (self.tire_temp_plot, "Tire")
        ]
        
        for plot, plot_name in plots_to_reset:
            if plot is not None and self.time_data and len(self.time_data) > 0:
                # Get current time and calculate 2-minute window
                current_time = self.time_data[-1]
                window_start = max(0, current_time - 120)  # Last 2 minutes, but not negative
                window_end = current_time + 5  # Show 5 seconds ahead
                
                # Get view box and set range
                view_box = plot.getViewBox()
                
                # Apply appropriate Y range based on plot type
                if "Speed" in plot_name:
                    view_box.setRange(xRange=[window_start, window_end], yRange=[-10, 200], padding=0)
                elif "Throttle" in plot_name:
                    view_box.setRange(xRange=[window_start, window_end], yRange=[-10, 110], padding=0)
                elif "G-Forces" in plot_name:
                    view_box.setRange(xRange=[window_start, window_end], yRange=[-3, 3], padding=0)
                elif "Acceleration" in plot_name:
                    view_box.setRange(xRange=[window_start, window_end], yRange=[-10, 10], padding=0)
                elif "Tire" in plot_name:
                    view_box.setRange(xRange=[window_start, window_end], yRange=[-10, 100], padding=0)
                else:
                    view_box.setRange(xRange=[window_start, window_end], yRange=[-10, 10], padding=0)
                
                # Disable auto-range to maintain the custom view
                plot.enableAutoRange(axis='x', enable=False)
                plot.enableAutoRange(axis='y', enable=False)
                plot.update()
        
        # Also reset zoom for track map if available
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'temporal_analysis'):
            temporal_analysis = self.parent_widget.temporal_analysis
            if hasattr(temporal_analysis, 'track_map'):
                temporal_analysis.track_map.enableAutoRange()
                temporal_analysis.track_map.update()
        elif hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'track_map'):
            # Direct access if parent has track_map
            self.parent_widget.track_map.enableAutoRange()
            self.parent_widget.track_map.update()
    
    def full_auto_zoom(self):
        """Enable full auto-zoom for all plots (automatic view adjustment)."""
        plots_to_reset = [
            self.speed_rpm_plot,
            self.throttle_temp_plot, 
            self.g_force_plot,
            self.accel_plot,
            self.tire_temp_plot
        ]
        
        for plot in plots_to_reset:
            if plot is not None:
                # Enable auto-zoom for both axes
                plot.enableAutoRange(axis='x', enable=True)
                plot.enableAutoRange(axis='y', enable=True)
                # Force view update
                plot.getViewBox().enableAutoRange()
                plot.update()
        
        # Also auto-zoom the track map if available
        if hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'temporal_analysis'):
            temporal_analysis = self.parent_widget.temporal_analysis
            if hasattr(temporal_analysis, 'track_map'):
                temporal_analysis.track_map.enableAutoRange()
                temporal_analysis.track_map.update()
        elif hasattr(self, 'parent_widget') and self.parent_widget and hasattr(self.parent_widget, 'track_map'):
            # Direct access if parent has track_map
            self.parent_widget.track_map.enableAutoRange()
            self.parent_widget.track_map.update()
    
    def init_ui(self):
        """Initialize user interface with charts."""
        # Configure pyqtgraph for modern appearance
        pg.setConfigOptions(antialias=True, background='#1a1a1a', foreground='#ffffff', enableExperimental=True)
        
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
        
        # Create main widget to contain all charts
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Set minimum size for full screen utilization
        self.setMinimumSize(1000, 1800)
        # Set size policy for better resizing
        from PyQt5.QtWidgets import QSizePolicy
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        
        # Modern title with gradient effect
        title = QLabel("🏎️ REAL-TIME TELEMETRY")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                margin: 10px;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #7c3aed);
                border-radius: 12px;
                border: 2px solid #3730a3;
            }
        """)
        layout.addWidget(title)
        
        # Auto-zoom buttons - more visible
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push buttons to the right
        
        # 2 Minutes button
        self.two_min_btn = QPushButton("🔄 2 MIN")
        self.two_min_btn.clicked.connect(self.reset_auto_zoom)
        self.two_min_btn.setFixedSize(100, 35)  # Fixed size for better visibility
        self.two_min_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4ecdc4, stop:1 #45b7b0);
                color: #1a1a1a;
                border: 2px solid #3ca39c;
                padding: 8px 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #45b7b0, stop:1 #3ca39c);
                border: 2px solid #2d8680;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3ca39c, stop:1 #2d8680);
                border: 2px solid #1e635e;
            }
        """)
        button_layout.addWidget(self.two_min_btn)
        
        # Auto-Zoom button
        self.auto_zoom_btn = QPushButton("🎯 AUTO")
        self.auto_zoom_btn.clicked.connect(self.full_auto_zoom)
        self.auto_zoom_btn.setFixedSize(100, 35)  # Fixed size for better visibility
        self.auto_zoom_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #7c3aed);
                color: #ffffff;
                border: 2px solid #3730a3;
                padding: 8px 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1d4ed8, stop:1 #6d28d9);
                border: 2px solid #2d3748;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e40af, stop:1 #5b21b6);
                border: 2px solid #1e293b;
            }
        """)
        button_layout.addWidget(self.auto_zoom_btn)
        
        layout.addLayout(button_layout)
        
        # Create charts container with modern styling (no scroll)
        charts_container = QWidget()
        charts_container.setStyleSheet("""
            QWidget {
                background: #2d2d2d;
                border-radius: 12px;
                border: 1px solid #404040;
            }
        """)
        chart_layout = QGridLayout()  # Use grid layout for better space utilization
        chart_layout.setSpacing(15)
        chart_layout.setContentsMargins(15, 15, 15, 15)
        
        # Speed and RPM chart (row 0, col 0)
        self.speed_rpm_plot = self.create_plot("Speed & RPM", "Time (s)", ["Speed (km/h)", "RPM/100"])
        chart_layout.addWidget(self.speed_rpm_plot, 0, 0)
        
        # Throttle and Battery Temperature chart (row 0, col 1)
        self.throttle_temp_plot = self.create_plot("Throttle & Battery Temp", "Time (s)", ["Throttle (%)", "Temp (°C)"])
        chart_layout.addWidget(self.throttle_temp_plot, 0, 1)
        
        # G-Forces chart (row 1, col 0)
        self.g_force_plot = self.create_plot("G-Forces", "Time (s)", ["Lateral (g)", "Longitudinal (g)", "Vertical (g)"])
        chart_layout.addWidget(self.g_force_plot, 1, 0)
        
        # Acceleration chart (row 1, col 1)
        self.accel_plot = self.create_plot("Acceleration", "Time (s)", ["X (m/s²)", "Y (m/s²)", "Z (m/s²)"])
        chart_layout.addWidget(self.accel_plot, 1, 1)
        
        # Tire Temperatures chart (row 2, span 2 columns)
        self.tire_temp_plot = self.create_plot("Tire Temperatures", "Time (s)", ["FL (°C)", "FR (°C)", "RL (°C)", "RR (°C)"])
        chart_layout.addWidget(self.tire_temp_plot, 2, 0, 1, 2)
        
        charts_container.setLayout(chart_layout)
        layout.addWidget(charts_container)
        
        # Set the main widget as the scroll area's widget
        main_scroll.setWidget(main_widget)
        
        # Add scroll area to the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_scroll)
    
    def create_plot(self, title, x_label, y_labels):
        """Create a plot widget with modern configuration."""
        plot_widget = pg.PlotWidget(title=title)
        
        # Modern dark theme configuration
        plot_widget.setLabel('left', y_labels[0], units='', **{'font-size': '12pt', 'color': '#ffffff', 'font-family': 'Segoe UI'})
        plot_widget.setLabel('bottom', x_label, units='', **{'font-size': '12pt', 'color': '#ffffff', 'font-family': 'Segoe UI'})
        
        # Modern grid with better visibility
        plot_widget.showGrid(x=True, y=True, alpha=0.3)
        plot_widget.setBackground('#2d2d2d')
        
        # Modern styling for the plot area
        plot_widget.getViewBox().setContentsMargins(15, 15, 15, 15)
        
        # Set minimum size for better visibility (larger for grid layout)
        plot_widget.setMinimumSize(450, 250)
        
        # Modern legend with better styling
        legend = plot_widget.addLegend()
        legend.setPos(0.98, 0.98)
        # Set legend style using setLabel instead of setStyle for compatibility
        legend.setLabelTextColor('#ffffff')
        
        # Modern color palette with better contrast
        colors = ['#00ff88', '#ff6b6b', '#4ecdc4', '#ffe66d', '#a8e6cf', '#ff8cc8']
        legend_names = {
            "Speed (km/h)": "⚡ Speed",
            "RPM/100": "🔄 RPM/100", 
            "Throttle (%)": "🎯 Throttle",
            "Temp (°C)": "🌡️ Battery",
            "Lateral (g)": "↔️ Lateral G",
            "Longitudinal (g)": "↕️ Long. G", 
            "Vertical (g)": "⬆️ Vert. G",
            "X (m/s²)": "➡️ Accel X",
            "Y (m/s²)": "⬅️ Accel Y",
            "Z (m/s²)": "⬆️ Accel Z",
            "FL (°C)": "🛞 Front L",
            "FR (°C)": "🛞 Front R", 
            "RL (°C)": "🛞 Rear L",
            "RR (°C)": "🛞 Rear R"
        }
        
        curves = []  # Initialize curves list
        current_points = []  # Store current points separately
        
        for i, y_label in enumerate(y_labels):
            color = colors[i % len(colors)]
            legend_name = legend_names.get(y_label, y_label)
            try:
                # Modern curve with glow effect - initialize with empty data to avoid (0,0) points
                curve = plot_widget.plot(
                    pen=pg.mkPen(
                        color=color, 
                        width=3.0,
                        style=Qt.SolidLine,
                        antialias=True
                    ), 
                    name=legend_name
                )
                # Initialize with empty data to prevent automatic (0,0) points
                curve.setData([], [])
            except Exception as e:
                print(f"! Error creating curve: {e}")
                curve = plot_widget.plot(pen={'color': color, 'width': 3}, name=legend_name)
                # Initialize with empty data to prevent automatic (0,0) points
                curve.setData([], [])
            curves.append(curve)
            
            # Modern current point with glow effect - COMMENTED TO REMOVE PERMANENT POINTS
            # current_point = plot_widget.plot(
            #     pen=None, 
            #     symbol='o', 
            #     symbolBrush=color, 
            #     symbolSize=12, 
            #     symbolPen=pg.mkPen(color='white', width=2),
            #     name=f'Current {legend_name}'
            # )
            # current_points.append(current_point)
            
            # Create empty placeholder for current points (will be used by cursor)
            current_points.append(None)
        
        # Store curves and current points with plot for later updates
        plot_widget.curves = curves
        plot_widget.current_points = current_points  # Store all current points
        plot_widget.y_labels = y_labels
        
        return plot_widget
    
    def update_data(self, data: TelemetryData):
        """Update all charts with new telemetry data."""
        if not isinstance(data, TelemetryData):
            return
        
        # Validate data to prevent None values that cause diagonals
        if (data.time_ms is None or data.speed is None or data.rpm is None or
            data.throttle is None or data.battery_temp is None):
            return  # Skip invalid data points
        
        # Convert time to seconds for better display
        # Keep original time for data, but track display offset
        time_seconds = data.time_ms / 1000.0
        
        # Update data storage with validated data
        self.time_data.append(time_seconds)
        self.speed_data.append(data.speed if data.speed is not None else 0)
        self.rpm_data.append((data.rpm / 100) if data.rpm is not None else 0)  # Scale RPM for better visualization
        self.throttle_data.append(data.throttle if data.throttle is not None else 0)
        self.battery_temp_data.append(data.battery_temp if data.battery_temp is not None else 0)
        
        self.g_force_lat_data.append(data.g_force_lat if data.g_force_lat is not None else 0)
        self.g_force_long_data.append(data.g_force_long if data.g_force_long is not None else 0)
        self.g_force_vert_data.append(data.g_force_vert if data.g_force_vert is not None else 0)
        
        self.accel_x_data.append(data.acceleration_x if data.acceleration_x is not None else 0)
        self.accel_y_data.append(data.acceleration_y if data.acceleration_y is not None else 0)
        self.accel_z_data.append(data.acceleration_z if data.acceleration_z is not None else 0)
        
        self.tire_fl_data.append(data.tire_temp_fl if data.tire_temp_fl is not None else 0)
        self.tire_fr_data.append(data.tire_temp_fr if data.tire_temp_fr is not None else 0)
        self.tire_rl_data.append(data.tire_temp_rl if data.tire_temp_rl is not None else 0)
        self.tire_rr_data.append(data.tire_temp_rr if data.tire_temp_rr is not None else 0)
        
        # Update plots
        self.update_plots()
    
    def update_plots(self):
        """Update all plot curves with current data."""
        if not self.time_data:
            return
        
        # Use original time data (no offset) - let the view handle the scrolling
        time_array = np.array(self.time_data)
        
        # Check if first time is > 0 to avoid diagonal lines from origin
        first_time = time_array[0] if len(time_array) > 0 else 0
        
        try:
            # Create valid data mask (exclude None and invalid values)
            valid_mask = np.array([t is not None for t in self.time_data])
            valid_time = time_array[valid_mask]
            
            # Update Speed & RPM plot with valid data only
            if len(self.speed_data) > 0:
                speed_array = np.array(self.speed_data)[valid_mask]
                self.speed_rpm_plot.curves[0].setData(valid_time, speed_array)
            if len(self.rpm_data) > 0:
                rpm_array = np.array(self.rpm_data)[valid_mask]
                self.speed_rpm_plot.curves[1].setData(valid_time, rpm_array)
            
            # Update Throttle & Battery Temperature plot
            if len(self.throttle_data) > 0:
                throttle_array = np.array(self.throttle_data)[valid_mask]
                self.throttle_temp_plot.curves[0].setData(valid_time, throttle_array)
            if len(self.battery_temp_data) > 0:
                temp_array = np.array(self.battery_temp_data)[valid_mask]
                self.throttle_temp_plot.curves[1].setData(valid_time, temp_array)
            
            # Update G-Forces plot
            if len(self.g_force_lat_data) > 0:
                g_lat_array = np.array(self.g_force_lat_data)[valid_mask]
                self.g_force_plot.curves[0].setData(valid_time, g_lat_array)
            if len(self.g_force_long_data) > 0:
                g_long_array = np.array(self.g_force_long_data)[valid_mask]
                self.g_force_plot.curves[1].setData(valid_time, g_long_array)
            if len(self.g_force_vert_data) > 0:
                g_vert_array = np.array(self.g_force_vert_data)[valid_mask]
                self.g_force_plot.curves[2].setData(valid_time, g_vert_array)
            
            # Update Acceleration plot
            if len(self.accel_x_data) > 0:
                accel_x_array = np.array(self.accel_x_data)[valid_mask]
                self.accel_plot.curves[0].setData(valid_time, accel_x_array)
            if len(self.accel_y_data) > 0:
                accel_y_array = np.array(self.accel_y_data)[valid_mask]
                self.accel_plot.curves[1].setData(valid_time, accel_y_array)
            if len(self.accel_z_data) > 0:
                accel_z_array = np.array(self.accel_z_data)[valid_mask]
                self.accel_plot.curves[2].setData(valid_time, accel_z_array)
            
            # Update Tire Temperatures plot
            if len(self.tire_fl_data) > 0:
                tire_fl_array = np.array(self.tire_fl_data)[valid_mask]
                self.tire_temp_plot.curves[0].setData(valid_time, tire_fl_array)
            if len(self.tire_fr_data) > 0:
                tire_fr_array = np.array(self.tire_fr_data)[valid_mask]
                self.tire_temp_plot.curves[1].setData(valid_time, tire_fr_array)
            if len(self.tire_rl_data) > 0:
                tire_rl_array = np.array(self.tire_rl_data)[valid_mask]
                self.tire_temp_plot.curves[2].setData(valid_time, tire_rl_array)
            if len(self.tire_rr_data) > 0:
                tire_rr_array = np.array(self.tire_rr_data)[valid_mask]
                self.tire_temp_plot.curves[3].setData(valid_time, tire_rr_array)
                
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
                    curve.setData([], [])  # Ensure empty data to prevent (0,0) points
                
                # Clear current points - don't set to (0,0) to avoid diagonals
                if hasattr(plot, 'current_points'):
                    for current_point in plot.current_points:
                        if current_point is not None:  # Skip None points
                            current_point.clear()  # Clear instead of setting to (0,0)
                
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
    
    def quick_clear(self):
        """Quick clear for live mode - don't delete data, just reset displays."""
        # Don't clear data arrays - keep them for continuous display
        # Just reset display labels to default
        
        # This method now only resets displays without touching chart data
        # Data is preserved for continuous display across sessions
