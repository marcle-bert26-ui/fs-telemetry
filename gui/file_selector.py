"""
File Selector Widget
Provides CSV file selection with dropdown list and browse functionality.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import os
from pathlib import Path


class FileSelectorWidget(QWidget):
    """
    Widget for CSV file selection with dropdown and browse functionality.
    """
    
    file_selected = pyqtSignal(str)  # Emits selected file path
    
    def __init__(self, tests_directory="tests"):
        """Initialize file selector widget."""
        super().__init__()
        self.tests_directory = tests_directory
        self.current_file = None
        self.init_ui()
        self.refresh_file_list()
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("📁 Select CSV File")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #1e3a8a; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # File selection layout
        file_layout = QHBoxLayout()
        
        # Dropdown for file selection
        self.file_dropdown = QComboBox()
        self.file_dropdown.setMinimumWidth(400)
        self.file_dropdown.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #d1d5db;
                border-radius: 5px;
                background: white;
                font-size: 12px;
            }
            QComboBox:focus {
                border-color: #3b82f6;
            }
        """)
        self.file_dropdown.currentTextChanged.connect(self.on_file_selected)
        
        # Browse button
        self.browse_btn = QPushButton("📂 Browse...")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(QLabel("File:"))
        file_layout.addWidget(self.file_dropdown)
        file_layout.addWidget(self.browse_btn)
        
        layout.addLayout(file_layout)
        
        # Current file display
        self.file_display = QLabel("No file selected")
        self.file_display.setStyleSheet("""
            QLabel {
                background-color: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 5px;
                padding: 8px;
                font-family: monospace;
                font-size: 10px;
            }
        """)
        self.file_display.setWordWrap(True)
        layout.addWidget(self.file_display)
        
        # Quick access buttons
        quick_layout = QHBoxLayout()
        
        self.enhanced_btn = QPushButton("📊 Enhanced Data")
        self.enhanced_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.enhanced_btn.clicked.connect(lambda: self.select_file("enhanced_sample_data.csv"))
        
        self.full_circuit_btn = QPushButton("🗺️ Full Circuit")
        self.full_circuit_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        self.full_circuit_btn.clicked.connect(lambda: self.select_file("full_circuit_data.csv"))
        
        quick_layout.addWidget(self.enhanced_btn)
        quick_layout.addWidget(self.full_circuit_btn)
        quick_layout.addStretch()
        
        layout.addLayout(quick_layout)
        layout.addStretch()
    
    def refresh_file_list(self):
        """Refresh the list of available CSV files."""
        self.file_dropdown.clear()
        self.file_dropdown.addItem("Select a file...")
        
        try:
            if os.path.exists(self.tests_directory):
                csv_files = []
                for file in os.listdir(self.tests_directory):
                    if file.endswith('.csv'):
                        csv_files.append(file)
                
                csv_files.sort()
                for file in csv_files:
                    self.file_dropdown.addItem(file)
                    
                # Auto-select first file if available
                if csv_files and not self.current_file:
                    self.on_file_selected(csv_files[0])
                    
        except Exception as e:
            print(f"! Error refreshing file list: {e}")
    
    def on_file_selected(self, filename):
        """Handle file selection from dropdown."""
        if filename and filename != "Select a file...":
            file_path = os.path.join(self.tests_directory, filename)
            if os.path.exists(file_path):
                self.current_file = file_path
                self.file_display.setText(f"📄 {filename}")
                self.file_selected.emit(file_path)
    
    def select_file(self, filename):
        """Select a specific file."""
        file_path = os.path.join(self.tests_directory, filename)
        if os.path.exists(file_path):
            # Find and select in dropdown
            index = self.file_dropdown.findText(filename)
            if index >= 0:
                self.file_dropdown.setCurrentIndex(index)
            self.on_file_selected(filename)
    
    def browse_file(self):
        """Open file dialog to select CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            self.tests_directory,
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            # Copy to tests directory if not already there
            if not file_path.startswith(self.tests_directory):
                import shutil
                try:
                    os.makedirs(self.tests_directory, exist_ok=True)
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(self.tests_directory, filename)
                    shutil.copy2(file_path, dest_path)
                    self.refresh_file_list()
                    self.select_file(filename)
                except Exception as e:
                    print(f"! Error copying file: {e}")
            else:
                filename = os.path.basename(file_path)
                self.select_file(filename)
    
    def get_current_file(self):
        """Get currently selected file path."""
        return self.current_file
