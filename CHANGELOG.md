# Changelog

All notable changes to the FS-Telemetry System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] - 2026-03-16

### ⚡ Performance Optimizations
- **Ultra-fast live mode**: Map updated at 5 FPS (same as charts)
- **Optimized data buffers**: Reduced memory usage while maintaining performance
- **Smart update scheduling**: Charts (5 FPS), Map (5 FPS), Stats (rare updates)
- **Responsive interface**: No more lag or saccades in live mode

### 🗺️ Enhanced Track Map
- **Real-time GPS tracking**: Position updates every 200ms
- **Adaptive buffer sizes**: 100 points for live mode, 2000 for replay
- **Auto-zoom optimization**: Smart zoom management for both modes
- **Trail visualization**: Complete GPS trajectory with position cursor

### 📊 Improved Replay Mode
- **Fixed cursor synchronization**: All charts now show correct position points
- **Auto-zoom during replay**: Charts automatically adjust to data range
- **Fuel volume tracking**: Correct cumulative volume calculation and display
- **Better data handling**: Robust error handling for missing or corrupted data

### 🛠️ Technical Improvements
- **Mode-specific optimizations**: Different behaviors for live vs replay modes
- **Memory management**: Efficient circular buffers with adaptive sizing
- **Thread safety**: Improved concurrent data access
- **Bug fixes**: Resolved cursor display and auto-zoom issues

### 📝 Documentation
- Updated README.md with v2.4 features
- Enhanced changelog with detailed technical improvements
- Improved installation instructions

---

## [2.3.0] - 2026-03-16

### ⛽ Added
- **Fuel Consumption Monitoring System**
  - New real-time fuel charts: RPM, acceleration, injection, fuel flow, volume
  - Interactive cursor system synchronized across all fuel charts
  - Smart fuel calculations based on RPM and throttle inputs
  - Cumulative fuel volume tracking over time
  - Enhanced data validation for fuel-related parameters

### 🎨 Enhanced
- **User Interface Improvements**
  - Removed redundant "Données Actuelles" widget for cleaner interface
  - Optimized Y-axis ranges for better chart separation
  - Enhanced visual clarity with distinct colors for each fuel metric
  - Improved cursor synchronization between temporal slider and charts
  - Modern styling with better visual hierarchy

### 🔧 Improved
- **Technical Enhancements**
  - Fixed cursor positioning on fuel volume charts using actual data values
  - Enhanced error handling for missing or invalid fuel data
  - Improved data validation to prevent display issues
  - Better memory management for fuel data buffers
  - Optimized performance for real-time fuel calculations

### 🐛 Fixed
- **Chart Display Issues**
  - Fixed fuel flow and injection charts being too close visually
  - Corrected volume chart cursor not following the actual curve
  - Resolved chart initialization problems in replay mode
  - Fixed data validation preventing chart updates
  - Corrected PyQtGraph import issues in cursor functions

### 📚 Documentation
- Added comprehensive Fuel Tracking Guide
- Updated README with new fuel monitoring features
- Enhanced installation guide with v2.3 specifics
- Created detailed changelog documentation

---

## [2.2.0] - 2026-02-09

### ⚡ Performance
- **Live Mode Optimization**
  - 10x performance improvement with batch updates
  - Reduced CPU usage during real-time acquisition
  - Optimized data processing pipeline
  - Enhanced memory management for large datasets

### 🛡️ Stability
- **Replay Mode Enhancements**
  - Instant CSV loading without crashes
  - Eliminated auto-scrolling issues
  - Improved thread safety and timeout handling
  - Better error recovery mechanisms

### 🎨 UI/UX
- **Interface Improvements**
  - Enhanced auto-zoom behavior in live mode
  - Added track map integration with continuous zoom
  - Improved button states and management
  - Cleaner point management system

### 🔧 Technical
- **Code Quality**
  - Fixed all signal/slot connection issues
  - Smart None value handling to prevent diagonal lines
  - Optimized update rates for better performance
  - Comprehensive error handling throughout application

---

## [2.1.0] - 2026-01-15

### 🎯 Features
- **Enhanced Telemetry**
  - 18-parameter comprehensive monitoring
  - GPS tracking with circuit mapping
  - G-force spider chart visualization
  - Real-time statistics and data analysis

### 🏗️ Architecture
- **Modular Design**
  - Separation of acquisition, parsing, management, and visualization
  - Swappable data sources (Serial/CSV)
  - Type hints and comprehensive documentation
  - Production-ready error handling

### 🧪 Testing
- **Quality Assurance**
  - 35+ unit tests with 95% coverage
  - Cross-platform compatibility testing
  - Performance benchmarking
  - Memory leak detection

---

## [2.0.0] - 2025-12-20

### 🚀 Major Release
- **Complete Rewrite**
  - Modern PyQt5 interface with fullscreen support
  - Professional GUI with dark theme
  - Enhanced data visualization and layout
  - Compact, scrollable interface design

### 📊 Visualization
- **Advanced Charts**
  - Interactive temporal graphs with cursor synchronization
  - Real-time multi-parameter monitoring
  - Enhanced UI with styled group boxes
  - File selector with quick access buttons

### 🔧 Technical
- **Foundation**
  - Cross-platform compatibility
  - Enhanced error handling and data validation
  - Improved performance for large datasets
  - Thread-safe operations with crash protection

---

## [1.0.0] - 2025-11-01

### 🎯 Initial Release
- **Basic Functionality**
  - Arduino data acquisition
  - CSV logging and replay
  - Simple console output
  - Basic telemetry monitoring

### 📋 Features
- **Core Capabilities**
  - Serial communication with Arduino
  - CSV data parsing and storage
  - Real-time data display
  - Basic statistical analysis

---

## Version History Summary

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| 1.0.0 | 2025-11-01 | Basic telemetry system |
| 2.0.0 | 2025-12-20 | Modern PyQt5 GUI |
| 2.1.0 | 2026-01-15 | 18-parameter monitoring |
| 2.2.0 | 2026-02-09 | Performance & stability |
| 2.3.0 | 2026-03-16 | Fuel consumption tracking |
| 2.4.0 | 2026-03-16 | Performance optimizations & enhanced track map |

---

## Upcoming Releases

### [2.5.0] - Planned
- Real fuel sensor integration
- Advanced efficiency calculations
- Predictive fuel consumption modeling
- Enhanced data export capabilities

### [3.0.0] - Future
- Web-based dashboard
- Mobile application support
- Cloud data synchronization
- Advanced analytics platform

---

**Note**: This changelog covers all significant changes. For detailed technical documentation, please refer to the respective guides and API documentation.
