"""
CSV Logging Module - Saves telemetry data to CSV files for persistent storage.
"""

import csv
from datetime import datetime
from pathlib import Path
from parsing.csv_parser import TelemetryData
import config


class CSVLogger:
    """
    Logs telemetry data to CSV files with proper formatting and headers.
    """
    
    def __init__(self, filename: str = None):
        """
        Initialize CSV logger.
        
        :param filename: Output CSV filename (auto-generated if None)
        """
        if filename is None:
            filename = self._generate_filename()
        
        self.filepath = Path(config.LOG_DIRECTORY) / filename
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        self.file = None
        self.writer = None
        self._init_file()
    
    def _generate_filename(self) -> str:
        """Generate unique filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        return f"{config.LOG_FILENAME_PREFIX}_{timestamp}.csv"
    
    def _init_file(self):
        """Create and initialize CSV file with header."""
        try:
            self.file = open(self.filepath, 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file, delimiter=config.CSV_DELIMITER)
            self.writer.writerow(config.CSV_HEADER)
            self.file.flush()
            print(f"✓ Logging to: {self.filepath}")
        except IOError as e:
            print(f"✗ Failed to create log file: {e}")
            raise
    
    def log(self, data: TelemetryData):
        """
        Write one telemetry data point to CSV.
        
        :param data: TelemetryData object to log
        """
        if self.writer is None:
            print("⚠️  Logger not initialized")
            return
        
        try:
            self.writer.writerow([
                data.time_ms,
                data.speed,
                data.rpm,
                data.throttle,
                data.battery_temp
            ])
            self.file.flush()
        except Exception as e:
            print(f"⚠️  Logging error: {e}")
    
    def close(self):
        """Close and finalize the CSV file."""
        if self.file and not self.file.closed:
            self.file.close()
            print(f"✓ Log file saved: {self.filepath}")
