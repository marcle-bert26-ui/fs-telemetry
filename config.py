# ============================================================================
# Configuration File for Formula Student Telemetry Application
# ============================================================================

# Serial Configuration
SERIAL_PORT = "COM3"  # Change to your Arduino port
SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 1

# Data Logging
LOG_DIRECTORY = "data_logs"
LOG_FILENAME_PREFIX = "run"

# Simulation / Replay Mode
SIMULATION_MODE = True  # Set to True to replay from CSV instead of reading Arduino

# CSV Format
CSV_DELIMITER = ";"
CSV_HEADER = ["time_ms", "speed_kmh", "rpm", "throttle", "battery_temp"]

# Telemetry Update Frequency
TELEMETRY_FREQUENCY_HZ = 50  # Adjust based on your Arduino sending frequency

# ============================================================================
