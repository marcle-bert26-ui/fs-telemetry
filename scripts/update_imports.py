#!/usr/bin/env python3
"""
Script to update imports after reorganization.
Updates all Python files to use the new module structure.
"""

import os
import re
from pathlib import Path

# Mapping of old imports to new imports
IMPORT_MAPPING = {
    # Core modules
    'from src.core.telemetry_manager import': 'from src.core.telemetry_manager import',
    'from src.core.telemetry_source import': 'from src.core.telemetry_source import',
    'import src.core.telemetry_manager': 'import src.core.telemetry_manager',
    'import src.core.telemetry_source': 'import src.core.telemetry_source',
    
    # Data modules
    'from src.data.csv_parser import': 'from src.data.csv_parser import',
    'from src.data.csv_logger import': 'from src.data.csv_logger import',
    'from src.csv_source import': 'from src.csv_source import',
    'import src.data.csv_parser': 'import src.data.csv_parser',
    'import src.data.csv_logger': 'import src.data.csv_logger',
    'import src.data.csv_source': 'import src.data.csv_source',
    
    # Sources
    'from src.sources.serial_source import': 'from src.sources.serial_source import',
    'import src.sources.serial_source': 'import src.sources.serial_source',
    
    # GUI modules
    'from src.gui.main_window import': 'from src.gui.main_window import',
    'from src.gui.live_mode_widget import': 'from src.gui.live_mode_widget import',
    'from src.gui.replay_mode_widget import': 'from src.gui.replay_mode_widget import',
    'from src.gui.temporal_analysis_widget import': 'from src.gui.temporal_analysis_widget import',
    'from src.gui.file_selector_widget import': 'from src.gui.file_selector_widget import',
    'import src.gui.main_window': 'import src.gui.main_window',
    'import src.gui.live_mode_widget': 'import src.gui.live_mode_widget',
    'import src.gui.replay_mode_widget': 'import src.gui.replay_mode_widget',
    'import src.gui.temporal_analysis_widget': 'import src.gui.temporal_analysis_widget',
    'import src.gui.file_selector_widget': 'import src.gui.file_selector_widget',
    
    # Visualization modules
    'from src.visualization.telemetry_charts import': 'from src.visualization.telemetry_charts import',
    'from src.visualization.spider_charts import': 'from src.visualization.spider_charts import',
    'import src.visualization.telemetry_charts': 'import src.visualization.telemetry_charts',
    'import src.visualization.spider_charts': 'import src.visualization.spider_charts',
    
    # Utils modules
    'from src.utils.console_display import': 'from src.utils.console_display import',
    'from src.utils.console_handler import': 'from src.utils.console_handler import',
    'from src.utils.replay_thread import': 'from src.utils.replay_thread import',
    'import src.utils.console_display': 'import src.utils.console_display',
    'import src.utils.console_handler': 'import src.utils.console_handler',
    'import src.utils.replay_thread': 'import src.utils.replay_thread',
}

def update_file_imports(file_path):
    """Update imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply import mappings
        for old_import, new_import in IMPORT_MAPPING.items():
            content = content.replace(old_import, new_import)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated imports in: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update all Python files in the project."""
    print("Updating imports after reorganization...")
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'build', 'dist']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    print(f"Found {len(python_files)} Python files")
    
    updated_count = 0
    for file_path in python_files:
        if update_file_imports(file_path):
            updated_count += 1
    
    print(f"\nReorganization complete!")
    print(f"Updated {updated_count} files")
    print(f"Total files processed: {len(python_files)}")

if __name__ == "__main__":
    main()
