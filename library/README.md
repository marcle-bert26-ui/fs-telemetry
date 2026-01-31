# FS Telemetry Library Documentation

## 📚 Component Library

This directory contains detailed documentation for all major components of the FS Telemetry system.

## 🎯 Core Components

### 1. Temporal Analysis Widget
**File**: `src/temporal_analysis_widget.py`

**Purpose**: Main analysis interface with unified widget layout

**Key Features**:
- Vertical layout with 4 main components
- Synchronized cursor system
- Real-time data updates
- Auto-zoom integration

**Usage**:
```python
from temporal_analysis_widget import TemporalAnalysisWidget

widget = TemporalAnalysisWidget()
widget.update_data(telemetry_data)
```

---

### 2. Telemetry Charts
**File**: `src/telemetry_charts.py`

**Purpose**: Real-time telemetry data visualization

**Key Features**:
- Multiple chart types (Speed, RPM, G-forces, etc.)
- Auto-zoom controls
- Cursor synchronization
- Real-time updates

**Usage**:
```python
from telemetry_charts import TelemetryCharts

charts = TelemetryCharts()
charts.reset_auto_zoom()  # 2-minute window
charts.full_auto_zoom()  # Full auto-zoom
```

---

### 3. Spider Charts
**File**: `src/spider_charts.py`

**Purpose**: G-force visualization in radar/spider format

**Key Features**:
- Real-time G-force display
- Current G-forces tracking
- Statistics calculation
- Color-coded force vectors

**Usage**:
```python
from spider_charts import GForcesSpiderWidget

spider = GForcesSpiderWidget()
spider.update_data(telemetry_data)
```

---

### 4. Track Map
**File**: `src/temporal_analysis_widget.py` (CompactTrackMap class)

**Purpose**: GPS tracking and circuit visualization

**Key Features**:
- Real-time position tracking
- Trajectory visualization
- Auto-zoom integration
- GPS coordinate mapping

**Usage**:
```python
from temporal_analysis_widget import CompactTrackMap

track_map = CompactTrackMap()
track_map.update_data(telemetry_data)
track_map.enableAutoRange()
```

---

### 5. CSV Parser
**File**: `src/csv_parser.py`

**Purpose**: CSV data parsing and telemetry data handling

**Key Features**:
- Flexible CSV format support
- Data validation
- Error handling
- Telemetry data object creation

**Usage**:
```python
from csv_parser import parse_csv_line, TelemetryData

data = parse_csv_line(csv_line)
# or
telemetry = TelemetryData(time_ms=1000, speed=45.2, ...)
```

---

### 6. Replay Mode Widget
**File**: `src/replay_mode_widget.py`

**Purpose**: CSV data replay interface

**Key Features**:
- File selection
- Playback controls
- Temporal analysis integration
- Data synchronization

**Usage**:
```python
from replay_mode_widget import ReplayModeWidget

replay = ReplayModeWidget()
replay.load_csv_file("data.csv")
```

---

### 7. Live Mode Widget
**File**: `src/live_mode_widget.py`

**Purpose**: Real-time data acquisition interface

**Key Features**:
- Serial communication
- Real-time data display
- Data logging
- Live analysis

**Usage**:
```python
from live_mode_widget import LiveModeWidget

live = LiveModeWidget()
live.start_acquisition("COM3", 115200)
```

---

## 🔄 Data Flow

```
Arduino/Serial → CSV Parser → Telemetry Manager → Widgets
                                                    ↓
CSV File → CSV Parser → Telemetry Manager → Widgets
```

## 🎨 UI Components

### Layout Structure
- **50/50 Split**: Left panel (analysis) + Right panel (charts)
- **Vertical Layout**: G-forces → Temporal → Controls → Track Map
- **Synchronized Cursor**: Time-based positioning across all components

### Color Scheme
- **G-Forces**: Orange (#f59e0b)
- **Temporal**: Purple (#8b5cf6)
- **Controls**: Green (#22c55e)
- **Track Map**: Blue (#3b82f6)

## 📊 Data Formats

### TelemetryData Object
```python
class TelemetryData:
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

### CSV Format
```csv
time_ms,speed,rpm,throttle,battery_temp,g_force_lat,g_force_long,g_force_vert,latitude,longitude
1000,45.2,3500,65.5,23.4,0.12,0.05,0.98,45.1234,5.6789
```

## 🔧 Configuration

### Auto-Zoom Settings
- **2-minute window**: `reset_auto_zoom()`
- **Full auto-zoom**: `full_auto_zoom()`
- **Track map**: Integrated with chart auto-zoom

### Cursor Settings
- **Time-based**: 0 to duration in seconds
- **Mathematical mapping**: Time → Data index
- **Real-time updates**: All components synchronized

## 🚀 Performance

### Memory Management
- **Circular buffers**: Efficient data storage
- **Lazy loading**: Data loaded on demand
- **Garbage collection**: Automatic cleanup

### Update Rates
- **Real-time**: Up to 100Hz
- **UI updates**: 30-60Hz
- **Data logging**: Real-time to CSV

## 🧪 Testing

### Unit Tests
```bash
pytest tests/test_csv_parser.py
pytest tests/test_telemetry_manager.py
```

### Integration Tests
```bash
pytest tests/test_integration.py
```

### Sample Data
- **Location**: `tests/enhanced_sample_data.csv`
- **Duration**: ~120 seconds
- **Parameters**: Full telemetry dataset

## 🔍 Debugging

### Common Issues
1. **Cursor not synchronized**: Check data source consistency
2. **Track map not updating**: Verify GPS data availability
3. **Auto-zoom not working**: Ensure data is loaded first

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 References

- [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
- [PyQtGraph Documentation](https://pyqtgraph.readthedocs.io/)
- [Python Serial Documentation](https://pyserial.readthedocs.io/)

---

*Last updated: January 2026*
