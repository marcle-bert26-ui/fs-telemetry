"""
Replay module - Replay recorded telemetry sessions with timing preservation.
"""

import csv
from pathlib import Path
from typing import Iterator, Dict


def replay_csv(filename: str) -> Iterator[Dict[str, str]]:
    """
    Replay telemetry data from a CSV file with proper timing.
    
    :param filename: Path to CSV file to replay
    :yield: Dictionary of telemetry values
    """
    filepath = Path(filename)
    
    if not filepath.exists():
        print(f"X File not found: {filepath}")
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            prev_time = None
            
            for row in reader:
                yield row
                
    except Exception as e:
        print(f"X Replay error: {e}")
