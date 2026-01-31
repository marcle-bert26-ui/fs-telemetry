# EIGSI Formula Student Telemetry System

🏎️ **Advanced real-time telemetry data acquisition and analysis application for EIGSI Formula Student vehicles with GPS tracking, G-force visualization, and circuit mapping.**

[![Tests](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml/badge.svg)](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Language** • [English](docs/README_EN.md) | [Français](docs/README_FR.md)

---

## 🚀 Get Started in 3 Steps

### 1. Clone & Setup
```bash
git clone https://github.com/marcle-bert26-ui/fs-telemetry.git
cd fs-telemetry
python -m venv venv
```

### 2. Activate & Install
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch
```bash
py app.py          # GUI mode (LIVE/REPLAY) - Recommended
py main.py         # CLI mode (console output)
```

---

## 📋 Features

### 🎯 Core Telemetry
- **Real-time data acquisition** from Arduino/serial sources
- **CSV data replay** with full temporal analysis
- **Multi-parameter monitoring**: Speed, RPM, Throttle, Temperature, G-forces
- **GPS tracking** with circuit mapping
- **Data logging** to CSV files

### 📊 Visualization
- **Interactive temporal graphs** with cursor synchronization
- **Spider chart** for G-force analysis
- **Track map** with real-time position tracking
- **Real-time charts** with auto-zoom capabilities
- **Current data display** with live updates

### 🎮 User Interface
- **Unified widget layout** with vertical organization
- **Synchronized cursor** across all visualizations
- **Auto-zoom controls** (2-minute window, full auto)
- **Responsive design** with 50/50 layout split
- **Dark theme** with modern styling

---

## 📁 Project Structure

```
fs-telemetry/
├── src/                    # Source code
│   ├── temporal_analysis_widget.py    # Main analysis widget
│   ├── telemetry_charts.py            # Real-time charts
│   ├── spider_charts.py               # G-force spider chart
│   ├── replay_mode_widget.py          # Replay interface
│   ├── live_mode_widget.py            # Live acquisition
│   ├── csv_parser.py                  # CSV data parsing
│   └── telemetry_manager.py           # Data management
├── tests/                  # Test files & sample data
│   ├── enhanced_sample_data.csv      # Sample telemetry data
│   └── test_*.py                      # Unit tests
├── tools/                  # Utility scripts
│   ├── build_exe.py                   # Executable builder
│   └── cleanup_logs.py                # Log management
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
└── app.py                  # Main application entry
```

---

## 🎯 Key Components

### Temporal Analysis Widget
- **Vertical layout** with 4 main components:
  1. **G-Forces Spider Chart** - Real-time force visualization
  2. **Temporal Graphs** - Speed, RPM, G-forces over time
  3. **Data Controls** - Cursor and range selection
  4. **Track Map** - GPS position and trajectory

### Synchronized Cursor System
- **Time-based cursor** (0 to duration in seconds)
- **Mathematical mapping** to data indices
- **Real-time updates** across all visualizations
- **Auto-follow mode** during data loading

### Chart Integration
- **Left panel**: Unified analysis widgets (50% width)
- **Right panel**: Detailed telemetry charts (50% width)
- **Auto-zoom**: Synchronized across track map and charts
- **Cursor points**: Visual indicators on all graphs

---

## 📊 Data Format

### Supported Parameters
- **Time**: Timestamp in milliseconds
- **Speed**: Vehicle speed in km/h
- **RPM**: Engine revolutions per minute
- **Throttle**: Accelerator pedal position (%)
- **Temperature**: Battery temperature (°C)
- **G-Forces**: Lateral, longitudinal, vertical (g)
- **GPS**: Latitude, longitude for track mapping

### CSV Structure
```csv
time_ms,speed,rpm,throttle,battery_temp,g_force_lat,g_force_long,g_force_vert,latitude,longitude
1000,45.2,3500,65.5,23.4,0.12,0.05,0.98,45.1234,5.6789
```

---

## 🔧 Configuration

### Serial Port Settings
- **Port**: Configurable COM port (Windows) or tty device (Linux)
- **Baud Rate**: 115200 (default, adjustable)
- **Data Format**: Arduino-compatible serial protocol

### Display Settings
- **Auto-zoom**: 2-minute window or full auto
- **Update Rate**: Real-time (10Hz recommended)
- **Theme**: Dark mode with color-coded parameters

---

## 🧪 Testing

### Run Tests
```bash
pytest tests/                    # Run all tests
pytest tests/test_csv_parser.py  # Test specific module
```

### Sample Data
- **Location**: `tests/enhanced_sample_data.csv`
- **Duration**: ~120 seconds of telemetry
- **Parameters**: Full telemetry dataset with GPS

---

## 📈 Performance

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum
- **Storage**: 100MB for application + data
- **Display**: 1024x768 minimum (1920x1080 recommended)

### Data Handling
- **Real-time**: Up to 100Hz data acquisition
- **Replay**: Unlimited CSV file size
- **Memory**: Efficient circular buffers
- **Storage**: Compressed CSV logging

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/marcle-bert26-ui/fs-telemetry/issues)
- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)

---

**Built with ❤️ for EIGSI Formula Student Team**
```

**Note**: On Windows, use `py app.py` instead of `python app.py`

---

## ✨ Key Features

✅ **Real-time Arduino data acquisition**  
✅ **Professional PyQt5 GUI with fullscreen support**  
✅ **CSV logging and replay with 100+ data points**  
✅ **Interactive GPS track mapping with time slider**  
✅ **G-force spider/radar charts visualization**  
✅ **18-parameter telemetry monitoring**  
✅ **Enhanced UI with styled group boxes**  
✅ **Improved data visualization and layout**  
✅ **Compact, scrollable interface design**  
✅ **35+ unit tests with 95% coverage**  
✅ **Cross-platform compatibility**  
✅ **File selector with quick access buttons**  
✅ **Real-time statistics and data analysis**  
✅ **Fixed signal/slot connections in GUI components**  
✅ **Enhanced error handling and data validation**  
✅ **Improved performance for large datasets**  

---

## 📚 Full Documentation

Choose your language:

- **[English Documentation](docs/README_EN.md)** - Complete guide in English
- **[Documentation Française](docs/README_FR.md)** - Guide complet en français

---

## 📞 Support

- 📖 Read [INSTALL.md](INSTALL.md) for setup help
- 🐛 Report issues on [GitHub Issues](https://github.com/marcle-bert26-ui/fs-telemetry/issues)
- 💬 Discuss on [GitHub Discussions](https://github.com/marcle-bert26-ui/fs-telemetry/discussions)

---

<div align="center">

**Made with ❤️ for Formula Student**

</div>

python -m venv venv
venv\Scripts\activate  # On Windows
# or: source venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt

### 2. Configure Arduino Connection
Edit `config.py`:
```python
SERIAL_PORT = "COM3"        # Change to your Arduino port
SERIAL_BAUDRATE = 115200    # Match Arduino serial speed
```

### 3. Run in LIVE Mode (Read from Arduino)
```bash
python main.py
```
- Connects to Arduino
- Displays data in real-time
- Saves to `data_logs/run_TIMESTAMP.csv`
- Press `Ctrl+C` to stop

### 4. Run in REPLAY Mode (Analyze recorded run)
Edit `config.py`:
```python
SIMULATION_MODE = True
```
Then:
```bash
python main.py
```
- Prompts for CSV file path
- Replays with timing
- Shows statistics

## Arduino Format (CSV)

Your Arduino should send CSV lines like:
```
time_ms;speed_kmh;rpm;throttle;battery_temp
123456;45.2;8120;0.78;62.3
123457;45.5;8150;0.80;62.4
```

**Send CSV header once at startup**, then one data line per measurement.

## Example Arduino Code
```c
void setup() {
  Serial.begin(115200);
  Serial.println("time_ms;speed_kmh;rpm;throttle;battery_temp");
}

void loop() {
  unsigned long time = millis();
  float speed = readSpeed();
  int rpm = readRPM();
  float throttle = readThrottle();
  float temp = readBatteryTemp();
  
  Serial.print(time); Serial.print(";");
  Serial.print(speed, 1); Serial.print(";");
  Serial.print(rpm); Serial.print(";");
  Serial.print(throttle, 2); Serial.print(";");
  Serial.println(temp, 1);
  
  delay(20);  // 50 Hz = 20ms
}
```

## Key Design Principles

### 1. Separation of Concerns
- **Acquisition**: Only reads data, no parsing
- **Parsing**: Only converts format, no storage
- **Data Manager**: Only manages state, no I/O
- **Logger**: Only writes, no logic
- **Display**: Only shows, no decisions

### 2. Swappable Sources
Same code runs with:
- `SerialSource()` → reads from Arduino
- `CSVSource()` → reads from CSV file
No changes to main logic needed.

### 3. Production Ready
- Error handling & validation
- Type hints & docstrings
- Clear separation HARDWARE / SOFTWARE
- Testable components

## Usage Examples

### Access current data
```python
from data.telemetry_manager import TelemetryManager

manager = TelemetryManager()
current = manager.get_current()
print(f"Speed: {current.speed} km/h")
```

### Get statistics
```python
stats = manager.get_stats()
print(f"Max Speed: {stats['max_speed']} km/h")
print(f"Avg Temp: {stats['avg_temp']}°C")
```

### Process all historical data
```python
for data_point in manager.get_history():
    print(data_point)
```

## Troubleshooting

### Arduino Not Found
- Check `config.SERIAL_PORT` matches your Arduino's port
- On Windows: Check Device Manager → COM ports
- On Linux: `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`

### Serial Timeout
- Verify Arduino is sending data at configured baudrate
- Check USB cable connection
- Try increasing `SERIAL_TIMEOUT` in config.py

### CSV Parse Errors
- Ensure Arduino sends exactly 5 semicolon-separated values
- No extra spaces or line endings
- Check `config.CSV_HEADER` matches Arduino output

## Next Steps

- Add graphs with matplotlib/plotly
- Implement real-time plots with pyqtgraph
- Build web dashboard with Dash/Flask
- Add CAN bus support for future hardware
- Implement data validation & fault detection

## Formula Student Best Practices ✓

- ✅ Modular architecture → easy to test & extend
- ✅ Hardware / Software separation → swap sources easily  
- ✅ CSV logging → reproducible & portable data
- ✅ Replay capability → analyze without car
- ✅ Clear code structure → easy for judges to understand
- ✅ Type hints & docstrings → professional standards

---

**Made for serious Formula Student teams** 🏎️⚡

---

## 🎯 **Usage Examples**

### LIVE MODE - Real-time Acquisition
```bash
python app.py
```
- Connects to Arduino automatically
- Displays real-time data with GPS tracking
- Shows G-force spider charts and track map
- Saves to `data_logs/run_TIMESTAMP.csv`

### REPLAY MODE - Data Analysis  
```bash
python app.py
```
- Select CSV file with dropdown or quick buttons
- Analyze 100+ data points with time slider
- Interactive circuit map with position tracking
- G-force visualization with statistics

---

## 📊 **Data Format**

### Enhanced CSV Format (18 parameters)
```csv
time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr
0;0;800;0;20;0;0;1;0;0;0;48.8566;2.3522;100;25;25;25;25
1000;15;1200;5;21;0.1;0.2;0.9;0.1;0.1;0.1;48.8561;2.3523;102;26;26;26;26
```

---

## 🏗️ **Architecture Highlights**

### 🎨 **Modern UI Components**
- **FileSelectorWidget** - CSV file selection with quick access
- **TrackMapWidget** - Interactive GPS visualization
- **SpiderChartWidget** - G-force radar charts  
- **TemporalAnalysisWidget** - Time-based data exploration
- **TelemetryCharts** - Real-time multi-parameter graphs

### 🔧 **Modular Design**
- **Acquisition** → Serial/CSV data sources
- **Parsing** → CSV to TelemetryData conversion
- **Management** → State and statistics tracking
- **Visualization** → Charts, maps, spider graphs
- **Logging** → CSV file output with timestamps

---

## 🎯 **Formula Student Compliance**

✅ **Modular architecture** → Easy to test & extend  
✅ **Hardware/software separation** → Swap sources easily  
✅ **CSV logging** → Reproducible & portable data  
✅ **Replay capability** → Analyze without car  
✅ **Clear code structure** → Easy for judges to understand  
✅ **Type hints & documentation** → Professional standards  
✅ **Error handling & validation** → Production ready  
✅ **18-parameter telemetry** → Comprehensive vehicle monitoring  

---

## 🚀 **What's New in v2.0**

### 🗺️ **Advanced Visualization**
- Interactive GPS track map with time slider
- G-force spider/radar charts
- Temporal analysis with data exploration
- Professional compact interface design
- Enhanced UI styling with color-coded borders

### 📊 **Enhanced Data Support**
- 18 telemetry parameters (vs 4 previously)
- GPS coordinates and altitude tracking
- 3-axis acceleration monitoring
- 4 tire temperature sensors
- 100+ data points for complete circuit analysis

### 🎨 **UI/UX Improvements**
- Compact layout with 350px left panel
- Fullscreen mode with F11/ESC shortcuts
- File selector with quick access buttons
- Scrollable charts without double scroll issues
- Color-coded data displays (blue for controls, red for temperature)
- Fixed ReplayModeWidget signal connections
- Improved error handling and data validation

### 🔧 **Technical Enhancements**
- Fixed PyQt5 signal/slot connections
- Enhanced CSV file parsing error handling
- Improved thread management in replay functionality
- Better performance for large datasets
- Comprehensive GUI component testing
- Enhanced file selector widget reliability

---

<div align="center">

**🏎️ Made with ❤️ for EIGSI Formula Student - Advanced Telemetry System v2.1**

**Latest Release**: v2.1.0 (2026-01-15) - Enhanced UI & Fixed Signal Issues

</div>
