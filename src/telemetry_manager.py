"""
Data Manager Module - Manages current and historical telemetry data.
"""

from typing import List, Optional
from .csv_parser import TelemetryData
import app_config as config


class TelemetryManager:
    """
    Maintains current telemetry state and historical data.
    Acts as the central hub for data processing.
    """
    
    def __init__(self):
        """Initialize the data manager."""
        self.current: Optional[TelemetryData] = None
        self.history: List[TelemetryData] = []
        self.update_count = 0
    
    def update(self, data: TelemetryData):
        """
        Update with new telemetry data.
        
        :param data: New TelemetryData object
        """
        if data is None:
            return
        
        self.current = data
        self.history.append(data)
        self.update_count += 1
    
    def get_current(self) -> Optional[TelemetryData]:
        """Get the most recent telemetry data."""
        return self.current
    
    def get_history(self) -> List[TelemetryData]:
        """Get all historical data."""
        return self.history
    
    def get_history_count(self) -> int:
        """Get number of data points collected."""
        return len(self.history)
    
    def get_stats(self) -> dict:
        """
        Calculate summary statistics from collected data.
        
        :return: Dictionary with min/max/avg values
        """
        if not self.history:
            return {}
        
        speeds = [d.speed for d in self.history]
        rpms = [d.rpm for d in self.history]
        temps = [d.battery_temp for d in self.history]
        throttles = [d.throttle for d in self.history]
        
        return {
            'max_speed': max(speeds),
            'min_speed': min(speeds),
            'avg_speed': sum(speeds) / len(speeds),
            'max_rpm': max(rpms),
            'min_rpm': min(rpms),
            'avg_rpm': sum(rpms) / len(rpms),
            'max_temp': max(temps),
            'min_temp': min(temps),
            'avg_temp': sum(temps) / len(temps),
            'max_throttle': max(throttles),
            'data_points': len(self.history),
        }
    
    def clear_history(self):
        """Clear all historical data."""
        self.history.clear()
        self.update_count = 0
        self.current = None
    
    def reset_stats(self):
        """Reset all statistics and data to initial state."""
        self.clear_history()
