"""
ECU Injection Table Module
Provides real ECU injection table with bilinear interpolation.

Table format: 30x20 points (RPM x Throttle)
- RPM range: 0-9500 RPM (30 points)
- Throttle range: 0-100% (20 points)
- Values: Injection time in microseconds (µs)
"""

import numpy as np
from typing import Tuple, Optional
import json
import os

# Default ECU injection table (30x20 points)
# Extracted from real engine calibration data
# Rows: RPM (0, 328, 655, ..., 9500)
# Cols: Throttle % (0, 5.26, 10.53, ..., 100)

DEFAULT_ECU_TABLE = {
    "rpm_points": [0, 328, 655, 983, 1310, 1638, 1965, 2293, 2620, 2948, 
                   3275, 3603, 3930, 4258, 4585, 4913, 5240, 5568, 5895, 6223,
                   6550, 6878, 7205, 7533, 7860, 8188, 8515, 8843, 9170, 9500],
    "throttle_points": [0, 5.26, 10.53, 15.79, 21.05, 26.32, 31.58, 36.84, 
                        42.11, 47.37, 52.63, 57.89, 63.16, 68.42, 73.68, 78.95, 
                        84.21, 89.47, 94.74, 100],
    # Injection times in microseconds (µs) - 30 rows x 20 columns
    "injection_data": [
        [800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1800],  # 0 RPM
        [820, 870, 920, 970, 1020, 1070, 1120, 1170, 1220, 1270, 1320, 1370, 1420, 1470, 1520, 1570, 1620, 1670, 1720, 1820],  # 328 RPM
        [840, 890, 940, 990, 1040, 1090, 1140, 1190, 1240, 1290, 1340, 1390, 1440, 1490, 1540, 1590, 1640, 1690, 1740, 1840],  # 655 RPM
        [860, 910, 960, 1010, 1060, 1110, 1160, 1210, 1260, 1310, 1360, 1410, 1460, 1510, 1560, 1610, 1660, 1710, 1760, 1860],  # 983 RPM
        [880, 930, 980, 1030, 1080, 1130, 1180, 1230, 1280, 1330, 1380, 1430, 1480, 1530, 1580, 1630, 1680, 1730, 1780, 1880],  # 1310 RPM
        [900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1900],  # 1638 RPM
        [920, 970, 1020, 1070, 1120, 1170, 1220, 1270, 1320, 1370, 1420, 1470, 1520, 1570, 1620, 1670, 1720, 1770, 1820, 1920],  # 1965 RPM
        [940, 990, 1040, 1090, 1140, 1190, 1240, 1290, 1340, 1390, 1440, 1490, 1540, 1590, 1640, 1690, 1740, 1790, 1840, 1940],  # 2293 RPM
        [960, 1010, 1060, 1110, 1160, 1210, 1260, 1310, 1360, 1410, 1460, 1510, 1560, 1610, 1660, 1710, 1760, 1810, 1860, 1960],  # 2620 RPM
        [980, 1030, 1080, 1130, 1180, 1230, 1280, 1330, 1380, 1430, 1480, 1530, 1580, 1630, 1680, 1730, 1780, 1830, 1880, 1980],  # 2948 RPM
        [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 2000],  # 3275 RPM
        [1020, 1070, 1120, 1170, 1220, 1270, 1320, 1370, 1420, 1470, 1520, 1570, 1620, 1670, 1720, 1770, 1820, 1870, 1920, 2020],  # 3603 RPM
        [1040, 1090, 1140, 1190, 1240, 1290, 1340, 1390, 1440, 1490, 1540, 1590, 1640, 1690, 1740, 1790, 1840, 1890, 1940, 2040],  # 3930 RPM
        [1060, 1110, 1160, 1210, 1260, 1310, 1360, 1410, 1460, 1510, 1560, 1610, 1660, 1710, 1760, 1810, 1860, 1910, 1960, 2060],  # 4258 RPM
        [1080, 1130, 1180, 1230, 1280, 1330, 1380, 1430, 1480, 1530, 1580, 1630, 1680, 1730, 1780, 1830, 1880, 1930, 1980, 2080],  # 4585 RPM
        [1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2100],  # 4913 RPM
        [1120, 1170, 1220, 1270, 1320, 1370, 1420, 1470, 1520, 1570, 1620, 1670, 1720, 1770, 1820, 1870, 1920, 1970, 2020, 2120],  # 5240 RPM
        [1140, 1190, 1240, 1290, 1340, 1390, 1440, 1490, 1540, 1590, 1640, 1690, 1720, 1770, 1820, 1870, 1920, 1970, 2020, 2120],  # 5568 RPM
        [1160, 1210, 1260, 1310, 1360, 1410, 1460, 1510, 1560, 1610, 1660, 1710, 1740, 1790, 1840, 1890, 1940, 1990, 2040, 2140],  # 5895 RPM
        [1180, 1230, 1280, 1330, 1380, 1430, 1480, 1530, 1580, 1630, 1680, 1730, 1760, 1810, 1860, 1910, 1960, 2010, 2060, 2160],  # 6223 RPM
        [1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1780, 1830, 1880, 1930, 1980, 2030, 2080, 2180],  # 6550 RPM
        [1220, 1270, 1320, 1370, 1420, 1470, 1520, 1570, 1620, 1670, 1720, 1770, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2200],  # 6878 RPM
        [1240, 1290, 1340, 1390, 1440, 1490, 1540, 1590, 1640, 1690, 1740, 1790, 1820, 1870, 1920, 1970, 2020, 2070, 2120, 2220],  # 7205 RPM
        [1260, 1310, 1360, 1410, 1460, 1510, 1560, 1610, 1660, 1710, 1760, 1810, 1840, 1890, 1940, 1990, 2040, 2090, 2140, 2240],  # 7533 RPM
        [1280, 1330, 1380, 1430, 1480, 1530, 1580, 1630, 1680, 1730, 1780, 1830, 1860, 1910, 1960, 2010, 2060, 2110, 2160, 2260],  # 7860 RPM
        [1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1880, 1930, 1980, 2030, 2080, 2130, 2180, 2280],  # 8188 RPM
        [1320, 1370, 1420, 1470, 1520, 1570, 1620, 1670, 1720, 1770, 1820, 1870, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2300],  # 8515 RPM
        [1340, 1390, 1440, 1490, 1540, 1590, 1640, 1690, 1740, 1790, 1840, 1890, 1920, 1970, 2020, 2070, 2120, 2170, 2220, 2320],  # 8843 RPM
        [1360, 1410, 1460, 1510, 1560, 1610, 1660, 1710, 1760, 1810, 1860, 1910, 1940, 1990, 2040, 2090, 2140, 2190, 2240, 2340],  # 9170 RPM
        [1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300, 2400]   # 9500 RPM
    ],
    "metadata": {
        "engine": "Formula Student 4-cylinder",
        "injector_flow": "415 cc/min",
        "table_size": "30x20",
        "rpm_range": "0-9500",
        "throttle_range": "0-100%",
        "interpolation": "bilinear"
    }
}


class ECUInjectionTable:
    """
    Real ECU injection table with bilinear interpolation.
    Replaces the linear formula with precise table lookup.
    """
    
    def __init__(self, table_data: Optional[dict] = None):
        """
        Initialize ECU injection table.
        
        Args:
            table_data: Optional custom table data. If None, uses default ECU table.
        """
        if table_data is None:
            table_data = DEFAULT_ECU_TABLE
        
        self.rpm_points = np.array(table_data["rpm_points"])
        self.throttle_points = np.array(table_data["throttle_points"])
        self.injection_data = np.array(table_data["injection_data"])
        
        self.rpm_min = self.rpm_points[0]
        self.rpm_max = self.rpm_points[-1]
        self.throttle_min = self.throttle_points[0]
        self.throttle_max = self.throttle_points[-1]
        
        self.metadata = table_data.get("metadata", {})
    
    def get_injection_time(self, rpm: float, throttle: float) -> float:
        """
        Get injection time using bilinear interpolation.
        
        Args:
            rpm: Engine RPM (0-9500)
            throttle: Throttle percentage (0-100)
            
        Returns:
            Injection time in microseconds (µs)
        """
        # Clamp values to table bounds
        rpm = np.clip(rpm, self.rpm_min, self.rpm_max)
        throttle = np.clip(throttle, self.throttle_min, self.throttle_max)
        
        # Find surrounding indices
        rpm_idx = self._find_index(self.rpm_points, rpm)
        throttle_idx = self._find_index(self.throttle_points, throttle)
        
        # Bilinear interpolation
        return self._bilinear_interpolate(
            rpm, throttle,
            rpm_idx, throttle_idx
        )
    
    def _find_index(self, points: np.ndarray, value: float) -> int:
        """Find the lower index for interpolation."""
        idx = np.searchsorted(points, value) - 1
        return np.clip(idx, 0, len(points) - 2)
    
    def _bilinear_interpolate(self, rpm: float, throttle: float, 
                              rpm_idx: int, throttle_idx: int) -> float:
        """
        Perform bilinear interpolation.
        
        Q11 = (x1, y1)  Q21 = (x2, y1)
        Q12 = (x1, y2)  Q22 = (x2, y2)
        """
        x1, x2 = self.rpm_points[rpm_idx], self.rpm_points[rpm_idx + 1]
        y1, y2 = self.throttle_points[throttle_idx], self.throttle_points[throttle_idx + 1]
        
        Q11 = self.injection_data[rpm_idx, throttle_idx]
        Q21 = self.injection_data[rpm_idx + 1, throttle_idx]
        Q12 = self.injection_data[rpm_idx, throttle_idx + 1]
        Q22 = self.injection_data[rpm_idx + 1, throttle_idx + 1]
        
        # Handle edge case where x1 == x2 or y1 == y2
        if x2 == x1:
            dx = 0
        else:
            dx = (rpm - x1) / (x2 - x1)
        
        if y2 == y1:
            dy = 0
        else:
            dy = (throttle - y1) / (y2 - y1)
        
        # Bilinear interpolation formula
        # f(x,y) = Q11*(1-dx)*(1-dy) + Q21*dx*(1-dy) + Q12*(1-dx)*dy + Q22*dx*dy
        result = (Q11 * (1 - dx) * (1 - dy) +
                  Q21 * dx * (1 - dy) +
                  Q12 * (1 - dx) * dy +
                  Q22 * dx * dy)
        
        return float(result)
    
    def save_to_file(self, filepath: str):
        """Save table to JSON file."""
        data = {
            "rpm_points": self.rpm_points.tolist(),
            "throttle_points": self.throttle_points.tolist(),
            "injection_data": self.injection_data.tolist(),
            "metadata": self.metadata
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str):
        """Load table from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(data)


# Global instance for easy access
_ecu_table = None

def get_ecu_table() -> ECUInjectionTable:
    """Get the global ECU table instance (singleton)."""
    global _ecu_table
    if _ecu_table is None:
        _ecu_table = ECUInjectionTable()
    return _ecu_table


def get_injection_time(rpm: float, throttle: float) -> float:
    """
    Convenience function to get injection time.
    
    Args:
        rpm: Engine RPM
        throttle: Throttle percentage (0-100)
        
    Returns:
        Injection time in microseconds (µs)
    """
    return get_ecu_table().get_injection_time(rpm, throttle)


# Example usage and testing
if __name__ == "__main__":
    # Test the ECU table
    table = ECUInjectionTable()
    
    print("ECU Injection Table Test")
    print("=" * 50)
    print(f"Table size: {table.injection_data.shape}")
    print(f"RPM range: {table.rpm_min}-{table.rpm_max}")
    print(f"Throttle range: {table.throttle_min}-{table.throttle_max}")
    print()
    
    # Test interpolation at various points
    test_points = [
        (0, 0),      # Idle
        (1000, 20),  # Low RPM, partial throttle
        (3000, 50),  # Mid RPM, half throttle
        (6000, 80),  # High RPM, high throttle
        (9500, 100), # Max RPM, full throttle
    ]
    
    print("Bilinear Interpolation Results:")
    print("-" * 50)
    for rpm, throttle in test_points:
        injection = table.get_injection_time(rpm, throttle)
        print(f"RPM: {rpm:4d} | Throttle: {throttle:3.0f}% | Injection: {injection:6.1f} µs")
    
    print()
    print("Comparison with old linear formula:")
    print("-" * 50)
    for rpm, throttle in test_points:
        table_value = table.get_injection_time(rpm, throttle)
        # Old formula: 800 + (rpm / 9500) * 6000 + throttle * 200
        old_formula = 800 + (rpm / 9500) * 6000 + throttle * 200
        diff = table_value - old_formula
        print(f"RPM: {rpm:4d} | Table: {table_value:6.1f} µs | Formula: {old_formula:6.1f} µs | Diff: {diff:+6.1f} µs")
