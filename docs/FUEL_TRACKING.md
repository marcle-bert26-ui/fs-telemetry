# Fuel Consumption Tracking Guide

## Overview

The FS-Telemetry System v2.3 introduces comprehensive fuel consumption monitoring with real-time calculations and interactive visualizations.

## 📊 Fuel Charts

### Available Metrics

1. **Régime Moteur (RPM)**
   - Engine revolutions per minute
   - Range: 0-10,000 RPM
   - Real-time monitoring

2. **Accélération**
   - Calculated from longitudinal G-forces
   - Formula: `acceleration = g_force_long * 9.81`
   - Range: -20 to +20 m/s²
   - Units: m/s²

3. **Injection**
   - Simulated injection timing based on RPM and throttle
   - Formula: `injection_us = 800 + (rpm/9500) * 6000 + throttle * 200`
   - Range: 0-20,000 µs
   - Units: microseconds (µs)

4. **Débit Carburant (Fuel Flow)**
   - Calculated fuel consumption rate
   - Formula: `fuel_flow_lh = (injection_us/1000000) * (rpm/60) * 0.415 * 3600/1000`
   - Range: 0-50 L/h
   - Units: Liters per hour

5. **Volume Carburant (Fuel Volume)**
   - Cumulative fuel consumption
   - Formula: `volume_total = previous_volume + fuel_flow_lh/3600`
   - Range: 0-20 L
   - Units: Liters (L)

## 🎯 Interactive Features

### Synchronized Cursor System

- **Real-time tracking**: Cursor follows temporal slider position
- **Cross-chart synchronization**: All fuel charts update simultaneously
- **Accurate positioning**: Uses actual data values from chart buffers
- **Visual indicators**: Colored circles match chart colors

### Chart Interactions

- **Auto-zoom**: 2-minute window and full auto-zoom options
- **Real-time updates**: Live data streaming in LIVE mode
- **Replay analysis**: Frame-by-frame cursor movement in REPLAY mode
- **Data validation**: Smart filtering prevents invalid data display

## 🔧 Technical Implementation

### Data Flow

```
Arduino Data → CSV Parser → Telemetry Manager → Fuel Charts
     ↓
Real-time Calculations → Buffer Storage → Visual Display
```

### Calculation Methods

#### Injection Timing
```python
injection_us = 800 + (rpm/9500) * 6000 + throttle * 200
```

#### Fuel Flow Rate
```python
fuel_flow_lh = (injection_us/1000000) * (rpm/60) * 0.415 * 3600/1000
```

#### Cumulative Volume
```python
volume_total = previous_volume + fuel_flow_lh/3600
```

### Buffer Management

- **Circular buffers**: 1000-point maximum capacity
- **Real-time updates**: 10Hz recommended update rate
- **Memory efficient**: Automatic cleanup of old data points
- **Thread-safe**: Concurrent access protection

## 📈 Data Analysis

### Performance Metrics

- **Fuel Efficiency**: Calculate L/100km from speed and fuel flow
- **Consumption Rate**: Monitor fuel flow variations
- **Injection Patterns**: Analyze timing vs. RPM relationships
- **Cumulative Usage**: Track total fuel consumption over sessions

### Statistical Analysis

Available statistics for each fuel parameter:
- **Minimum/Maximum**: Session extremes
- **Average**: Mean values over time
- **Current**: Real-time values
- **Rate of Change**: Trend analysis

## 🎨 User Interface

### Chart Layout

```
┌─────────────────────────────────────────────────────┐
│                 Fuel Charts Panel                    │
├─────────────────────┬───────────────────────────────┤
│    RPM (tr/min)     │      Accélération (m/s²)      │
├─────────────────────┼───────────────────────────────┤
│           Injection (µs) - Span 2 Columns            │
├─────────────────────┬───────────────────────────────┤
│   Débit (L/h)       │        Volume (L)              │
└─────────────────────┴───────────────────────────────┘
```

### Visual Features

- **Color coding**: Each parameter has distinct color
- **Grid lines**: Enhanced readability with 0.3 alpha
- **Legend display**: Parameter names with units
- **Dark theme**: Professional appearance with reduced eye strain

## 🔍 Troubleshooting

### Common Issues

#### Fuel Charts Not Updating
- **Check data source**: Ensure Arduino is sending valid RPM data
- **Verify calculations**: Check throttle and RPM values
- **Buffer status**: Confirm data buffers are populated

#### Cursor Not Synchronized
- **Slider connection**: Verify temporal slider is moving
- **Data indexing**: Check point_idx matches buffer positions
- **Chart updates**: Ensure cursor update function is called

#### Incorrect Calculations
- **Formula validation**: Verify calculation constants
- **Data types**: Check for None values in calculations
- **Unit consistency**: Ensure proper unit conversions

### Debug Information

Enable debug mode by checking console output:
- Data buffer sizes
- Cursor update calls
- Calculation results
- Error messages

## 🚀 Future Enhancements

### Planned Features

- **Real fuel sensor integration**: Direct fuel flow measurements
- **Efficiency calculations**: L/100km and MPG metrics
- **Predictive modeling**: Fuel consumption forecasting
- **Alert system**: Low fuel warnings
- **Export capabilities**: CSV/Excel data export

### Optimization Opportunities

- **GPU acceleration**: Hardware-accelerated rendering
- **Data compression**: Efficient storage algorithms
- **Real-time filtering**: Noise reduction techniques
- **Machine learning**: Pattern recognition and anomaly detection

## 📚 Related Documentation

- [Main README](../README.md) - General system overview
- [Installation Guide](../INSTALL.md) - Setup instructions
- [API Reference](API_REFERENCE.md) - Technical documentation
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

---

**Version**: 2.3.0  
**Last Updated**: 2026-03-16  
**Compatibility**: FS-Telemetry v2.3+
