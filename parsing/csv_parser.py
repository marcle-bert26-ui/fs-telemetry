"""
CSV Parser Module
Converts raw CSV lines into TelemetryData objects with proper type conversion and validation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TelemetryData:
    """
    Represents a single telemetry data point from the vehicle.
    
    Attributes:
        time_ms: Timestamp in milliseconds since start
        speed: Vehicle speed in km/h
        rpm: Engine RPM
        throttle: Throttle percentage (0-100)
        battery_temp: Battery temperature in Celsius
    """
    time_ms: int
    speed: float
    rpm: int
    throttle: float
    battery_temp: float

    def __str__(self):
        return (
            f"Time: {self.time_ms}ms | "
            f"Speed: {self.speed:.1f} km/h | "
            f"RPM: {self.rpm} | "
            f"Throttle: {self.throttle:.1f}% | "
            f"Temp: {self.battery_temp:.1f}°C"
        )


def parse_csv_line(line: str) -> Optional[TelemetryData]:
    """
    Parse a CSV line from the Arduino into a TelemetryData object.
    
    Expected format: time_ms;speed_kmh;rpm;throttle;battery_temp
    Example: 123456;45.2;8120;0.78;62.3
    
    :param line: Raw CSV line from Arduino/file
    :return: TelemetryData object or None if parsing fails
    """
    try:
        # Remove whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line or line.startswith("time_ms"):
            return None
        
        # Split by semicolon
        values = line.split(";")
        
        # Validate number of fields
        if len(values) != 5:
            raise ValueError(f"Expected 5 fields, got {len(values)}")
        
        # Parse and convert types
        data = TelemetryData(
            time_ms=int(values[0]),
            speed=float(values[1]),
            rpm=int(values[2]),
            throttle=float(values[3]),
            battery_temp=float(values[4])
        )
        
        return data
        
    except (ValueError, IndexError) as e:
        print(f"⚠️  Parse error: {e} | Line: {line}")
        return None
