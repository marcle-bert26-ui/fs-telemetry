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
try:
    from csv_parser import TelemetryData
except ImportError:
    # Fallback for testing environment
    TelemetryData = None


class TelemetryCharts(QWidget):
    """
    Widget containing multiple real-time telemetry charts.
    """
    
    def __init__(self, parent=None):
        """Initialize telemetry charts."""
        super().__init__(parent)
        
        # Data storage with deque for performance - Only 5 fuel parameters
        max_points = 300  # Further reduced from 500 for better performance
        self.time_data = deque(maxlen=max_points)
        self.rpm_data = deque(maxlen=max_points)
        self.acceleration_data = deque(maxlen=max_points)
        self.injection_data = deque(maxlen=max_points)
        self.fuel_flow_lh_data = deque(maxlen=max_points)
        self.fuel_volume_data = deque(maxlen=max_points)
        
        # Display offset for oscilloscope effect
        self.display_offset = 0.0
        
        self.init_ui()
    
    def reset_auto_zoom(self):
        """Reset auto-zoom to show last 2 minutes (120 seconds) of data."""
        plots_to_reset = [
            (self.rpm_plot, "RPM"),
            (self.acceleration_plot, "Acceleration"), 
            (self.injection_plot, "Injection"),
            (self.fuel_flow_lh_plot, "Fuel Flow L/h"),
            (self.fuel_volume_plot, "Fuel Volume L")
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
            self.rpm_plot,
            self.acceleration_plot, 
            self.injection_plot,
            self.fuel_flow_lh_plot,
            self.fuel_volume_plot
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
        
        # Create 5 fuel parameter charts
        # RPM chart (row 0, col 0)
        self.rpm_plot = self.create_plot("Régime Moteur", "Time (s)", ["RPM (tr/min)"])
        chart_layout.addWidget(self.rpm_plot, 0, 0)
        
        # Acceleration chart (row 0, col 1)
        self.acceleration_plot = self.create_plot("Accélération", "Time (s)", ["Accélération (m/s²)"])
        chart_layout.addWidget(self.acceleration_plot, 0, 1)
        
        # Injection chart (row 1, span 2 columns)
        self.injection_plot = self.create_plot("Injection", "Time (s)", ["Injection (µs)"])
        chart_layout.addWidget(self.injection_plot, 1, 0, 1, 2)
        
        # Fuel Flow L/h chart (row 2, col 0)
        self.fuel_flow_lh_plot = self.create_plot("Débit Carburant", "Time (s)", ["Débit (L/h)"])
        chart_layout.addWidget(self.fuel_flow_lh_plot, 2, 0)
        
        # Fuel Volume L chart (row 2, col 1)
        self.fuel_volume_plot = self.create_plot("Volume Carburant", "Time (s)", ["Volume (L)"])
        chart_layout.addWidget(self.fuel_volume_plot, 2, 1)
        
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
                curves.append(curve)
                
                # Create current point marker for this curve
                current_point = plot_widget.plot([], [], 
                                                pen=None, 
                                                symbol='o', 
                                                symbolBrush=color, 
                                                symbolSize=8, 
                                                symbolPen=pg.mkPen(color='white', width=2),
                                                name=f'Current {legend_name}')
                current_points.append(current_point)
                
            except Exception as e:
                print(f"! Error creating curve: {e}")
                curves.append(None)
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
        # Only validate the fields we actually use for fuel calculations
        if (data.time_ms is None or data.rpm is None):
            return  # Skip invalid data points
        
        # Convert time to seconds for better display
        # Keep original time for data, but track display offset
        time_seconds = data.time_ms / 1000.0
        
        # Update data storage with validated data - Only 5 fuel parameters
        self.time_data.append(time_seconds)
        self.rpm_data.append(data.rpm if data.rpm is not None else 0)
        
        # Calculate acceleration from G-forces (simplified)
        acceleration = data.g_force_long * 9.81 if data.g_force_long is not None else 0
        self.acceleration_data.append(acceleration)
        
        # Simulate injection data based on RPM and throttle (µs)
        injection_us = 800 + (data.rpm / 9500) * 6000 + data.throttle * 200 if data.rpm is not None and data.throttle is not None else 0
        self.injection_data.append(injection_us)
        
        # Calculate fuel flow L/h based on injection (CORRECTED FORMULA)
        # 415 cc/min = 0.415 L/min = 0.415/60 L/s (débit continu de l'injecteur)
        # Moteur 4 temps : 1 injection tous les 2 tours
        if data.rpm is not None:
            # Volume par injection (L) = temps_injection * débit_injecteur
            volume_per_injection = (injection_us / 1000000) * (0.415 / 60)  # L
            
            # Nombre d'injections par seconde (4 temps)
            injections_per_second = (data.rpm / 60 / 2)  # injections/s
            
            # Volume par seconde = volume_par_injection * injections_par_seconde
            volume_per_second = volume_per_injection * injections_per_second
            
            # Conversion en L/h pour affichage
            fuel_flow_lh = volume_per_second * 3600
        else:
            fuel_flow_lh = 0
        self.fuel_flow_lh_data.append(fuel_flow_lh)
        
        # Calculate cumulative volume L (CORRECTED FORMULA)
        # Calculate fuel flow first with corrected formula
        rpm = getattr(data, 'rpm', 0)
        throttle = getattr(data, 'throttle', 0)
        injection_us = 800 + (rpm / 9500) * 6000 + throttle * 200 if rpm is not None and throttle is not None else 0
        
        # Initialize volume_added
        volume_added = 0
        
        # CORRECTED: Calculate volume per injection, not continuous flow
        if rpm is not None and rpm > 0:
            # Volume par injection (L) = temps_injection * débit_injecteur
            volume_per_injection = (injection_us / 1000000) * (0.415 / 60)  # L
            
            # Nombre d'injections par seconde (4 temps)
            injections_per_second = rpm / 60 / 2
            
            # Volume ajouté par seconde = volume_par_injection * injections_par_seconde
            volume_per_second = volume_per_injection * injections_per_second
            
            # Conversion en L/h pour cohérence avec fuel_flow_lh
            fuel_flow_lh = volume_per_second * 3600
            
            # Volume ajouté depuis le dernier point (1 seconde d'échantillonnage)
            volume_added = volume_per_second  # L par seconde
        else:
            fuel_flow_lh = 0
            volume_added = 0
        
        # Add current volume to last cumulative volume
        if len(self.fuel_volume_data) > 0:
            last_volume = self.fuel_volume_data[-1]
            volume_total = last_volume + volume_added
        else:
            # First point - start from 0
            volume_total = volume_added
        self.fuel_volume_data.append(volume_total)
        
        # Debug: print volume calculation
        # print(f"Fuel volume: {volume_total:.6f} L (added: {volume_added:.6f} L, fuel_flow: {fuel_flow_lh:.2f} L/h, rpm: {getattr(data, 'rpm', 0)}, injection_us: {injection_us:.0f}µs)")
        
        # Update plots only if not in batch mode (for live mode optimization)
        if not hasattr(self, '_batch_mode') or not self._batch_mode:
            self.update_plots()
    
    def update_plots(self):
        """Update all plot curves with current data - optimized for speed."""
        if not self.time_data:
            return
        
        # Use original time data (no offset) - let the view handle the scrolling
        time_array = np.array(self.time_data)
        
        try:
            # Debug: show that plots are being updated
            # print(f"Updating plots with {len(time_array)} points")
            
            # Update 5 fuel parameter plots - optimized for live mode
            # RPM plot
            if hasattr(self.rpm_plot, 'curves') and len(self.rpm_plot.curves) > 0 and len(self.rpm_data) > 0:
                rpm_array = np.array(self.rpm_data)
                self.rpm_plot.curves[0].setData(time_array, rpm_array)
                # self.rpm_plot.update()  # Skip forced refresh for performance
            
            # Acceleration plot
            if hasattr(self.acceleration_plot, 'curves') and len(self.acceleration_plot.curves) > 0 and len(self.acceleration_data) > 0:
                accel_array = np.array(self.acceleration_data)
                self.acceleration_plot.curves[0].setData(time_array, accel_array)
                # self.acceleration_plot.update()  # Skip forced refresh for performance
            
            # Injection plot
            if hasattr(self.injection_plot, 'curves') and len(self.injection_plot.curves) > 0 and len(self.injection_data) > 0:
                injection_array = np.array(self.injection_data)
                self.injection_plot.curves[0].setData(time_array, injection_array)
                # self.injection_plot.update()  # Skip forced refresh for performance
            
            # Fuel Flow L/h plot
            if hasattr(self.fuel_flow_lh_plot, 'curves') and len(self.fuel_flow_lh_plot.curves) > 0 and len(self.fuel_flow_lh_data) > 0:
                fuel_flow_array = np.array(self.fuel_flow_lh_data)
                self.fuel_flow_lh_plot.curves[0].setData(time_array, fuel_flow_array)
                # self.fuel_flow_lh_plot.update()  # Skip forced refresh for performance
            
            # Fuel Volume L plot
            if hasattr(self.fuel_volume_plot, 'curves') and len(self.fuel_volume_plot.curves) > 0 and len(self.fuel_volume_data) > 0:
                volume_array = np.array(self.fuel_volume_data)
                self.fuel_volume_plot.curves[0].setData(time_array, volume_array)
                # self.fuel_volume_plot.update()  # Skip forced refresh for performance
                
        except Exception as e:
            print(f"! Error updating plots: {e}")
        
     
    
    def clear_data(self):
        """Clear all chart data and reset points to origin."""
        # Clear all data arrays - Only 5 fuel parameters
        self.time_data.clear()
        self.rpm_data.clear()
        self.acceleration_data.clear()
        self.injection_data.clear()
        self.fuel_flow_lh_data.clear()
        self.fuel_volume_data.clear()
        
        # Clear and reset all plots
        plots_to_clear = [
            (self.rpm_plot, "RPM"),
            (self.acceleration_plot, "Acceleration"), 
            (self.injection_plot, "Injection"),
            (self.fuel_flow_lh_plot, "Fuel Flow L/h"),
            (self.fuel_volume_plot, "Fuel Volume L")
        ]
        
        for plot, plot_name in plots_to_clear:
            if plot is not None and hasattr(plot, 'curves'):
                # Clear all curves
                for curve in plot.curves:
                    if curve is not None:
                        curve.clear()
                        curve.setData([], [])  # Ensure empty data to prevent (0,0) points
                
                # Clear current points
                if hasattr(plot, 'current_points'):
                    for current_point in plot.current_points:
                        if current_point is not None:
                            current_point.clear()
                            current_point.setData([], [])
                
                # Reset plot view to show origin with appropriate ranges
                view_box = plot.getViewBox()
                if "RPM" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-500, 10000], padding=0)
                elif "Acceleration" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[-20, 20], padding=0)
                elif "Injection" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[0, 20000], padding=0)
                elif "Fuel Flow L/h" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[0, 50], padding=0)
                elif "Fuel Volume L" in plot_name:
                    view_box.setRange(xRange=[-1, 5], yRange=[0, 1], padding=0)  # Increased from 0-20 to 0-1 for better visibility
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
