"""
CSV Source - Replay telemetry data from a previously recorded CSV file.
"""

from .telemetry_source import TelemetrySource


class CSVSource(TelemetrySource):
    """
    Reads telemetry data from a CSV file.
    Used for offline analysis and replay of recorded runs.
    """
    
    def __init__(self, filename: str):
        """
        Initialize CSV file reader.
        
        :param filename: Path to CSV file
        """
        self.filename = filename
        self.file = None
        self.line_count = 0
        self._open()
    
    def _open(self):
        """Open and read CSV file."""
        try:
            self.file = open(self.filename, 'r')
            print(f"✓ Opened CSV file: {self.filename}")
        except FileNotFoundError as e:
            print(f"✗ File not found: {e}")
            raise
    
    def read(self) -> str:
        """
        Read one line from CSV file.
        
        :return: CSV-formatted line or empty string if EOF
        """
        if not self.is_connected():
            return ""
        
        try:
            line = self.file.readline().strip()
            if line:
                self.line_count += 1
            return line
        except Exception as e:
            print(f"⚠️  CSV read error: {e}")
            return ""
    
    def is_connected(self) -> bool:
        """Check if file is open."""
        return self.file is not None and not self.file.closed
    
    def close(self):
        """Close the CSV file."""
        if self.file and not self.file.closed:
            self.file.close()
            print(f"CSV file closed ({self.line_count} lines read)")
