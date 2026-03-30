#!/usr/bin/env python3
"""
Script final pour mettre à jour tous les imports après réorganisation.
"""

import os
import re
from pathlib import Path

def fix_imports_comprehensive(file_path):
    """Fix all imports in a single file comprehensively."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Import mappings for all possible patterns
        import_mappings = {
            # Absolute imports from src
            'from src.core.telemetry_manager import': 'from src.core.telemetry_manager import',
            'from src.core.telemetry_source import': 'from src.core.telemetry_source import',
            'from src.data.csv_parser import': 'from src.data.csv_parser import',
            'from src.data.csv_logger import': 'from src.data.csv_logger import',
            'from src.data.csv_source import': 'from src.data.csv_source import',
            'from src.sources.serial_source import': 'from src.sources.serial_source import',
            'from src.gui.main_window import': 'from src.gui.main_window import',
            'from src.gui.live_mode_widget import': 'from src.gui.live_mode_widget import',
            'from src.gui.replay_mode_widget import': 'from src.gui.replay_mode_widget import',
            'from src.gui.temporal_analysis_widget import': 'from src.gui.temporal_analysis_widget import',
            'from src.gui.file_selector_widget import': 'from src.gui.file_selector_widget import',
            'from src.visualization.telemetry_charts import': 'from src.visualization.telemetry_charts import',
            'from src.visualization.spider_charts import': 'from src.visualization.spider_charts import',
            'from src.utils.console_display import': 'from src.utils.console_display import',
            'from src.utils.console_handler import': 'from src.utils.console_handler import',
            'from src.utils.replay_thread import': 'from src.utils.replay_thread import',
            
            # Relative imports that need fixing
            'from telemetry_manager import': 'from ..core.telemetry_manager import',
            'from telemetry_source import': 'from ..core.telemetry_source import',
            'from csv_parser import': 'from ..data.csv_parser import',
            'from csv_logger import': 'from ..data.csv_logger import',
            'from csv_source import': 'from ..data.csv_source import',
            'from serial_source import': 'from ..sources.serial_source import',
            'from main_window import': 'from .main_window import',
            'from live_mode_widget import': 'from .live_mode_widget import',
            'from replay_mode_widget import': 'from .replay_mode_widget import',
            'from temporal_analysis_widget import': 'from .temporal_analysis_widget import',
            'from file_selector_widget import': 'from .file_selector_widget import',
            'from telemetry_charts import': 'from ..visualization.telemetry_charts import',
            'from spider_charts import': 'from ..visualization.spider_charts import',
            'from console_display import': 'from ..utils.console_display import',
            'from console_handler import': 'from ..utils.console_handler import',
            'from replay_thread import': 'from ..utils.replay_thread import',
        }
        
        # Apply import mappings
        changes_made = False
        for old_import, new_import in import_mappings.items():
            if old_import in content and new_import not in content:
                content = content.replace(old_import, new_import)
                changes_made = True
                print(f"  Fixed: {old_import} -> {new_import}")
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Update all imports in the project."""
    print("Mise a jour complete de tous les imports...")
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'build', 'dist']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    print(f"Found {len(python_files)} Python files")
    
    updated_count = 0
    for file_path in python_files:
        if fix_imports_comprehensive(file_path):
            updated_count += 1
    
    print(f"\nMise a jour terminee!")
    print(f"Fichiers mis a jour: {updated_count}")
    print(f"Total fichiers traites: {len(python_files)}")
    
    if updated_count == 0:
        print("Tous les imports sont deja corrects!")

if __name__ == "__main__":
    main()
