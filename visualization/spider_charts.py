"""
Spider Charts Module
Displays G-forces and other multi-dimensional data in radar/spider charts.
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QGridLayout, QScrollArea)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF
from collections import deque
from parsing.csv_parser import TelemetryData


class SpiderChartWidget(QWidget):
    """
    Custom spider/radar chart widget for multi-dimensional data visualization.
    """
    
    def __init__(self, title, labels, max_value=2.0, parent=None):
        """Initialize spider chart."""
        super().__init__(parent)
        self.title = title
        self.labels = labels
        self.max_value = max_value
        self.data = []
        self.colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
        
        self.setMinimumSize(400, 400)
    
    def add_data(self, values, label="Data"):
        """Add data point to chart."""
        self.data.append({
            'values': values,
            'label': label,
            'color': self.colors[len(self.data) % len(self.colors)]
        })
        self.update()
    
    def clear_data(self):
        """Clear all data."""
        self.data = []
        self.update()
    
    def paintEvent(self, event):
        """Paint the spider chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get drawing area with more padding
        rect = self.rect().adjusted(50, 80, -50, -50)  # Augmenté de 40,60,-40,-40 à 50,80,-50,-50
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2
        
        # Draw title with more space
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.setPen(QPen(QColor('#1e3a8a')))
        title_rect = self.rect().adjusted(0, 10, 0, 0)  # Ajouter de l'espace en haut
        painter.drawText(title_rect, Qt.AlignTop | Qt.AlignHCenter, self.title)
        
        # Calculate angles for each axis
        num_axes = len(self.labels)
        angles = []
        for i in range(num_axes):
            angle = -np.pi/2 + (2 * np.pi * i / num_axes)
            angles.append(angle)
        
        # Draw grid circles
        painter.setPen(QPen(QColor('#d1d5db'), 1))
        num_circles = 5
        for i in range(1, num_circles + 1):
            circle_radius = radius * i / num_circles
            painter.drawEllipse(center, circle_radius, circle_radius)
        
        # Draw axes
        painter.setPen(QPen(QColor('#9ca3af'), 1))
        for angle in angles:
            end_x = center.x() + radius * np.cos(angle)
            end_y = center.y() + radius * np.sin(angle)
            painter.drawLine(center, QPointF(end_x, end_y))
        
        # Draw labels with better positioning
        painter.setFont(QFont("Arial", 9))
        painter.setPen(QPen(QColor('#374151')))
        for i, (angle, label) in enumerate(zip(angles, self.labels)):
            label_radius = radius + 30  # Augmenté de 20 à 30 pour plus d'espace
            label_x = center.x() + label_radius * np.cos(angle)
            label_y = center.y() + label_radius * np.sin(angle)
            
            # Adjust text alignment based on position with more space
            if abs(label_x - center.x()) < 10:
                alignment = Qt.AlignHCenter | Qt.AlignVCenter
            elif label_x < center.x():
                alignment = Qt.AlignRight | Qt.AlignVCenter
            else:
                alignment = Qt.AlignLeft | Qt.AlignVCenter
            
            # Use larger rect for text with more padding
            painter.drawText(QRectF(label_x - 40, label_y - 15, 80, 30), alignment, label)
        
        # Draw data
        for data_point in self.data:
            self._draw_data_polygon(painter, center, radius, angles, data_point)
        
        # Draw scale values
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QPen(QColor('#6b7280')))
        for i in range(1, num_circles + 1):
            value = self.max_value * i / num_circles
            painter.drawText(QRectF(center.x() - 20, center.y() - radius * i / num_circles - 5, 40, 10), 
                          Qt.AlignRight | Qt.AlignVCenter, f"{value:.1f}")
    
    def _draw_data_polygon(self, painter, center, radius, angles, data_point):
        """Draw data polygon."""
        values = data_point['values']
        color = QColor(data_point['color'])
        
        # Calculate polygon points
        points = []
        for i, (angle, value) in enumerate(zip(angles, values)):
            if i < len(values):
                normalized_value = min(value / self.max_value, 1.0)
                x = center.x() + radius * normalized_value * np.cos(angle)
                y = center.y() + radius * normalized_value * np.sin(angle)
                points.append(QPointF(x, y))
        
        if len(points) >= 3:
            # Draw filled polygon
            polygon = QPolygonF(points)
            color.setAlphaF(0.3)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color, 2))
            painter.drawPolygon(polygon)
            
            # Draw points
            color.setAlphaF(1.0)
            painter.setBrush(QBrush(color))
            for point in points:
                painter.drawEllipse(point, 4, 4)


class GForcesSpiderWidget(QWidget):
    """
    Widget displaying G-forces in spider chart format.
    """
    
    # Signal pour émettre les données actuelles du spider chart
    current_data_changed = pyqtSignal('PyQt_PyObject')
    
    def __init__(self, max_points=100):
        """Initialize G-forces spider widget."""
        super().__init__()
        self.max_points = max_points
        
        # Data storage
        self.time_data = deque(maxlen=max_points)
        self.g_force_lat_data = deque(maxlen=max_points)
        self.g_force_long_data = deque(maxlen=max_points)
        self.g_force_vert_data = deque(maxlen=max_points)
        self.telemetry_data = deque(maxlen=max_points)
        
        self.current_index = -1
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("🕷️ G-Forces Spider Chart")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a8a; margin: 10px;")
        layout.addWidget(title)
        
        # Create charts widget directly (no scroll area)
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        
        # Current G-forces spider chart
        current_group = QGroupBox("Current G-Forces")
        current_layout = QVBoxLayout()
        
        self.current_spider = SpiderChartWidget(
            "Real-time G-Forces",
            ["Lateral G", "Longitudinal G", "Vertical G"],
            max_value=3.0
        )
        current_layout.addWidget(self.current_spider)
        
        # Current values display
        self.current_values = QLabel("Lateral: 0.0g | Longitudinal: 0.0g | Vertical: 0.0g")
        self.current_values.setFont(QFont("Arial", 10))
        self.current_values.setStyleSheet("color: #6b7280; padding: 5px; background: #f3f4f6; border-radius: 5px;")
        current_layout.addWidget(self.current_values)
        
        current_group.setLayout(current_layout)
        charts_layout.addWidget(current_group)
        
        # Comparison spider chart
        comparison_group = QGroupBox("G-Forces Comparison")
        comparison_layout = QVBoxLayout()
        
        self.comparison_spider = SpiderChartWidget(
            "G-Forces Comparison",
            ["Lateral G", "Longitudinal G", "Vertical G"],
            max_value=3.0
        )
        comparison_layout.addWidget(self.comparison_spider)
        
        # Comparison info
        self.comparison_info = QLabel("Select time points to compare G-forces")
        self.comparison_info.setFont(QFont("Arial", 10))
        self.comparison_info.setStyleSheet("color: #6b7280; padding: 5px; background: #f3f4f6; border-radius: 5px;")
        comparison_layout.addWidget(self.comparison_info)
        
        comparison_group.setLayout(comparison_layout)
        charts_layout.addWidget(comparison_group)
        
        # Statistics
        stats_group = QGroupBox("G-Forces Statistics")
        stats_layout = QGridLayout()
        
        self.max_lat_label = QLabel("--")
        self.max_long_label = QLabel("--")
        self.max_vert_label = QLabel("--")
        
        self.avg_lat_label = QLabel("--")
        self.avg_long_label = QLabel("--")
        self.avg_vert_label = QLabel("--")
        
        stats_layout.addWidget(QLabel("Max Lateral G:"), 0, 0)
        stats_layout.addWidget(self.max_lat_label, 0, 1)
        stats_layout.addWidget(QLabel("Max Longitudinal G:"), 0, 2)
        stats_layout.addWidget(self.max_long_label, 0, 3)
        stats_layout.addWidget(QLabel("Max Vertical G:"), 0, 4)
        stats_layout.addWidget(self.max_vert_label, 0, 5)
        
        stats_layout.addWidget(QLabel("Avg Lateral G:"), 1, 0)
        stats_layout.addWidget(self.avg_lat_label, 1, 1)
        stats_layout.addWidget(QLabel("Avg Longitudinal G:"), 1, 2)
        stats_layout.addWidget(self.avg_long_label, 1, 3)
        stats_layout.addWidget(QLabel("Avg Vertical G:"), 1, 4)
        stats_layout.addWidget(self.avg_vert_label, 1, 5)
        
        stats_group.setLayout(stats_layout)
        charts_layout.addWidget(stats_group)
        
        # Add charts widget directly to layout (no scroll area)
        layout.addWidget(charts_widget)
    
    def update_data(self, data: TelemetryData):
        """Update spider chart with new telemetry data."""
        time_seconds = data.time_ms / 1000.0
        
        # Store data
        self.time_data.append(time_seconds)
        self.g_force_lat_data.append(data.g_force_lat)
        self.g_force_long_data.append(data.g_force_long)
        self.g_force_vert_data.append(data.g_force_vert)
        self.telemetry_data.append(data)
        
        self.current_index = len(self.telemetry_data) - 1
        
        # Update current spider chart
        self.current_spider.clear_data()
        self.current_spider.add_data(
            [data.g_force_lat, data.g_force_long, data.g_force_vert],
            f"t={time_seconds:.1f}s"
        )
        
        # Update current values display
        self.current_values.setText(
            f"Lateral: {data.g_force_lat:.2f}g | "
            f"Longitudinal: {data.g_force_long:.2f}g | "
            f"Vertical: {data.g_force_vert:.2f}g"
        )
        
        # Émettre le signal avec les données actuelles pour synchroniser avec les graphiques de droite
        self.current_data_changed.emit(data)
        
        # Update statistics
        self.update_statistics()
    
    def update_position(self, data: TelemetryData):
        """Update display for specific time position."""
        if data:
            # Update current spider chart
            self.current_spider.clear_data()
            self.current_spider.add_data(
                [data.g_force_lat, data.g_force_long, data.g_force_vert],
                f"t={data.time_ms/1000:.1f}s"
            )
            
            # Update current values display
            self.current_values.setText(
                f"Lateral: {data.g_force_lat:.2f}g | "
                f"Longitudinal: {data.g_force_long:.2f}g | "
                f"Vertical: {data.g_force_vert:.2f}g"
            )
            
            # Émettre le signal avec les données actuelles pour synchroniser avec les graphiques de droite
            self.current_data_changed.emit(data)
    
    def update_statistics(self):
        """Update G-forces statistics."""
        if self.g_force_lat_data:
            self.max_lat_label.setText(f"{max(self.g_force_lat_data):.2f}g")
            self.max_long_label.setText(f"{max(self.g_force_long_data):.2f}g")
            self.max_vert_label.setText(f"{max(self.g_force_vert_data):.2f}g")
            
            self.avg_lat_label.setText(f"{np.mean(self.g_force_lat_data):.2f}g")
            self.avg_long_label.setText(f"{np.mean(self.g_force_long_data):.2f}g")
            self.avg_vert_label.setText(f"{np.mean(self.g_force_vert_data):.2f}g")
    
    def clear_data(self):
        """Clear all data."""
        self.time_data.clear()
        self.g_force_lat_data.clear()
        self.g_force_long_data.clear()
        self.g_force_vert_data.clear()
        self.telemetry_data.clear()
        
        self.current_spider.clear_data()
        self.comparison_spider.clear_data()
        
        self.current_values.setText("Lateral: 0.0g | Longitudinal: 0.0g | Vertical: 0.0g")
        self.comparison_info.setText("Select time points to compare G-forces")
        
        self.max_lat_label.setText("--")
        self.max_long_label.setText("--")
        self.max_vert_label.setText("--")
        self.avg_lat_label.setText("--")
        self.avg_long_label.setText("--")
        self.avg_vert_label.setText("--")
