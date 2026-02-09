#!/usr/bin/env python3
"""
Test script for temporal analysis widget
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import QApplication
from src.temporal_analysis_widget import TemporalAnalysisWidget
from src.csv_parser import TelemetryData

def test_temporal_widget():
    """Test the temporal analysis widget with sample data."""
    app = QApplication(sys.argv)
    
    # Create widget
    widget = TemporalAnalysisWidget()
    widget.show()
    
    # Add some test data
    for i in range(10):
        data = TelemetryData(
            time_ms=i * 1000,
            speed=50 + i * 5,
            rpm=3000 + i * 200,
            throttle=50 + i * 3,
            battery_temp=25 + i * 0.5,
            g_force_lat=0.1 * i,
            g_force_long=0.2 * i,
            g_force_vert=1.0,
            acceleration_x=0.0,
            acceleration_y=0.0,
            acceleration_z=0.0,
            gps_latitude=48.8566 + i * 0.0001,
            gps_longitude=2.3522 + i * 0.0001,
            gps_altitude=100,
            tire_temp_fl=25 + i,
            tire_temp_fr=25 + i,
            tire_temp_rl=25 + i,
            tire_temp_rr=25 + i
        )
        widget.update_data(data)
    
    print("Test data loaded. Widget should show graphs with data.")
    print("Check if:")
    print("1. Spider chart shows G-forces")
    print("2. Temporal graphs show speed and G-forces over time")
    print("3. Track map shows GPS points")
    print("4. Data selector shows correct count")
    
    return app.exec_()

if __name__ == "__main__":
    test_temporal_widget()
