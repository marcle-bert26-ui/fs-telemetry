# Formula Student Telemetry System

🏎️ Professional real-time telemetry data acquisition and analysis application for Formula Student vehicles.

[![Tests](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml/badge.svg)](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Full Documentation](README_APP.md)** • **[French Version](README_FR.md)** • **[Installation Guide](INSTALL.md)** • **[Contributing](CONTRIBUTING.md)** • **[Changelog](CHANGELOG.md)**

---

## ✨ Features

### 🟢 LIVE MODE
- Real-time Arduino data acquisition
- Live telemetry display (Speed, RPM, Throttle, Temperature)
- Automatic CSV logging
- Real-time statistics

### 🔄 REPLAY MODE  
- Load and analyze recorded CSV files
- Session statistics and analytics
- Historical data visualization
- Performance metrics

### 📊 Core Capabilities
- ✅ Professional PyQt5 GUI
- ✅ Multi-threaded architecture
- ✅ Comprehensive testing (35+ tests)
- ✅ Cross-platform (Windows/Linux/macOS)
- ✅ CSV data logging
- ✅ Statistics calculation
- ✅ Error handling & recovery

---

## 🚀 Quick Start

### Windows
```bash
double-click run.bat    # GUI mode
# or
python review.py       # Project review
```

### Linux / macOS
```bash
bash run.sh            # GUI mode
# or
python3 review.py      # Project review
```

Or manually:
```bash
python app.py          # GUI mode
python main.py         # CLI mode
python review.py       # Project overview & statistics
```

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Linux, or macOS
- **Dependencies**: See [requirements.txt](requirements.txt)
- **Arduino**: (Optional, for LIVE mode)

---

## 📦 Installation

### Quick Install
```bash
# Clone repository
git clone https://github.com/marcle-bert26-ui/fs-telemetry.git
cd fs-telemetry

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# or (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

**For detailed installation instructions**, see [INSTALL.md](INSTALL.md)

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README_APP.md](README_APP.md) | Complete feature documentation |
| [README_FR.md](README_FR.md) | Version française |
| [INSTALL.md](INSTALL.md) | Platform-specific installation guide |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history and releases |
| [tests/README.md](tests/README.md) | Testing documentation |

---

## 🏗️ Project Structure

```
fs-telemetry/
├── gui/                 # GUI application
├── acquisition/         # Data acquisition
├── parsing/            # Data parsing
├── data/               # Data management
├── log_handlers/       # CSV logging
├── visualization/      # Display utilities
├── tests/              # Unit tests
├── app.py              # GUI entry point
├── main.py             # CLI entry point
├── config.py           # Configuration
└── requirements.txt    # Dependencies
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_csv_parser.py::TestParseCSVLine::test_valid_csv_line -v
```

**Test Results**: ✅ 35/35 tests passing

---

## ⚙️ Configuration

Edit `config.py`:

```python
# Serial Configuration
SERIAL_PORT = "COM3"        # Change to your Arduino port
SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 1

# Logging
LOG_DIRECTORY = "data_logs"
LOG_FILENAME_PREFIX = "run"

# CSV Format
CSV_DELIMITER = ";"
CSV_HEADER = ["time_ms", "speed_kmh", "rpm", "throttle", "battery_temp"]

# Mode
SIMULATION_MODE = False     # Set True for replay mode
```

---

## 🔌 Arduino Integration

Expected CSV format:
```
time_ms;speed_kmh;rpm;throttle;battery_temp
100;10.5;2000;25;35.2
200;15.3;2500;40;35.5
```

Find your Arduino port:
- **Windows**: Device Manager → Ports (COM & LPT)
- **Linux**: `ls /dev/ttyUSB*`
- **macOS**: `ls /dev/cu.*`

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Write tests for new features
5. Ensure all tests pass
6. Commit clearly (`git commit -m "Add my feature"`)
7. Push and open a Pull Request

**[Contributing Guidelines](CONTRIBUTING.md)** • **[Code of Conduct](CONTRIBUTING.md#code-of-conduct)**

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- [Project GitHub](https://github.com/marcle-bert26-ui/fs-telemetry)
- [Issues & Bugs](https://github.com/marcle-bert26-ui/fs-telemetry/issues)
- [Discussions](https://github.com/marcle-bert26-ui/fs-telemetry/discussions)
- [Website](https://eigsiformulateam.fr/)
- [Formula Student](https://www.formulastudent.com/)

---

## 💡 Tips & Tricks

### Performance
- Close other applications for better responsiveness
- Use SSD for faster CSV file operations
- Update Python and dependencies regularly

### Troubleshooting
- Serial port not found? Check Device Manager
- ModuleNotFoundError? Install dependencies: `pip install -r requirements.txt`
- GUI not starting? Ensure PyQt5 is installed: `pip install PyQt5`

### Common Tasks
```bash
# Create new CSV log
python main.py

# Analyze recorded data  
python main.py  # Set SIMULATION_MODE = True

# Run tests with coverage
pytest --cov=.

# Check for issues
pylint *.py acquisition/*.py
```

---

## 🎓 Educational Value

This project demonstrates:
- ✅ Professional Python application architecture
- ✅ GUI development with PyQt5
- ✅ Serial communication with hardware
- ✅ Data processing and analysis
- ✅ Unit testing best practices
- ✅ Documentation and project setup
- ✅ Version control and CI/CD

Perfect for students and developers learning real-world Python!

---

## 💡 Future Improvements

The project is functionally complete for basic acquisition, replay and analysis, but there are many practical enhancements that would improve usability, analysis power and distribution. Below are suggested additions (good first issues) and higher-impact features to consider.

- **Multi-session comparison**: side-by-side and overlay comparisons, delta traces, aligned lap/sector comparison and automatic session matching.
- **Improved UI / UX**: modern themes, responsive layouts, smoother controls and improved file dialogs; consider `pyqtgraph` or `plotly` for interactive charts.
- **Branding & visuals**: add a team logo, icons, themed color scheme, and exportable report templates (PDF).
- **Export formats**: JSON, Excel (`.xlsx`), compressed archives and GPX/KML exports for mapping data.
- **Advanced analytics**: automatic lap detection, telemetry alignment, sensor fusion, derived metrics (power, energy, lateral/longitudinal G), and anomaly detection.
- **Plugin/importers**: support for additional telemetry sources (CAN, OBD-II) and a plugin system to extend parsers and visualizations.
- **Realtime dashboards & streaming**: low-latency plots, dashboard layouts, and optional WebSocket streaming for remote monitoring.
- **Packaging & installers**: provide signed installers and CI-built artifacts (NSIS for Windows, AppImage/.deb for Linux, signed DMG for macOS) and publish releases automatically.
- **Localization & accessibility**: translations, keyboard navigation, high-contrast themes and screen-reader friendliness.
- **Automated benchmarks & telemetry fuzzing**: stress tests for high-rate data, CI performance checks and profiling.

How to help: pick an item above, open an issue, and submit a PR — small, focused changes (UI polish, a single export format, or a plugin) are very welcome.

---

## 🎯 Roadmap

### Version 1.1.0 (Planned)
- [ ] Real-time graphical charts
- [ ] Data export (JSON, Excel)
- [ ] Advanced filtering

### Version 1.2.0 (Future)
- [ ] Multi-session comparison
- [ ] Web interface
- [ ] Cloud storage

---

## 📞 Support

Need help?
1. Check [INSTALL.md](INSTALL.md) for common issues
2. Review [README_APP.md](README_APP.md) for features
3. Open an [issue on GitHub](https://github.com/yourusername/fs-telemetry/issues)

---

<div align="center">

**Made with ❤️ for Formula Student**

[⬆ Back to top](#formula-student-telemetry-system)

</div>
