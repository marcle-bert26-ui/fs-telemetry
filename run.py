#!/usr/bin/env python3
"""
Ultra-simple launcher for fs-telemetry
"""

import os
import subprocess
import sys

def main():
    """Run the application with the simplest approach."""
    
    # Change to src directory and run app.py
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    if os.path.exists(src_dir):
        print("Starting Formula Student Telemetry...")
        try:
            # Run app.py from src directory
            subprocess.run([sys.executable, 'app.py'], cwd=src_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running application: {e}")
        except FileNotFoundError:
            print("app.py not found in src directory")
    else:
        print("src directory not found")
        print("Please check your project structure")

if __name__ == "__main__":
    main()
