"""
Console Display Module - Real-time telemetry display in terminal.
"""

from csv_parser import TelemetryData


class ConsoleDisplay:
    """
    Simple console-based visualization of telemetry data.
    """
    
    def __init__(self, update_interval: int = 10):
        """
        Initialize console display.
        
        :param update_interval: Update display every N data points
        """
        self.update_interval = update_interval
        self.display_count = 0
    
    def update(self, data: TelemetryData):
        """
        Display telemetry data to console.
        
        :param data: TelemetryData to display
        """
        self.display_count += 1
        
        # Only display every N updates to avoid spam
        if self.display_count % self.update_interval == 0:
            print(f"[{self.display_count}] {data}")
    
    def print_header(self):
        """Print header information."""
        print("\n" + "=" * 80)
        print("[RACING CAR] Formula Student Telemetry System")
        print("=" * 80 + "\n")
    
    def print_footer(self, stats: dict):
        """
        Print summary statistics.
        
        :param stats: Dictionary of statistics from TelemetryManager
        """
        if not stats:
            return
        
        print("\n" + "=" * 80)
        print("📊 Session Summary")
        print("=" * 80)
        print(f"Data Points:     {stats['data_points']}")
        print(f"Speed:           {stats['min_speed']:.1f} - {stats['max_speed']:.1f} km/h (avg: {stats['avg_speed']:.1f})")
        print(f"RPM:             {stats['min_rpm']} - {stats['max_rpm']}")
        print(f"Throttle:        0 - {stats['max_throttle']:.1f}%")
        print(f"Battery Temp:    {stats['min_temp']:.1f} - {stats['max_temp']:.1f}°C (avg: {stats['avg_temp']:.1f})")
        print("=" * 80 + "\n")
