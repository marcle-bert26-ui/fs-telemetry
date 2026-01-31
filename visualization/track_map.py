"""
Track Map Module
Displays GPS position on a circuit map with time slider.
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSlider, 
                             QLabel, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush, QColor
import pyqtgraph as pg
from collections import deque
from src.csv_parser import TelemetryData


class TrackMapWidget(QWidget):
    """
    Widget displaying vehicle position on track with time slider.
    """
    
    position_changed = pyqtSignal(object)  # Emits TelemetryData for selected time
    
    def __init__(self, max_points=1000):
        """Initialize track map widget."""
        super().__init__()
        self.max_points = max_points
        
        # Data storage
        self.time_data = deque(maxlen=max_points)
        self.lat_data = deque(maxlen=max_points)
        self.lon_data = deque(maxlen=max_points)
        self.alt_data = deque(maxlen=max_points)
        self.telemetry_data = deque(maxlen=max_points)  # Store full objects
        
        self.current_index = 0
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("🗺️ Track Map & Position Analysis")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a; margin: 10px;")
        layout.addWidget(title)
        
        # Map display
        self.map_plot = pg.PlotWidget(title="Vehicle Position")
        self.map_plot.setLabel('left', 'Latitude')
        self.map_plot.setLabel('bottom', 'Longitude')
        self.map_plot.showGrid(x=True, y=True, alpha=0.3)
        self.map_plot.setBackground('#f0f4f8')
        self.map_plot.setMinimumSize(600, 400)
        
        # Create track line
        self.track_line = self.map_plot.plot(pen=pg.mkPen('#1e40af', width=3), name='Track')
        
        # Create current position marker
        self.position_marker = self.map_plot.plot(
            pen=None, 
            symbol='o', 
            symbolBrush='#ef4444', 
            symbolSize=15,
            name='Current Position'
        )
        
        # Create trail
        self.trail_line = self.map_plot.plot(pen=pg.mkPen('#3b82f6', width=1, alpha=0.5), name='Trail')
        
        layout.addWidget(self.map_plot)
        
        # Time slider and info
        slider_group = QGroupBox("Time Control")
        slider_layout = QVBoxLayout()
        
        # Time slider
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(0)
        self.time_slider.setValue(0)
        self.time_slider.valueChanged.connect(self.on_time_changed)
        
        # Time display
        self.time_label = QLabel("Time: 0.0s")
        self.time_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.time_label.setStyleSheet("color: #1e3a8a; padding: 5px;")
        
        # Position info
        self.position_info = QLabel("Position: --")
        self.position_info.setFont(QFont("Arial", 10))
        self.position_info.setStyleSheet("color: #6b7280; padding: 5px;")
        
        slider_layout.addWidget(QLabel("Select Time:"))
        slider_layout.addWidget(self.time_slider)
        slider_layout.addWidget(self.time_label)
        slider_layout.addWidget(self.position_info)
        
        slider_group.setLayout(slider_layout)
        layout.addWidget(slider_group)
        
        # Data info
        self.data_info = QLabel("No data loaded")
        self.data_info.setFont(QFont("Arial", 10))
        self.data_info.setStyleSheet("color: #6b7280; padding: 10px; background: #f3f4f6; border-radius: 5px;")
        layout.addWidget(self.data_info)
    
    def update_data(self, data: TelemetryData):
        """Update map with new telemetry data."""
        time_seconds = data.time_ms / 1000.0
        
        # Store data
        self.time_data.append(time_seconds)
        self.lat_data.append(data.gps_latitude)
        self.lon_data.append(data.gps_longitude)
        self.alt_data.append(data.gps_altitude)
        self.telemetry_data.append(data)
        
        # Update slider range
        self.time_slider.setMaximum(len(self.time_data) - 1)
        if self.current_index >= len(self.time_data):
            self.current_index = len(self.time_data) - 1
            self.time_slider.setValue(self.current_index)
        
        # Update display
        self.update_display()
        self.update_info()
    
    def on_time_changed(self, index):
        """Handle time slider change."""
        if 0 <= index < len(self.telemetry_data):
            self.current_index = index
            data = self.telemetry_data[index]
            
            # Update position marker
            self.position_marker.setData([data.gps_longitude], [data.gps_latitude])
            
            # Update trail (show path up to current position)
            trail_indices = list(range(index + 1))
            if trail_indices:
                trail_lons = [self.lon_data[i] for i in trail_indices]
                trail_lats = [self.lat_data[i] for i in trail_indices]
                self.trail_line.setData(trail_lons, trail_lats)
            
            # Update time label
            self.time_label.setText(f"Time: {self.time_data[index]:.1f}s")
            
            # Update position info
            pos_text = (f"Lat: {data.gps_latitude:.6f}°, "
                       f"Lon: {data.gps_longitude:.6f}°, "
                       f"Alt: {data.gps_altitude:.1f}m")
            self.position_info.setText(f"Position: {pos_text}")
            
            # Emit signal for other widgets
            self.position_changed.emit(data)
    
    def update_display(self):
        """Update the complete track display."""
        if len(self.lat_data) > 1:
            # Update track line
            self.track_line.setData(list(self.lon_data), list(self.lat_data))
            
            # Update trail to current position
            self.on_time_changed(self.current_index)
    
    def update_info(self):
        """Update data information display."""
        if self.telemetry_data:
            data_count = len(self.telemetry_data)
            if data_count > 0:
                first_data = self.telemetry_data[0]
                last_data = self.telemetry_data[-1]
                
                info_text = (f"Data Points: {data_count}\n"
                           f"Time Range: {self.time_data[0]:.1f}s - {self.time_data[-1]:.1f}s\n"
                           f"Lat Range: {min(self.lat_data):.6f}° - {max(self.lat_data):.6f}°\n"
                           f"Lon Range: {min(self.lon_data):.6f}° - {max(self.lon_data):.6f}°")
                
                self.data_info.setText(info_text)
    
    def clear_data(self):
        """Clear all track data."""
        self.time_data.clear()
        self.lat_data.clear()
        self.lon_data.clear()
        self.alt_data.clear()
        self.telemetry_data.clear()
        self.current_index = 0
        
        self.time_slider.setMaximum(0)
        self.time_slider.setValue(0)
        
        self.track_line.clear()
        self.trail_line.clear()
        self.position_marker.clear()
        
        self.time_label.setText("Time: 0.0s")
        self.position_info.setText("Position: --")
        self.data_info.setText("No data loaded")
