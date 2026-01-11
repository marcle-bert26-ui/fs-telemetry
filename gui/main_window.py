"""
Main Application Window - Entry point for the GUI application.
Provides interface for both LIVE and REPLAY modes.
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QStatusBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from .live_mode_widget import LiveModeWidget
from .replay_mode_widget import ReplayModeWidget


class MainWindow(QMainWindow):
    """
    Main application window with tab interface for LIVE and REPLAY modes.
    """
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self.setWindowTitle("Formula Student Telemetry System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set minimum size
        self.setMinimumSize(1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create header
        header = QWidget()
        header.setStyleSheet("background-color: #1e3a8a; padding: 20px;")
        header_layout = QVBoxLayout(header)
        
        title = QLabel("🏎️ Formula Student Telemetry System")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        
        subtitle = QLabel("Real-time data acquisition and analysis from Formula Student vehicle")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #93c5fd;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        layout.addWidget(header)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
            }
            QTabBar::tab {
                background-color: #f3f4f6;
                padding: 8px 20px;
                border: 1px solid #d1d5db;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1e3a8a;
                color: white;
            }
        """)
        
        # Create mode widgets
        self.live_widget = LiveModeWidget()
        self.replay_widget = ReplayModeWidget()
        
        # Add tabs
        self.tabs.addTab(self.live_widget, "🟢 LIVE MODE")
        self.tabs.addTab(self.replay_widget, "🔄 REPLAY MODE")
        
        layout.addWidget(self.tabs)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9fafb;
            }
            QWidget {
                background-color: #f9fafb;
            }
        """)
    
    def closeEvent(self, event):
        """Handle application close event."""
        # Stop any running processes
        if self.live_widget:
            self.live_widget.stop_acquisition()
        if self.replay_widget:
            self.replay_widget.stop_replay()
        
        event.accept()


def main():
    """Main entry point for the GUI application."""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
