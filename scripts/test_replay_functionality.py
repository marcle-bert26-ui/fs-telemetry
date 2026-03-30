#!/usr/bin/env python3
"""
Test script pour vérifier que le mode replay fonctionne correctement.
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.replay_mode_widget import ReplayModeWidget
from src.data.csv_parser import TelemetryData, parse_csv_line
import csv

def create_test_csv():
    """Create a test CSV file with sample data."""
    test_file = "data/samples/test_replay.csv"
    
    # Create sample data
    sample_data = [
        TelemetryData(100, 10.5, 2000, 25, 35.2, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 48.8566, 2.3522, 100, 25, 25, 25, 25),
        TelemetryData(200, 15.3, 2500, 40, 35.5, 0.1, 0.2, 0.9, 0.1, 0.1, 0.1, 48.8561, 2.3523, 102, 26, 26, 26, 26),
        TelemetryData(300, 22.1, 3200, 60, 36.1, 0.2, 0.3, 0.8, 0.2, 0.2, 0.2, 48.8556, 2.3524, 105, 27, 27, 27, 27),
        TelemetryData(400, 28.7, 3800, 80, 36.8, 0.3, 0.4, 0.7, 0.3, 0.3, 0.3, 48.8551, 2.3525, 108, 28, 28, 28, 28),
        TelemetryData(500, 32.5, 4200, 100, 37.2, 0.4, 0.5, 0.6, 0.4, 0.4, 0.4, 48.8546, 2.3526, 110, 29, 29, 29, 29),
    ]
    
    # Write to CSV
    with open(test_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("time_ms,speed,rpm,throttle,battery_temp,g_force_lat,g_force_long,g_force_vert,acceleration_x,acceleration_y,acceleration_z,gps_latitude,gps_longitude,gps_altitude,tire_temp_fl,tire_temp_fr,tire_temp_rl,tire_temp_rr\n")
        
        # Write data
        for data in sample_data:
            f.write(f"{data.time_ms},{data.speed},{data.rpm},{data.throttle},{data.battery_temp},{data.g_force_lat},{data.g_force_long},{data.g_force_vert},{data.acceleration_x},{data.acceleration_y},{data.acceleration_z},{data.gps_latitude},{data.gps_longitude},{data.gps_altitude},{data.tire_temp_fl},{data.tire_temp_fr},{data.tire_temp_rl},{data.tire_temp_rr}\n")
    
    print(f"Test CSV created: {test_file}")
    return test_file

def test_replay_widget():
    """Test replay widget."""
    print("Testing Replay Widget...")
    
    # Create test CSV
    test_file = create_test_csv()
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create replay widget
    widget = ReplayModeWidget()
    
    # Load test file
    widget.current_file = test_file
    widget.on_file_selected(test_file)
    
    # Show widget
    widget.show()
    widget.setWindowTitle("Replay Mode Test")
    
    print("Replay widget created and test file loaded")
    print("Test data: 5 telemetry points")
    print("You can now test the replay functionality:")
    print("   - Click 'Play' to start replay")
    print("   - Use the timeline slider to navigate")
    print("   - Check that labels update correctly")
    print("   - Verify charts display data")
    
    # Auto-close after 30 seconds for testing
    QTimer.singleShot(30000, app.quit)
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_replay_widget()
