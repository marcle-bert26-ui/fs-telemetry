#!/usr/bin/env python3
"""
Clean up old CSV log files, keeping only the most recent one.
"""

import os
import glob
from datetime import datetime

def cleanup_old_logs():
    """Clean up old CSV log files, keeping only the most recent one."""
    
    # Get the data_logs directory
    data_logs_dir = os.path.join(os.path.dirname(__file__), 'data_logs')
    
    if not os.path.exists(data_logs_dir):
        print("data_logs directory not found")
        return
    
    # Find all CSV files
    csv_files = glob.glob(os.path.join(data_logs_dir, '*.csv'))
    
    if not csv_files:
        print("No CSV files found")
        return
    
    # Sort files by modification time (newest first)
    csv_files.sort(key=os.path.getmtime, reverse=True)
    
    # Keep the most recent file, delete the rest
    if len(csv_files) > 1:
        print(f"Found {len(csv_files)} CSV files")
        print(f"Keeping: {os.path.basename(csv_files[0])}")
        
        deleted_count = 0
        for csv_file in csv_files[1:]:  # Skip the first (newest) file
            try:
                os.remove(csv_file)
                print(f"Deleted: {os.path.basename(csv_file)}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {csv_file}: {e}")
        
        print(f"Cleanup complete. Deleted {deleted_count} old files.")
    else:
        print(f"Only one CSV file found: {os.path.basename(csv_files[0])}")

if __name__ == "__main__":
    cleanup_old_logs()
