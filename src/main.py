"""
🏎️ Formula Student Telemetry Application
Main orchestrator for live data acquisition and CSV replay.

This application provides:
- Live telemetry streaming from Arduino via serial
- Data logging to CSV files
- Real-time visualization
- Offline replay and analysis capability
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import app_config as config
from .serial_source import SerialSource
from .csv_source import CSVSource
from .csv_parser import parse_csv_line, TelemetryData
from .telemetry_manager import TelemetryManager
from .csv_logger import CSVLogger
from .console_display import ConsoleDisplay


def main_live():
    """
    Main loop for LIVE mode: Read from Arduino, log to CSV, display in real-time.
    """
    print("\n[GREEN] LIVE MODE - Reading from Arduino")
    print(f"Port: {config.SERIAL_PORT} | Baudrate: {config.SERIAL_BAUDRATE}\n")
    
    # Initialize components
    try:
        source = SerialSource(config.SERIAL_PORT, config.SERIAL_BAUDRATE)
    except Exception as e:
        print(f"Failed to start: {e}")
        return
    
    logger = CSVLogger()
    manager = TelemetryManager()
    display = ConsoleDisplay(update_interval=10)
    
    display.print_header()
    
    try:
        while True:
            # Read from Arduino
            line = source.read()
            
            if not line:
                continue
            
            # Parse the data
            data = parse_csv_line(line)
            if data is None:
                continue
            
            # Update manager
            manager.update(data)
            
            # Log to CSV
            logger.log(data)
            
            # Display
            display.update(data)
    
    except KeyboardInterrupt:
        print("\n\n[STOP] Acquisition stopped by user\n")
    
    finally:
        # Cleanup
        source.close()
        logger.close()
        display.print_footer(manager.get_stats())


def main_replay(csv_file: str):
    """
    Main loop for REPLAY mode: Read from CSV file, analyze, display.
    
    :param csv_file: Path to CSV file to replay
    """
    print(f"\n[REPLAY] REPLAY MODE - Reading from {csv_file}\n")
    
    # Initialize components
    try:
        source = CSVSource(csv_file)
    except Exception as e:
        print(f"Failed to start: {e}")
        return
    
    manager = TelemetryManager()
    display = ConsoleDisplay(update_interval=5)
    
    display.print_header()
    
    try:
        # Skip header line
        source.read()
        
        while True:
            line = source.read()
            
            if not line:
                break
            
            # Parse the data
            data = parse_csv_line(line)
            if data is None:
                continue
            
            # Update manager
            manager.update(data)
            
            # Display
            display.update(data)
    
    except Exception as e:
        print(f"Error during replay: {e}")
    
    finally:
        source.close()
        display.print_footer(manager.get_stats())


def main():
    """
    Main entry point - Routes to LIVE or REPLAY based on configuration.
    """
    if config.SIMULATION_MODE:
        # In simulation mode, ask which CSV file to replay
        csv_file = input(f"Enter CSV file path to replay (or press Enter for default: {config.DEFAULT_CSV_FILE}): ").strip()
        if not csv_file:
            # Default to the configured file
            csv_file = config.DEFAULT_CSV_FILE
        main_replay(csv_file)
    else:
        # Live mode - read from Arduino
        main_live()


if __name__ == "__main__":
    main()
