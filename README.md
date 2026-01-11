# Formula Student Telemetry System

🏎️ Professional real-time telemetry data acquisition and analysis application for Formula Student vehicles.

[![Tests](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml/badge.svg)](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Language** • [English](README_EN.md) | [Français](README_FR.md)

---

## Quick Access

| Document | Purpose | Language |
|----------|---------|----------|
| [README_EN.md](README_EN.md) | Main documentation | English |
| [README_FR.md](README_FR.md) | Documentation complète | Français |
| [README_APP.md](README_APP.md) | Feature details | English |
| [INSTALL.md](INSTALL.md) | Installation guide | English |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide | English |
| [CHANGELOG.md](CHANGELOG.md) | Version history | English |

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
python app.py        # GUI mode (LIVE/REPLAY)
python main.py       # CLI mode
python review.py     # Project review
```

---

## ✨ Key Features

✅ Real-time Arduino data acquisition  
✅ Professional PyQt5 GUI  
✅ CSV logging and replay  
✅ Live statistics  
✅ 35+ unit tests  
✅ Cross-platform  

---

## 📚 Full Documentation

Choose your language:

- **[English Documentation](README_EN.md)** - Complete guide in English
- **[Documentation Française](README_FR.md)** - Guide complet en français

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
```

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
