"""
Application Entry Point
Launches the GUI application for Formula Student Telemetry System.

Usage:
    python app.py
"""

import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from gui_app import main

if __name__ == "__main__":
    main()
