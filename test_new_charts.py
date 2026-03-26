"""
Test script for the new 5-parameter charts
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


class FakeTelemetryData:
    def __init__(self, time_ms, rpm, throttle, g_force_long):
        self.time_ms = time_ms
        self.rpm = rpm
        self.throttle = throttle
        self.g_force_long = g_force_long
        # Add other required attributes
        self.speed = 50
        self.battery_temp = 25


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New 5-Parameter Charts Test")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.charts = TelemetryCharts()
        layout.addWidget(self.charts)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_data)
        self.timer.start(100)
        
        self.time_counter = 0
    
    def simulate_data(self):
        phase = (self.time_counter // 100) % 4
        
        if phase == 0:  # Idle
            rpm = random.uniform(1400, 1700)
            throttle = random.uniform(0, 2)
            g_force_long = random.uniform(-0.5, 0.5)
        elif phase == 1:  # Acceleration
            rpm = random.uniform(1500, 7500)
            throttle = random.uniform(10, 80)
            g_force_long = random.uniform(0.5, 2.0)
        elif phase == 2:  # Full throttle
            rpm = random.uniform(7000, 8000)
            throttle = random.uniform(80, 100)
            g_force_long = random.uniform(1.5, 3.0)
        else:  # Deceleration
            rpm = random.uniform(2000, 6000)
            throttle = random.uniform(0, 20)
            g_force_long = random.uniform(-2.0, -0.5)
        
        data = FakeTelemetryData(self.time_counter * 100, rpm, throttle, g_force_long)
        self.charts.update_data(data)
        
        self.time_counter += 1


def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
