"""
CSV Logger Module
Handles logging telemetry data to CSV files.
"""

import os
import csv
from datetime import datetime
from typing import TextIO

class CSVLogger:
    """CSV logger for telemetry data."""
    
    def __init__(self, filename: str = None):
        """Initialize CSV logger."""
        self.filename = filename
        self.filepath = filename  # Add filepath attribute for compatibility
        self.file_handle = None
        self.csv_writer = None
        
    def start_logging(self, filename: str = None) -> str:
        """Start logging to CSV file."""
        if filename:
            self.filename = filename
            self.filepath = filename  # Update filepath too
        
        if not self.filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
            self.filename = f"data_logs/run_{timestamp}.csv"
            self.filepath = self.filename  # Update filepath too
        
        # Create data_logs directory if it doesn't exist
        dirname = os.path.dirname(self.filename)
        if dirname:  # Only create directory if dirname is not empty
            os.makedirs(dirname, exist_ok=True)
        
        self.file_handle = open(self.filename, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file_handle)
        
        # Write header
        from .csv_parser import CSV_HEADER
        self.csv_writer.writerow(CSV_HEADER)
        
        return self.filename
    
    def log(self, data):
        """Log telemetry data to CSV."""
        if self.csv_writer and self.file_handle:
            # Convert TelemetryData to CSV format
            if hasattr(data, 'time_ms'):
                row = [
                    data.time_ms,
                    data.speed,
                    data.rpm,
                    data.throttle,
                    data.battery_temp,
                    data.g_force_lat,
                    data.g_force_long,
                    data.g_force_vert,
                    data.acceleration_x,
                    data.acceleration_y,
                    data.acceleration_z,
                    data.gps_latitude,
                    data.gps_longitude,
                    data.gps_altitude,
                    data.tire_temp_fl,
                    data.tire_temp_fr,
                    data.tire_temp_rl,
                    data.tire_temp_rr
                ]
                self.csv_writer.writerow(row)
    
    def close(self):
        """Close CSV file."""
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
            self.csv_writer = None
