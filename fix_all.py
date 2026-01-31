#!/usr/bin/env python3
"""
Quick fix for all imports and structure.
"""

import os
import shutil
import glob

def main():
    """Quick fix function."""
    print("Fixing imports and structure...")
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Fix app.py
    app_content = '''"""
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

from app import main

if __name__ == "__main__":
    main()
'''
    
    with open(os.path.join(current_dir, 'app.py'), 'w') as f:
        f.write(app_content)
    print("Fixed: app.py")
    
    # 2. Fix imports in all src files
    src_dir = os.path.join(current_dir, 'src')
    if os.path.exists(src_dir):
        for filename in os.listdir(src_dir):
            if filename.endswith('.py'):
                filepath = os.path.join(src_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original = content
                    
                    # Fix all import patterns
                    content = content.replace('from src.', 'from ')
                    content = content.replace('from src/acquisition.', 'from ')
                    content = content.replace('from src/gui.', 'from ')
                    content = content.replace('from src/visualization.', 'from ')
                    content = content.replace('from src/parsing.', 'from ')
                    content = content.replace('from src/replay.', 'from ')
                    content = content.replace('from src/log_handlers.', 'from ')
                    content = content.replace('from data.', 'from ')
                    content = content.replace('from parsing.', 'from ')
                    content = content.replace('from gui.', 'from ')
                    content = content.replace('from visualization.', 'from ')
                    content = content.replace('from replay.', 'from ')
                    content = content.replace('from log_handlers.', 'from ')
                    content = content.replace('from acquisition.', 'from ')
                    content = content.replace('from .', 'from ')
                    content = content.replace('import config', 'import app_config as config')
                    
                    if content != original:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed imports: {filename}")
                        
                except Exception as e:
                    print(f"Error fixing {filename}: {e}")
    
    print("✅ All fixes complete!")
    print("Run: python app.py")

if __name__ == "__main__":
    main()
