#!/usr/bin/env python3
"""
Script to fix relative imports in GUI modules after reorganization.
"""

import os
import re
from pathlib import Path

def fix_relative_imports(file_path):
    """Fix relative imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix relative imports for GUI modules
        gui_imports = {
            'from live_mode_widget import': 'from .live_mode_widget import',
            'from replay_mode_widget import': 'from .replay_mode_widget import', 
            'from temporal_analysis_widget import': 'from .temporal_analysis_widget import',
            'from file_selector_widget import': 'from .file_selector_widget import',
            'from telemetry_charts import': 'from ..visualization.telemetry_charts import',
            'from spider_charts import': 'from ..visualization.spider_charts import',
            'from telemetry_manager import': 'from ..core.telemetry_manager import',
            'from csv_parser import': 'from ..data.csv_parser import',
            'from csv_logger import': 'from ..data.csv_logger import',
            'from console_display import': 'from ..utils.console_display import',
            'from replay_thread import': 'from ..utils.replay_thread import',
        }
        
        # Apply import mappings
        for old_import, new_import in gui_imports.items():
            content = content.replace(old_import, new_import)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all Python files in GUI and visualization directories."""
    print("Fixing relative imports after reorganization...")
    
    # Target directories
    target_dirs = ['src/gui', 'src/visualization']
    
    python_files = []
    for target_dir in target_dirs:
        if os.path.exists(target_dir):
            for root, dirs, files in os.walk(target_dir):
                # Skip __pycache__
                dirs[:] = [d for d in dirs if d != '__pycache__']
                
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(Path(root) / file)
    
    print(f"Found {len(python_files)} Python files to fix")
    
    fixed_count = 0
    for file_path in python_files:
        if fix_relative_imports(file_path):
            fixed_count += 1
    
    print(f"\nImport fixing complete!")
    print(f"Fixed {fixed_count} files")
    print(f"Total files processed: {len(python_files)}")

if __name__ == "__main__":
    main()
