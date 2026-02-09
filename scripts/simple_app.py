"""
Simple Application Entry Point
"""

import sys
import os

# Simple approach - add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Try to import and run
try:
    from src.app import main
    main()
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative approach...")
    
    # Alternative: run directly
    try:
        os.chdir('src')
        from app import main
        main()
    except Exception as e2:
        print(f"Alternative failed: {e2}")
        print("Please check your file structure.")
