"""
Serial Source - Read live telemetry data from Arduino via USB serial connection.
"""

import serial
from .telemetry_source import TelemetrySource


class SerialSource(TelemetrySource):
    """
    Reads telemetry data directly from Arduino via serial port.
    Used for live data acquisition during test drives.
    """
    
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1.0):
        """
        Initialize serial connection to Arduino.
        
        :param port: Serial port name (e.g., 'COM3', '/dev/ttyUSB0')
        :param baudrate: Serial communication speed
        :param timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self._connect()
    
    def _connect(self):
        """Establish serial connection."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"+ Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            print(f"X Failed to connect: {e}")
            raise
    
    def read(self) -> str:
        """
        Read one line from Arduino serial port.
        
        :return: CSV-formatted line
        """
        if not self.is_connected():
            return ""
        
        try:
            line = self.ser.readline().decode(errors='ignore').strip()
            return line
        except Exception as e:
            print(f"! Serial read error: {e}")
            return ""
    
    def is_connected(self) -> bool:
        """Check if serial connection is open."""
        return self.ser is not None and self.ser.is_open
    
    def close(self):
        """Close the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed")
