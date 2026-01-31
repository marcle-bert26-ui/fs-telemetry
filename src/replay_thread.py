"""
Replay Thread Module
Handles CSV file replay functionality.
"""

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import csv
from .csv_parser import parse_csv_line
from .telemetry_manager import TelemetryManager

class ReplayThread(QThread):
    """Thread for replaying CSV telemetry data."""
    
    data_received = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, csv_file_path: str):
        """Initialize replay thread."""
        super().__init__()
        self.csv_file_path = csv_file_path
        self.running = False
        self.manager = TelemetryManager()
        self.current_row = 0
        self.rows = []
        
    def run(self):
        """Run the replay thread."""
        try:
            self.running = True
            self.status_changed.emit("Loading CSV file...")
            
            # Load CSV file
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.rows = list(reader)
            
            self.status_changed.emit(f"Loaded {len(self.rows)} rows")
            
            # Replay data
            for i, row in enumerate(self.rows):
                if not self.running:
                    break
                
                # Parse CSV row
                data = parse_csv_line(','.join(row))
                if data:
                    self.manager.update(data)
                    self.data_received.emit(data)
                    
                    # Update status
                    if i % 10 == 0:
                        self.status_changed.emit(f"Replaying row {i+1}/{len(self.rows)}")
                
                # Small delay for realistic replay speed
                self.msleep(50)
            
            self.status_changed.emit("Replay complete")
            
        except Exception as e:
            self.error_occurred.emit(f"Replay error: {str(e)}")
        finally:
            self.finished.emit()
    
    def stop(self):
        """Stop the replay thread."""
        self.running = False
