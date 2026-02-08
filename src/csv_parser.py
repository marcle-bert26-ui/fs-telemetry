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
        g_force_lat: Lateral G-force (cornering forces)
        g_force_long: Longitudinal G-force (acceleration/braking)
        g_force_vert: Vertical G-force (bumps/weight transfer)
        acceleration_x: Linear acceleration X-axis in m/s²
        acceleration_y: Linear acceleration Y-axis in m/s²
        acceleration_z: Linear acceleration Z-axis in m/s²
        gps_latitude: GPS latitude coordinate
        gps_longitude: GPS longitude coordinate
        gps_altitude: GPS altitude in meters
        tire_temp_fl: Front left tire temperature in Celsius
        tire_temp_fr: Front right tire temperature in Celsius
        tire_temp_rl: Rear left tire temperature in Celsius
        tire_temp_rr: Rear right tire temperature in Celsius
    """
    time_ms: int
    speed: float
    rpm: int
    throttle: float
    battery_temp: float
    g_force_lat: float
    g_force_long: float
    g_force_vert: float
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    gps_latitude: float
    gps_longitude: float
    gps_altitude: float
    tire_temp_fl: float
    tire_temp_fr: float
    tire_temp_rl: float
    tire_temp_rr: float

    def __str__(self):
        return (
            f"Time: {self.time_ms}ms | "
            f"Speed: {self.speed:.1f} km/h | "
            f"RPM: {self.rpm} | "
            f"Throttle: {self.throttle:.1f}% | "
            f"Bat Temp: {self.battery_temp:.1f}°C | "
            f"G-Forces: L:{self.g_force_lat:.2f}g F:{self.g_force_long:.2f}g V:{self.g_force_vert:.2f}g | "
            f"Accel: X:{self.acceleration_x:.1f} Y:{self.acceleration_y:.1f} Z:{self.acceleration_z:.1f} m/s² | "
            f"GPS: {self.gps_latitude:.6f},{self.gps_longitude:.6f} | "
            f"Tire Temps: FL:{self.tire_temp_fl:.1f}° FR:{self.tire_temp_fr:.1f}° RL:{self.tire_temp_rl:.1f}° RR:{self.tire_temp_rr:.1f}°"
        )


def parse_csv_line(line: str) -> Optional[TelemetryData]:
    """
    Parse a CSV line from the Arduino into a TelemetryData object.
    
    Supports both legacy format (5 fields) and enhanced format (18 fields).
    
    Legacy format: time_ms;speed_kmh;rpm;throttle;battery_temp
    Enhanced format: time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr
    
    Example: 123456;45.2;8120;0.78;62.3;0.5;0.3;1.0;2.1;0.5;9.8;48.8566;2.3522;150;75.2;74.8;73.5;74.1
    
    :param line: Raw CSV line from Arduino/file
    :return: TelemetryData object or None if parsing fails
    """
    try:
        # Remove whitespace
        line = line.strip()
        
        # Skip empty lines and header
        if not line or line.startswith("time_ms"):
            return None
        
        # Split by semicolon
        values = line.split(";")
        
        # Handle both 5-field and 18-field formats
        if len(values) == 5:
            # Legacy format - parse first 5 fields, set others to defaults
            data = TelemetryData(
                time_ms=int(values[0]),
                speed=float(values[1]),
                rpm=int(values[2]),
                throttle=float(values[3]),
                battery_temp=float(values[4]),
                g_force_lat=0.0,  # Default values
                g_force_long=0.0,
                g_force_vert=1.0,
                acceleration_x=0.0,
                acceleration_y=0.0,
                acceleration_z=0.0,
                gps_latitude=0.0,
                gps_longitude=0.0,
                gps_altitude=0.0,
                tire_temp_fl=0.0,
                tire_temp_fr=0.0,
                tire_temp_rl=0.0,
                tire_temp_rr=0.0
            )
        elif len(values) == 18:
            # Enhanced format - parse all fields
            data = TelemetryData(
                time_ms=int(values[0]),
                speed=float(values[1]),
                rpm=int(values[2]),
                throttle=float(values[3]),
                battery_temp=float(values[4]),
                g_force_lat=float(values[5]),
                g_force_long=float(values[6]),
                g_force_vert=float(values[7]),
                acceleration_x=float(values[8]),
                acceleration_y=float(values[9]),
                acceleration_z=float(values[10]),
                gps_latitude=float(values[11]),
                gps_longitude=float(values[12]),
                gps_altitude=float(values[13]),
                tire_temp_fl=float(values[14]),
                tire_temp_fr=float(values[15]),
                tire_temp_rl=float(values[16]),
                tire_temp_rr=float(values[17])
            )
        else:
            # print(f"ERROR: Expected 5 or 18 fields, got {len(values)} | Line: {line}")
            return None
        
        return data
        
    except (ValueError, IndexError) as e:
        # print(f"ERROR: {e} | Line: {line}")
        return None


# CSV header for logging
CSV_HEADER = [
    "time_ms", "speed", "rpm", "throttle", "battery_temp", 
    "g_force_lat", "g_force_long", "g_force_vert", 
    "acceleration_x", "acceleration_y", "acceleration_z",
    "gps_latitude", "gps_longitude", "gps_altitude",
    "tire_temp_fl", "tire_temp_fr", "tire_temp_rl", "tire_temp_rr"
]
