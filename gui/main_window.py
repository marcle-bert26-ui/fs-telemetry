"""
Main Application Window - Entry point for the GUI application.
Provides interface for both LIVE and REPLAY modes.
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QStatusBar, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QKeySequence

from .live_mode_widget import LiveModeWidget
from .replay_mode_widget import ReplayModeWidget


class MainWindow(QMainWindow):
    """
    Main application window with tab interface for LIVE and REPLAY modes.
    """
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self.setWindowTitle("EIGSI Formula Student Telemetry System")
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
        header.setStyleSheet("background-color: #1e3a8a; padding: 10px;")
        header_layout = QVBoxLayout(header)
        
        title = QLabel("🏎️ Formula Student Telemetry")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        
        subtitle = QLabel("Real-time data acquisition and analysis from Formula Student vehicle")
        subtitle_font = QFont()
        subtitle_font.setPointSize(9)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #93c5fd;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setContentsMargins(15, 8, 15, 8)
        
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
        self.status_bar.showMessage("Ready - Press ESC to exit fullscreen")
        
        # Add fullscreen toggle action
        self.toggle_fullscreen_action = QAction("Toggle Fullscreen", self)
        self.toggle_fullscreen_action.setShortcut(QKeySequence("F11"))
        self.toggle_fullscreen_action.triggered.connect(self.toggle_fullscreen)
        self.addAction(self.toggle_fullscreen_action)
        
        # Add exit action
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut(QKeySequence("Escape"))
        self.exit_action.triggered.connect(self.close)
        self.addAction(self.exit_action)
        
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
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and normal mode."""
        if self.isFullScreen():
            self.showNormal()
            self.status_bar.showMessage("Ready - Press F11 for fullscreen")
        else:
            self.showFullScreen()
            self.status_bar.showMessage("Ready - Press ESC to exit fullscreen")


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
