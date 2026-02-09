#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_imports():
    """Test all critical imports."""
    
    print("Testing imports...")
    
    try:
        print("1. Importing app...")
        from src import app
        print("   OK: app")
        
        print("2. Importing temporal_analysis_widget...")
        from src.temporal_analysis_widget import TemporalAnalysisWidget
        print("   OK: temporal_analysis_widget")
        
        print("3. Importing live_mode_widget...")
        from src.live_mode_widget import LiveModeWidget
        print("   OK: live_mode_widget")
        
        print("4. Importing telemetry_charts...")
        from src.telemetry_charts import TelemetryCharts
        print("   OK: telemetry_charts")
        
        print("5. Importing csv_parser...")
        from src.csv_parser import parse_csv_line, TelemetryData
        print("   OK: csv_parser")
        
        print("6. Importing telemetry_manager...")
        from src.telemetry_manager import TelemetryManager
        print("   OK: telemetry_manager")
        
        print("7. Importing PyQt5...")
        from PyQt5.QtWidgets import QApplication
        print("   OK: PyQt5")
        
        print("\nAll imports successful!")
        print("The application should launch correctly with: py app.py")
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Other error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\nReady to launch the application!")
    else:
        print("\nFix the import errors before launching.")
