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
DEFAULT_CSV_FILE = "tests/circuit_loop_data.csv"  # Default file for simulation mode

# CSV Format
CSV_DELIMITER = ";"
CSV_HEADER = ["time_ms", "speed_kmh", "rpm", "throttle", "battery_temp", "g_force_lat", "g_force_long", "g_force_vert", "acceleration_x", "acceleration_y", "acceleration_z", "gps_latitude", "gps_longitude", "gps_altitude", "tire_temp_fl", "tire_temp_fr", "tire_temp_rl", "tire_temp_rr"]

# Telemetry Update Frequency
TELEMETRY_FREQUENCY_HZ = 50  # Adjust based on your Arduino sending frequency

# ============================================================================
