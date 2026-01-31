"""
Console Handler Module
Handles console output for telemetry data.
"""

class ConsoleHandler:
    """Console handler for telemetry data display."""
    
    def __init__(self):
        """Initialize console handler."""
        self.enabled = True
        
    def print_header(self):
        """Print header for telemetry display."""
        if self.enabled:
            print("\n" + "=" * 80)
            print("[RACING CAR] Formula Student Telemetry System")
            print("=" * 80 + "\n")
    
    def print_data(self, data):
        """Print telemetry data to console."""
        if self.enabled and hasattr(data, 'speed'):
            print(f"Speed: {data.speed:.1f} km/h | RPM: {data.rpm:.0f} | "
                  f"Throttle: {data.throttle:.0f}% | Temp: {data.battery_temp:.1f}°C")
    
    def print_status(self, message):
        """Print status message."""
        if self.enabled:
            print(f"[STATUS] {message}")
    
    def print_error(self, message):
        """Print error message."""
        if self.enabled:
            print(f"[ERROR] {message}")
