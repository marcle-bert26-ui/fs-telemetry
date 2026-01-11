# Formula Student Telemetry System

A comprehensive Python application for acquiring, logging, and analyzing telemetry data from Formula Student vehicles. Features both real-time Arduino data acquisition and offline CSV replay capabilities with a modern GUI interface.

[![Tests](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml/badge.svg)](https://github.com/marcle-bert26-ui/fs-telemetry/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

🟢 **LIVE MODE** - Real-time data acquisition
- Direct Arduino serial communication
- Live telemetry visualization
- Automatic CSV logging
- Real-time statistics

🔄 **REPLAY MODE** - Offline analysis
- Load and replay recorded CSV files
- Session statistics and analysis
- Historical data visualization
- Export and sharing capabilities

📊 **Advanced Features**
- Multi-threaded architecture for smooth UI
- Comprehensive error handling
- **All 35+ tests passing** ✅
- Professional PyQt5 GUI
- Detailed logging and reporting
- **Full CI/CD with GitHub Actions** (Python 3.8-3.12, Windows/Linux/macOS)

## System Requirements

- **Python**: 3.8 or higher (tested up to 3.12)
- **OS**: Windows, Linux, or macOS
- **PyQt5**: For GUI interface
- **pyserial**: For Arduino communication
- **pytest**: For testing

## Installation

### Clone the repository
```bash
git clone https://github.com/marcle-bert26-ui/fs-telemetry.git
cd fs-telemetry
```

### Install dependencies
```bash
pip install -r requirements.txt
pip install PyQt5  # For GUI
```

### Configure Arduino Port
Edit `config.py`:
```python
SERIAL_PORT = "COM3"  # Windows
# or
SERIAL_PORT = "/dev/ttyUSB0"  # Linux
SERIAL_BAUDRATE = 115200
```

## Quick Start

### Launch the GUI Application
```bash
python app.py
```

### Run CLI Version (Live Mode)
```bash
python main.py
```

### Run CLI Version (Replay Mode)
```bash
python main.py
# Enter CSV file path when prompted
```

### Run Tests
```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html  # With coverage
```

### Run Demo
```bash
python test_main_demo.py
```

## Project Structure

```
fs-telemetry/
├── acquisition/          # Data source modules
│   ├── serial_source.py   # Arduino serial communication
│   ├── csv_source.py      # CSV file reading
│   └── telemetry_source.py
├── parsing/              # Data parsing
│   └── csv_parser.py      # CSV parsing and validation
├── data/                 # Data management
│   └── telemetry_manager.py
├── log_handlers/         # Data logging
│   └── csv_logger.py      # CSV file writing
├── gui/                  # GUI components
│   ├── main_window.py     # Main window
│   ├── live_mode_widget.py
│   └── replay_mode_widget.py
├── visualization/        # Console display
│   └── console_display.py
├── tests/                # Unit tests
│   ├── test_csv_parser.py
│   ├── test_csv_logger.py
│   ├── test_csv_source.py
│   └── test_telemetry_manager.py
├── app.py               # GUI application entry point
├── main.py              # CLI application entry point
├── config.py            # Configuration
└── requirements.txt     # Dependencies
```

## Configuration

All configuration is managed in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| SERIAL_PORT | COM3 | Arduino serial port |
| SERIAL_BAUDRATE | 115200 | Serial communication speed |
| LOG_DIRECTORY | data_logs | Directory for CSV logs |
| CSV_DELIMITER | ; | CSV field separator |
| SIMULATION_MODE | False | Enable replay mode |

## CSV Format

The application uses the following CSV format:

```
time_ms;speed_kmh;rpm;throttle;battery_temp
100;10.5;2000;25;35.2
200;15.3;2500;40;35.5
```

## API Reference

### TelemetryData
```python
from parsing.csv_parser import TelemetryData

data = TelemetryData(
    time_ms=100,
    speed=10.5,
    rpm=2000,
    throttle=25,
    battery_temp=35.2
)
```

### TelemetryManager
```python
from data.telemetry_manager import TelemetryManager

manager = TelemetryManager()
manager.update(data)

stats = manager.get_stats()
# Returns: max_speed, avg_speed, max_rpm, avg_rpm, max_temp, avg_temp, data_points

history = manager.get_history()
```

### CSVLogger
```python
from log_handlers.csv_logger import CSVLogger

logger = CSVLogger("custom_filename.csv")
logger.log(data)
logger.close()
```

## Testing

The project includes comprehensive unit tests:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_csv_parser.py

# Run specific test
pytest tests/test_csv_parser.py::TestParseCSVLine::test_valid_csv_line

# View coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

Test coverage includes:
- CSV parsing and validation
- Data logging and file I/O
- Telemetry manager operations
- Error handling and edge cases

## Common Issues

### Arduino Not Detected
- Check COM port in Device Manager (Windows) or `/dev/ttyUSB*` (Linux)
- Update `SERIAL_PORT` in `config.py`
- Verify Arduino is connected and USB driver installed

### ImportError: No module named 'serial'
```bash
pip install pyserial
```

### ImportError: No module named 'PyQt5'
```bash
pip install PyQt5
```

## Development

### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### Install development dependencies
```bash
pip install -r requirements.txt
pip install PyQt5 pytest pytest-cov
```

### Run code formatting
```bash
# Using autopep8 (optional)
autopep8 --in-place --aggressive --aggressive *.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- All tests pass
- Code is well-commented (English)
- Follows PEP 8 style guide
- New features include tests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Marc Legendre** - Formula Student Telemetry Development

## Acknowledgments

- Python/PyQt5 community
- Formula Student community
- Arduino platform

## Changelog

### Version 1.0.0
- Initial release with LIVE and REPLAY modes
- GUI application with PyQt5
- Complete test suite
- Arduino serial integration
- CSV logging and playback

## Support

For issues, questions, or contributions, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include error messages and configuration

## Future Enhancements

- [ ] Real-time graphical charts
- [ ] Export to multiple formats (JSON, Excel)
- [ ] Data filtering and smoothing
- [ ] Advanced analytics (acceleration, performance metrics)
- [ ] Multi-session comparison
- [ ] Web interface

---

**Made with ❤️ for Formula Student**
