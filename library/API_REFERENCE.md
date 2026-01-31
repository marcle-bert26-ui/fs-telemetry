# Component API Reference

## TemporalAnalysisWidget

### Constructor
```python
TemporalAnalysisWidget()
```

### Key Methods
```python
def update_data(self, data: TelemetryData) -> None
    """Update widget with new telemetry data"""

def update_all_components(self, point_idx: int) -> None
    """Update all components to specified point index"""

def clear_data(self) -> None
    """Clear all data and reset widget"""

def set_parent(self, parent_widget) -> None
    """Set parent widget for data synchronization"""
```

### Signals
```python
data_sync_signal = pyqtSignal(object)  # Emitted when data is updated
```

---

## TelemetryCharts

### Constructor
```python
TelemetryCharts(parent=None)
```

### Key Methods
```python
def reset_auto_zoom(self) -> None
    """Reset zoom to show last 2 minutes of data"""

def full_auto_zoom(self) -> None
    """Enable full auto-zoom for all plots"""

def update_data(self, data: TelemetryData) -> None
    """Update charts with new telemetry data"""

def clear_data(self) -> None
    """Clear all chart data"""
```

### Data Attributes
```python
time_data: deque          # Time stamps
speed_data: deque         # Speed values
rpm_data: deque           # RPM values
throttle_data: deque     # Throttle values
battery_temp_data: deque # Temperature values
g_force_lat_data: deque  # Lateral G-force
g_force_long_data: deque # Longitudinal G-force
g_force_vert_data: deque # Vertical G-force
```

---

## GForcesSpiderWidget

### Constructor
```python
GForcesSpiderWidget(max_points=100)
```

### Key Methods
```python
def update_data(self, data: TelemetryData) -> None
    """Update spider chart with new G-force data"""

def update_position(self, position) -> None
    """Update chart based on track position"""

def clear_data(self) -> None
    """Clear all spider chart data"""

def update_statistics(self) -> None
    """Update G-force statistics display"""
```

### Signals
```python
current_data_changed = pyqtSignal('PyQt_PyObject')  # Emitted when data changes
```

---

## CompactTrackMap

### Constructor
```python
CompactTrackMap()
```

### Key Methods
```python
def update_data(self, data: TelemetryData) -> None
    """Update track map with new GPS data"""

def clear_data(self) -> None
    """Clear all track data"""

def enableAutoRange(self) -> None
    """Enable automatic zoom adjustment"""

def update_position(self, position) -> None
    """Update current position marker"""
```

### Signals
```python
position_changed = pyqtSignal(object)  # Emitted when position changes
```

---

## TelemetryData

### Constructor
```python
TelemetryData(time_ms=0, speed=0, rpm=0, throttle=0, battery_temp=0,
              g_force_lat=0, g_force_long=0, g_force_vert=0,
              latitude=0, longitude=0)
```

### Attributes
```python
time_ms: int           # Timestamp in milliseconds
speed: float           # Speed in km/h
rpm: int              # Engine RPM
throttle: float       # Throttle position (%)
battery_temp: float   # Battery temperature (°C)
g_force_lat: float    # Lateral G-force
g_force_long: float   # Longitudinal G-force
g_force_vert: float   # Vertical G-force
latitude: float       # GPS latitude
longitude: float      # GPS longitude
```

### Methods
```python
def __str__(self) -> str
    """Return formatted string representation"""

def to_dict(self) -> dict
    """Convert to dictionary format"""

def from_dict(cls, data: dict) -> 'TelemetryData'
    """Create from dictionary"""
```

---

## CSV Parser Functions

### parse_csv_line
```python
def parse_csv_line(line: str) -> TelemetryData
    """Parse a single CSV line into TelemetryData object"""
```

### parse_csv_file
```python
def parse_csv_file(filepath: str) -> List[TelemetryData]
    """Parse entire CSV file into list of TelemetryData objects"""
```

### validate_telemetry_data
```python
def validate_telemetry_data(data: TelemetryData) -> bool
    """Validate telemetry data for consistency"""
```

---

## ReplayModeWidget

### Constructor
```python
ReplayModeWidget()
```

### Key Methods
```python
def load_csv_file(self, filepath: str) -> None
    """Load CSV file for replay"""

def start_replay(self) -> None
    """Start data replay"""

def stop_replay(self) -> None
    """Stop data replay"""

def set_playback_speed(self, speed: float) -> None
    """Set playback speed multiplier"""
```

---

## LiveModeWidget

### Constructor
```python
LiveModeWidget()
```

### Key Methods
```python
def start_acquisition(self, port: str, baudrate: int) -> None
    """Start real-time data acquisition"""

def stop_acquisition(self) -> None
    """Stop data acquisition"""

def start_logging(self, filepath: str) -> None
    """Start data logging to CSV"""

def stop_logging(self) -> None
    """Stop data logging"""
```

---

## TelemetryManager

### Constructor
```python
TelemetryManager()
```

### Key Methods
```python
def add_data(self, data: TelemetryData) -> None
    """Add new telemetry data"""

def get_latest_data(self) -> TelemetryData
    """Get most recent telemetry data"""

def get_data_range(self, start_idx: int, end_idx: int) -> List[TelemetryData]
    """Get data in specified range"""

def clear_data(self) -> None
    """Clear all stored data"""
```

---

## Usage Examples

### Basic Widget Setup
```python
from PyQt5.QtWidgets import QApplication
from temporal_analysis_widget import TemporalAnalysisWidget
from telemetry_charts import TelemetryCharts

app = QApplication([])

# Create widgets
temporal_widget = TemporalAnalysisWidget()
charts = TelemetryCharts()

# Set up parent relationship
temporal_widget.set_parent(parent_widget)

# Connect signals
temporal_widget.data_sync_signal.connect(charts.update_data)
```

### Data Processing
```python
from csv_parser import parse_csv_file

# Load CSV data
data_list = parse_csv_file("telemetry_data.csv")

# Update widgets
for data in data_list:
    temporal_widget.update_data(data)
    charts.update_data(data)
```

### Real-time Acquisition
```python
from live_mode_widget import LiveModeWidget

# Create live widget
live_widget = LiveModeWidget()

# Start acquisition
live_widget.start_acquisition("COM3", 115200)
live_widget.start_logging("live_data.csv")
```

### Replay Analysis
```python
from replay_mode_widget import ReplayModeWidget

# Create replay widget
replay_widget = ReplayModeWidget()

# Load and start replay
replay_widget.load_csv_file("recorded_data.csv")
replay_widget.start_replay()
```

---

*API Reference v1.0 - January 2026*
