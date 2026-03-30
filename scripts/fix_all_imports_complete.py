#!/usr/bin/env python3
"""
Complete script to fix all imports after reorganization.
"""

import os
import re
from pathlib import Path

def fix_all_imports(file_path):
    """Fix all imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Comprehensive import mappings
        import_mappings = {
            # Core modules
            'from telemetry_manager import': 'from ..core.telemetry_manager import',
            'from telemetry_source import': 'from ..core.telemetry_source import',
            'import telemetry_manager': 'import ..core.telemetry_manager',
            'import telemetry_source': 'import ..core.telemetry_source',
            
            # Data modules
            'from csv_parser import': 'from ..data.csv_parser import',
            'from csv_logger import': 'from ..data.csv_logger import',
            'from csv_source import': 'from ..data.csv_source import',
            'import csv_parser': 'import ..data.csv_parser',
            'import csv_logger': 'import ..data.csv_logger',
            'import csv_source': 'import ..data.csv_source',
            
            # Sources
            'from serial_source import': 'from ..sources.serial_source import',
            'import serial_source': 'import ..sources.serial_source',
            
            # GUI modules (same level)
            'from live_mode_widget import': 'from .live_mode_widget import',
            'from replay_mode_widget import': 'from .replay_mode_widget import',
            'from temporal_analysis_widget import': 'from .temporal_analysis_widget import',
            'from file_selector_widget import': 'from .file_selector_widget import',
            'from main_window import': 'from .main_window import',
            
            # Visualization modules
            'from telemetry_charts import': 'from ..visualization.telemetry_charts import',
            'from spider_charts import': 'from ..visualization.spider_charts import',
            'import telemetry_charts': 'import ..visualization.telemetry_charts',
            'import spider_charts': 'import ..visualization.spider_charts',
            
            # Utils modules
            'from console_display import': 'from ..utils.console_display import',
            'from console_handler import': 'from ..utils.console_handler import',
            'from replay_thread import': 'from ..utils.replay_thread import',
            'import console_display': 'import ..utils.console_display',
            'import console_handler': 'import ..utils.console_handler',
            'import replay_thread': 'import ..utils.replay_thread',
        }
        
        # Apply import mappings
        for old_import, new_import in import_mappings.items():
            content = content.replace(old_import, new_import)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all Python files in src directory."""
    print("Fixing all imports after reorganization...")
    
    # Target all Python files in src directory
    python_files = []
    src_dir = Path('src')
    
    if src_dir.exists():
        for root, dirs, files in os.walk(src_dir):
            # Skip __pycache__
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    python_files.append(Path(root) / file)
    
    print(f"Found {len(python_files)} Python files to fix")
    
    fixed_count = 0
    for file_path in python_files:
        if fix_all_imports(file_path):
            fixed_count += 1
    
    print(f"\nImport fixing complete!")
    print(f"Fixed {fixed_count} files")
    print(f"Total files processed: {len(python_files)}")

if __name__ == "__main__":
    main()
