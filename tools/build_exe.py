#!/usr/bin/env python3
"""
Build script to create a standalone EXE for Formula Student Telemetry
"""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Build standalone EXE using PyInstaller."""
    print("🔨 Building Formula Student Telemetry EXE...\n")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "FormulaTelementry",
        "--icon=NONE",
        "--add-data", "tests/sample_data.csv:.",
        "--add-data", "stubs:stubs",
        "--hidden-import=PyQt5",
        "--hidden-import=pyserial",
        "--distpath", "./dist",
        "--buildpath", "./build",
        "--specpath", "./build",
        "app.py"
    ]
    
    print("Running PyInstaller...\n")
    print(" ".join(cmd))
    print("\n" + "="*70 + "\n")
    
    result = subprocess.run(cmd, cwd=str(Path(__file__).parent))
    
    if result.returncode == 0:
        exe_path = Path(__file__).parent / "dist" / "FormulaTelementry.exe"
        print("\n" + "="*70)
        print(f"\n✅ SUCCESS! EXE created at:\n   {exe_path}\n")
        print("You can now:")
        print("  • Double-click FormulaTelementry.exe to run")
        print("  • Share it with others (it's self-contained!)")
        print("  • Create a desktop shortcut\n")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
