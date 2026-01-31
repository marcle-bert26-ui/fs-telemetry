"""
GUI Application Entry Point
Launches the GUI application for Formula Student Telemetry System.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Formula Student Telemetry")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    
    # Show in fullscreen mode
    window.showFullScreen()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
