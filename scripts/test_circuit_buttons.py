#!/usr/bin/env python3
"""
Test script pour vérifier les boutons Circuit Loop et Full Circuit.
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.file_selector_widget import FileSelectorWidget

def test_circuit_buttons():
    """Test the circuit loop buttons."""
    print("Testing Circuit Loop and Full Circuit buttons...")
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Create file selector widget
    widget = FileSelectorWidget()
    
    # Show widget
    widget.show()
    widget.setWindowTitle("Circuit Buttons Test")
    
    print("Circuit buttons test:")
    print("- Check if 'Circuit Loop' button loads circuit_loop_data.csv")
    print("- Check if 'Full Circuit' button loads full_circuit_data.csv")
    print("- Verify files exist in tests/fixtures/")
    
    # Auto-close after 10 seconds for testing
    QTimer.singleShot(10000, app.quit)
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_circuit_buttons()
