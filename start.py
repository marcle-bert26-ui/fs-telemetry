#!/usr/bin/env python3
"""
Simple launcher for Formula Student Telemetry
"""

import sys
import os

def main():
    """Launch the application."""
    
    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    try:
        # Import and run the GUI app
        from gui_app import main
        print("Starting Formula Student Telemetry...")
        main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Missing files. Please check your installation.")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
