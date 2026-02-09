#!/usr/bin/env python3
"""
Simple test to verify CI environment setup
"""

import sys
import os

def test_ci_environment():
    """Test that CI environment is properly configured."""
    print("Testing CI Environment Setup")
    print("=" * 50)
    
    # Test basic imports
    try:
        print("1. Testing basic imports...")
        import pytest
        print("   pytest imported successfully")
    except ImportError as e:
        print(f"   pytest import failed: {e}")
        return False
    
    # Test numpy import
    try:
        import numpy as np
        print("   numpy imported successfully")
        # Test basic numpy functionality
        arr = np.array([1, 2, 3])
        assert arr.mean() == 2.0
        print("   numpy functionality works")
    except ImportError as e:
        print(f"   numpy import failed: {e}")
        return False
    except Exception as e:
        print(f"   numpy functionality failed: {e}")
        return False
    
    # Test CSV parser import
    try:
        sys.path.insert(0, 'src')
        from src.csv_parser import TelemetryData, CSV_HEADER
        print("   csv_parser imported successfully")
        
        # Test TelemetryData creation
        data = TelemetryData(
            time_ms=1000, speed=50.0, rpm=5000, throttle=75.0, battery_temp=60.0,
            g_force_lat=0.0, g_force_long=0.0, g_force_vert=1.0,
            acceleration_x=0.0, acceleration_y=0.0, acceleration_z=0.0,
            gps_latitude=48.8566, gps_longitude=2.3522, gps_altitude=100.0,
            tire_temp_fl=25.0, tire_temp_fr=25.0, tire_temp_rl=25.0, tire_temp_rr=25.0
        )
        print("   TelemetryData creation works")
        
        # Test CSV_HEADER
        assert len(CSV_HEADER) == 18
        print("   CSV_HEADER has 18 columns")
        
    except ImportError as e:
        print(f"   csv_parser import failed: {e}")
        return False
    except Exception as e:
        print(f"   csv_parser functionality failed: {e}")
        return False
    
    # Test telemetry manager
    try:
        from src.telemetry_manager import TelemetryManager
        manager = TelemetryManager()
        print("   TelemetryManager imported and created")
        
        # Test basic functionality
        manager.update(data)
        assert manager.current == data
        print("   TelemetryManager basic functionality works")
        
    except ImportError as e:
        print(f"   telemetry_manager import failed: {e}")
        return False
    except Exception as e:
        print(f"   telemetry_manager functionality failed: {e}")
        return False
    
    print("=" * 50)
    print("All CI Environment Tests Passed!")
    return True

if __name__ == "__main__":
    success = test_ci_environment()
    sys.exit(0 if success else 1)
