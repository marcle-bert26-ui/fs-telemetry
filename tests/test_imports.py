#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_imports():
    """Test all critical imports."""
    
    print("Testing imports...")
    
    try:
        print("1. Importing gui_app.main...")
        from gui_app import main
        print("   ✅ gui_app.main - OK")
        
        print("2. Importing main_window.MainWindow...")
        from main_window import MainWindow
        print("   ✅ main_window.MainWindow - OK")
        
        print("3. Importing live_mode_widget.LiveModeWidget...")
        from live_mode_widget import LiveModeWidget
        print("   ✅ live_mode_widget.LiveModeWidget - OK")
        
        print("4. Importing telemetry_charts.TelemetryCharts...")
        from telemetry_charts import TelemetryCharts
        print("   ✅ telemetry_charts.TelemetryCharts - OK")
        
        print("5. Importing csv_parser...")
        from csv_parser import parse_csv_line, TelemetryData
        print("   ✅ csv_parser - OK")
        
        print("6. Importing telemetry_manager...")
        from telemetry_manager import TelemetryManager
        print("   ✅ telemetry_manager - OK")
        
        print("7. Importing PyQt5...")
        from PyQt5.QtWidgets import QApplication
        print("   ✅ PyQt5 - OK")
        
        print("\n🎉 All imports successful!")
        print("The application should launch correctly with: python app.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n✅ Ready to launch the application!")
    else:
        print("\n❌ Fix the import errors before launching.")
