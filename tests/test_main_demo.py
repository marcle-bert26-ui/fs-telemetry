"""
Demo test to simulate and display main.py execution.
Tests both LIVE and REPLAY modes with mock data.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import csv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import app_config as config
from src.csv_parser import parse_csv_line, TelemetryData
from src.telemetry_manager import TelemetryManager
from src.csv_logger import CSVLogger
from src.csv_source import CSVSource


def test_replay_mode_demo():
    """
    Demo: Test REPLAY mode with sample CSV file.
    Shows how the system reads and processes recorded telemetry data.
    """
    print("\n" + "="*70)
    print("📊 DEMO: REPLAY MODE - Processing Sample Telemetry Data")
    print("="*70)
    
    # Create temporary CSV with sample data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        csv_file = f.name
        # Write header
        f.write('timestamp;speed;rpm;throttle;battery_temp\n')
        # Write sample data with semicolon separator
        sample_data = [
            '100;10.5;2000;25;35.2\n',
            '200;15.3;2500;40;35.5\n',
            '300;22.1;3200;60;36.1\n',
            '400;28.7;3800;80;36.8\n',
            '500;32.5;4200;100;37.2\n',
        ]
        for row in sample_data:
            f.write(row)
    
    print(f"✓ Created sample CSV file: {csv_file}")
    print(f"✓ Sample contains 5 data points\n")
    
    # Process the CSV file
    try:
        source = CSVSource(csv_file)
        manager = TelemetryManager()
        
        # Skip header
        source.read()
        
        # Process each line
        print("Processing telemetry data:")
        print("-" * 70)
        data_count = 0
        
        while True:
            line = source.read()
            if not line:
                break
            
            data = parse_csv_line(line)
            if data is None:
                continue
            
            data_count += 1
            manager.update(data)
            
            # Display each record
            print(f"  #{data_count} | Speed: {data.speed:6.1f} km/h | "
                  f"RPM: {data.rpm:5.0f} | Throttle: {data.throttle:3.0f}% | "
                  f"Temp: {data.battery_temp:5.1f}°C")
        
        source.close()
        
        print("-" * 70)
        print(f"✓ Successfully processed {data_count} telemetry records\n")
        
        # Show statistics
        stats = manager.get_stats()
        print("📈 Session Statistics:")
        if stats:
            print(f"  Max Speed:    {stats.get('max_speed', 0):.1f} km/h")
            print(f"  Avg Speed:    {stats.get('avg_speed', 0):.1f} km/h")
            print(f"  Max RPM:      {stats.get('max_rpm', 0):.0f}")
            print(f"  Avg RPM:      {stats.get('avg_rpm', 0):.0f}")
            print(f"  Max Throttle: {stats.get('max_throttle', 0):.0f}%")
            print(f"  Data Points:  {stats.get('data_points', 0)}")
        else:
            print("  No data to display")
        
    finally:
        # Cleanup
        Path(csv_file).unlink()


def test_logger_demo():
    """
    Demo: Test CSV logging functionality.
    Shows how telemetry data is saved to CSV files.
    """
    print("\n" + "="*70)
    print("💾 DEMO: CSV LOGGING - Saving Telemetry Data")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Override log directory
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_dir
        
        try:
            print(f"✓ Log directory: {temp_dir}\n")
            
            # Create logger
            logger = CSVLogger()
            print(f"✓ Created logger: {logger.filepath.name}\n")
            
            # Log some sample data
            print("Logging telemetry data:")
            print("-" * 70)
            
            sample_data = [
                TelemetryData(100, 10.5, 2000, 25, 35.2),
                TelemetryData(200, 15.3, 2500, 40, 35.5),
                TelemetryData(300, 22.1, 3200, 60, 36.1),
                TelemetryData(400, 28.7, 3800, 80, 36.8),
                TelemetryData(500, 32.5, 4200, 100, 37.2),
            ]
            
            for i, data in enumerate(sample_data, 1):
                logger.log(data)
                print(f"  #{i} | Logged: {data}")
            
            logger.close()
            
            print("-" * 70)
            print(f"✓ Successfully logged {len(sample_data)} records\n")
            
            # Read back the file
            print("Reading back saved data:")
            print("-" * 70)
            
            with open(logger.filepath, 'r') as f:
                lines = f.readlines()
                print(f"  Header: {lines[0].strip()}")
                for i, line in enumerate(lines[1:], 1):
                    print(f"  Row {i}:  {line.strip()}")
            
            print("-" * 70)
            print(f"✓ File saved successfully: {logger.filepath.name}\n")
            
        finally:
            config.LOG_DIRECTORY = original_dir


def test_telemetry_manager_demo():
    """
    Demo: Test telemetry manager functionality.
    Shows how data is accumulated and statistics calculated.
    """
    print("\n" + "="*70)
    print("📊 DEMO: TELEMETRY MANAGER - Data Accumulation & Statistics")
    print("="*70)
    
    manager = TelemetryManager()
    print("✓ Initialized telemetry manager\n")
    
    # Add sample data
    sample_data = [
        TelemetryData(100, 10.5, 2000, 25, 35.2, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 48.8566, 2.3522, 100, 25, 25, 25, 25),
        TelemetryData(200, 15.3, 2500, 40, 35.5, 0.1, 0.2, 0.9, 0.1, 0.1, 0.1, 48.8561, 2.3523, 102, 26, 26, 26, 26),
        TelemetryData(300, 22.1, 3200, 60, 36.1, 0.2, 0.3, 0.8, 0.2, 0.2, 0.2, 48.8556, 2.3524, 105, 27, 27, 27, 27),
        TelemetryData(400, 28.7, 3800, 80, 36.8, 0.3, 0.4, 0.7, 0.3, 0.3, 0.3, 48.8551, 2.3525, 108, 28, 28, 28, 28),
        TelemetryData(500, 32.5, 4200, 100, 37.2, 0.4, 0.5, 0.6, 0.4, 0.4, 0.4, 48.8546, 2.3526, 110, 29, 29, 29, 29),
    ]
    
    print("Updating manager with data points:")
    print("-" * 70)
    
    for i, data in enumerate(sample_data, 1):
        manager.update(data)
        current = manager.get_current()
        print(f"  #{i} | Speed: {current.speed:6.1f} | RPM: {current.rpm:5.0f} | "
              f"Throttle: {current.throttle:3.0f}% | Temp: {current.battery_temp:5.1f}°C")
    
    print("-" * 70)
    
    # Show history
    history = manager.get_history()
    print(f"\n✓ History stored: {len(history)} records")
    
    # Show statistics
    stats = manager.get_stats()
    print("\n📈 Calculated Statistics:")
    print(f"  Count:        {stats['data_points']}")
    print(f"  Max Speed:    {stats['max_speed']:.1f} km/h")
    print(f"  Avg Speed:    {stats['avg_speed']:.1f} km/h")
    print(f"  Max RPM:      {stats['max_rpm']:.0f}")
    print(f"  Avg RPM:      {stats['avg_rpm']:.0f}")
    print(f"  Max Throttle: {stats['max_throttle']:.0f}%")
    print(f"  Max Temp:     {stats['max_temp']:.1f}°C")
    print(f"  Avg Temp:     {stats['avg_temp']:.1f}°C")
    print()


if __name__ == "__main__":
    print("\n" + "🏎️ " * 10)
    print("FORMULA STUDENT TELEMETRY - MAIN.PY DEMO TEST")
    print("🏎️ " * 10)
    
    # Run all demos
    test_telemetry_manager_demo()
    test_logger_demo()
    test_replay_mode_demo()
    
    print("\n" + "="*70)
    print("✅ All demos completed successfully!")
    print("="*70 + "\n")
