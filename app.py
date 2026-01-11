"""
Application Entry Point
Launches the GUI application for Formula Student Telemetry System.

Usage:
    python app.py
"""

import sys
from gui.main_window import MainWindow
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
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
