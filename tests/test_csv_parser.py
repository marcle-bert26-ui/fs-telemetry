"""
Unit tests for CSV parser module.
Tests data parsing, validation, and error handling.
"""

import pytest
from parsing.csv_parser import parse_csv_line, TelemetryData


class TestParseCSVLine:
    """Tests for parse_csv_line function"""
    
    def test_valid_csv_line(self):
        """Test parsing a valid CSV line"""
        line = "123456;45.2;8120;0.78;62.3"
        data = parse_csv_line(line)
        
        assert data is not None
        assert data.time_ms == 123456
        assert data.speed == 45.2
        assert data.rpm == 8120
        assert data.throttle == 0.78
        assert data.battery_temp == 62.3
    
    def test_csv_line_with_whitespace(self):
        """Test parsing CSV line with leading/trailing whitespace"""
        line = "  123456;45.2;8120;0.78;62.3  \n"
        data = parse_csv_line(line)
        
        assert data is not None
        assert data.time_ms == 123456
    
    def test_header_line_returns_none(self):
        """Test that header line returns None"""
        header = "time_ms;speed_kmh;rpm;throttle;battery_temp"
        data = parse_csv_line(header)
        
        assert data is None
    
    def test_empty_line_returns_none(self):
        """Test that empty line returns None"""
        data = parse_csv_line("")
        assert data is None
    
    def test_invalid_field_count(self):
        """Test parsing with wrong number of fields"""
        line = "123456;45.2;8120"  # Only 3 fields
        data = parse_csv_line(line)
        
        assert data is None
    
    def test_invalid_numeric_values(self):
        """Test parsing with invalid numeric values"""
        line = "invalid;45.2;8120;0.78;62.3"
        data = parse_csv_line(line)
        
        assert data is None
    
    def test_large_values(self):
        """Test parsing with large values"""
        line = "999999999;120.5;15000;100.0;85.5"
        data = parse_csv_line(line)
        
        assert data is not None
        assert data.time_ms == 999999999
        assert data.speed == 120.5
        assert data.rpm == 15000
    
    def test_zero_values(self):
        """Test parsing with zero values"""
        line = "0;0.0;0;0.0;0.0"
        data = parse_csv_line(line)
        
        assert data is not None
        assert data.time_ms == 0
        assert data.speed == 0.0
        assert data.rpm == 0
    
    def test_negative_values(self):
        """Test parsing with negative values (should work)"""
        line = "123456;-5.0;-100;-0.5;-10.0"
        data = parse_csv_line(line)
        
        assert data is not None
        assert data.speed == -5.0


class TestTelemetryData:
    """Tests for TelemetryData dataclass"""
    
    def test_telemetry_data_creation(self):
        """Test creating TelemetryData object"""
        data = TelemetryData(
            time_ms=100,
            speed=50.0,
            rpm=5000,
            throttle=75.0,
            battery_temp=60.0
        )
        
        assert data.time_ms == 100
        assert data.speed == 50.0
        assert data.rpm == 5000
        assert data.throttle == 75.0
        assert data.battery_temp == 60.0
    
    def test_telemetry_data_str_representation(self):
        """Test string representation of TelemetryData"""
        data = TelemetryData(
            time_ms=100,
            speed=50.0,
            rpm=5000,
            throttle=75.0,
            battery_temp=60.0
        )
        
        str_repr = str(data)
        assert "100ms" in str_repr or "Time: 100" in str_repr
        assert "50.0" in str_repr
