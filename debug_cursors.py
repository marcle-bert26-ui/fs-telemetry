"""
Debug script to test cursor functionality
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import random

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from telemetry_charts import TelemetryCharts
from csv_parser import TelemetryData


class DebugWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debug Cursors")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.charts = TelemetryCharts()
        layout.addWidget(self.charts)
        
        # Generate test data
        self.test_data = []
        for i in range(100):
            data = TelemetryData(
                time_ms=i * 1000,
                speed=random.uniform(0, 150),
                rpm=random.uniform(1000, 8000),
                throttle=random.uniform(0, 100),
                battery_temp=random.uniform(20, 80),
                g_force_lat=random.uniform(-2, 2),
                g_force_long=random.uniform(-2, 2),
                g_force_vert=random.uniform(-1, 1),
                acceleration_x=0, acceleration_y=0, acceleration_z=0,
                gps_latitude=0, gps_longitude=0, gps_altitude=0,
                tire_temp_fl=0, tire_temp_fr=0, tire_temp_rl=0, tire_temp_rr=0
            )
            self.test_data.append(data)
        
        # Load all data into charts
        for data in self.test_data:
            self.charts.update_data(data)
        
        # Test cursor updates
        self.cursor_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor)
        self.timer.start(500)  # Update every 500ms
    
    def update_cursor(self):
        """Update cursor position"""
        if self.cursor_index < len(self.test_data):
            data = self.test_data[self.cursor_index]
            print(f"Updating cursor to index {self.cursor_index}, RPM: {data.rpm}")
            
            # Update cursor points manually
            self.update_chart_cursors(data, self.cursor_index)
            
            self.cursor_index += 1
        else:
            self.timer.stop()
    
    def update_chart_cursors(self, data, point_idx):
        """Update cursor points on telemetry charts."""
        try:
            if hasattr(self.charts, 'rpm_plot') and self.charts.rpm_plot:
                # Update RPM cursor
                if hasattr(self.charts.rpm_plot, 'current_points') and self.charts.rpm_plot.current_points:
                    time_ms = getattr(data, 'time_ms', 0) / 1000.0
                    value = getattr(data, 'rpm', 0)
                    
                    print(f"  RPM cursor: time={time_ms}, value={value}")
                    
                    # Remove old cursor point if exists
                    if self.charts.rpm_plot.current_points[0] is not None:
                        self.charts.rpm_plot.current_points[0].clear()
                    
                    # Create new cursor point
                    from pyqtgraph import pg
                    color = '#00ff88'
                    cursor_point = self.charts.rpm_plot.plot([time_ms], [value], 
                                                            pen=None, 
                                                            symbol='o', 
                                                            symbolBrush=color, 
                                                            symbolSize=12, 
                                                            symbolPen=pg.mkPen(color='white', width=2))
                    self.charts.rpm_plot.current_points[0] = cursor_point
                    
        except Exception as e:
            print(f"Error updating cursor: {e}")


def main():
    app = QApplication(sys.argv)
    window = DebugWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
