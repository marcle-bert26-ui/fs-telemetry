# Changelog

All notable changes to the Formula Student Telemetry System project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Real-time graphical charts and gauges
- Data export to JSON and Excel formats
- Advanced analytics (acceleration, performance metrics)
- Multi-session comparison and analysis
- Web interface for remote monitoring
- Cloud storage integration
- Mobile app support

## [1.1.0] - 2026-01-11

### Added
- **CI/CD Pipeline (GitHub Actions)**
  - Automated testing on Python 3.8-3.12
  - Cross-platform testing (Windows, Linux, macOS)
  - Code coverage reporting
  - Automatic linting

- **Type Stubs & IDE Support**
  - PyQt5 type stubs for Pylance/mypy
  - Pyrightconfig for static analysis
  - VS Code settings configuration

### Fixed
- **PyQt5 Compatibility**
  - Improved PyQt5 mocking for headless CI/CD environments
  - Fixed import errors in GUI modules
  - Created conftest.py mocking strategy for all PyQt5 modules

- **CSV Logger**
  - Fixed unique filename generation with counter to prevent collisions
  - Ensured rapid sequential calls generate unique filenames

- **Dependencies**
  - Created separate `requirements-ci.txt` without PyQt5 for CI
  - Updated PyQt5 to compatible versions
  - Fixed system dependencies for Ubuntu 24.04

## [1.0.0] - 2026-01-11

### Added
- **GUI Application**
  - PyQt5-based graphical user interface
  - LIVE mode tab for real-time Arduino data acquisition
  - REPLAY mode tab for CSV file analysis
  - Real-time data visualization
  - Session statistics display
  - Status logging and error reporting

- **Live Mode Features**
  - Serial communication with Arduino
  - Real-time telemetry data display
  - Automatic CSV logging
  - Configurable serial port and baudrate
  - Live statistics calculation
  - Error handling and recovery

- **Replay Mode Features**
  - CSV file loading and playback
  - Historical data analysis
  - Session statistics
  - File browser dialog
  - Progress monitoring

- **Core Modules**
  - `acquisition/`: Data source interfaces
    - `SerialSource`: Arduino serial communication
    - `CSVSource`: CSV file reading
    - `TelemetrySource`: Base interface
  - `parsing/`: Data parsing and validation
    - `parse_csv_line()`: CSV line parsing
    - `TelemetryData`: Data class with validation
  - `data/`: Data management
    - `TelemetryManager`: History and statistics
  - `log_handlers/`: Data persistence
    - `CSVLogger`: CSV file logging
  - `visualization/`: Display utilities
    - `ConsoleDisplay`: Terminal output
  - `gui/`: GUI components
    - `MainWindow`: Main application window
    - `LiveModeWidget`: LIVE mode interface
    - `ReplayModeWidget`: REPLAY mode interface

- **Testing**
  - Comprehensive unit test suite (35+ tests)
  - CSV parser tests
  - CSV logger tests
  - CSV source tests
  - Telemetry manager tests
  - Code coverage reporting
  - Demo test script

- **Documentation**
  - README with features and quick start
  - Installation guide for Windows/Linux/macOS
  - Contributing guidelines
  - API reference
  - Configuration documentation

- **Project Setup**
  - setup.py for packaging
  - pyproject.toml configuration
  - requirements.txt with dependencies
  - .gitignore for version control
  - MIT License
  - GitHub Actions CI/CD workflow

- **Command Line Interface**
  - CLI for LIVE mode (Arduino acquisition)
  - CLI for REPLAY mode (CSV analysis)
  - Configuration via config.py

### Features in Detail

#### Data Acquisition
- Real-time serial communication with Arduino
- Configurable baud rate and serial port
- Automatic error handling and reconnection
- Data validation and parsing
- Format: `time_ms;speed;rpm;throttle;battery_temp`

#### Data Logging
- Automatic CSV file generation with timestamps
- Unique filename generation (microsecond precision)
- Proper CSV formatting with headers
- Data persistence

#### Data Analysis
- Real-time statistics calculation
- Historical data tracking
- Min/max/average calculations
- CSV file replay from disk

#### User Interface
- Professional PyQt5 GUI
- Tab-based interface for modes
- Real-time data display
- Status logging
- Error reporting
- Cross-platform (Windows/Linux/macOS)

#### Testing & Quality
- 35+ unit tests
- Code coverage support
- Multiple Python version support (3.8+)
- Cross-platform CI/CD

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Removed
- N/A (initial release)

### Security
- Input validation on all data
- Safe file handling with proper permissions
- Error messages without sensitive data exposure

## [0.1.0] - 2026-01-10

### Initial Development
- Project structure setup
- Core module creation
- Basic CLI implementation
- Test framework setup
- Documentation scaffolding

---

## Release Guidelines

### Version Numbering
- MAJOR: Breaking changes or major features
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Before Release
- [ ] All tests passing
- [ ] Code coverage >80%
- [ ] Documentation updated
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Version number bumped
- [ ] Commit tagged with version

### Release Checklist
1. Update version in setup.py and pyproject.toml
2. Update CHANGELOG with release notes
3. Run all tests: `pytest tests/ -v`
4. Check code coverage: `pytest --cov=.`
5. Verify no Python warnings
6. Commit: `git commit -m "Release v1.x.x"`
7. Tag: `git tag -a v1.x.x -m "Release version 1.x.x"`
8. Push: `git push origin main --tags`
9. Create GitHub release with notes

---

## Comparison With Other Tools

### vs Arduino IDE Serial Monitor
- ✅ Professional GUI
- ✅ Data logging and analysis
- ✅ Replay capability
- ✅ Statistics calculation
- ✅ Cross-platform

### vs Custom Scripts
- ✅ Easy to use
- ✅ No programming required
- ✅ Professional appearance
- ✅ Well tested

---

**Last Updated**: 2026-01-11
