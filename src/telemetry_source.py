"""
Abstract Telemetry Source Interface
Allows swapping between Arduino (live) and CSV (replay) without changing main logic.
"""

from abc import ABC, abstractmethod


class TelemetrySource(ABC):
    """
    Abstract base class for telemetry data sources.
    Supports both live (Arduino) and offline (CSV replay) modes.
    """
    
    @abstractmethod
    def read(self) -> str:
        """
        Read one line of telemetry data.
        
        :return: CSV-formatted string
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if the data source is available.
        
        :return: True if connected/available
        """
        pass
    
    @abstractmethod
    def close(self):
        """
        Clean up resources (close serial connection, file handles, etc).
        """
        pass
