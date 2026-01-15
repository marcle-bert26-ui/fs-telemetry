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
        """Test TelemetryData object creation"""
        data = TelemetryData(
            time_ms=123456,
            speed=45.2,
            rpm=8120,
            throttle=0.78,
            battery_temp=62.3,
            g_force_lat=0.5,
            g_force_long=0.3,
            g_force_vert=1.0,
            acceleration_x=2.1,
            acceleration_y=0.5,
            acceleration_z=0.1,
            gps_latitude=48.8566,
            gps_longitude=2.3522,
            gps_altitude=150.0,
            tire_temp_fl=75.2,
            tire_temp_fr=74.8,
            tire_temp_rl=73.5,
            tire_temp_rr=74.1
        )
        
        assert data.time_ms == 123456
        assert data.speed == 45.2
        assert data.rpm == 8120
        assert data.battery_temp == 62.3
    
    def test_telemetry_data_str_representation(self):
        """Test string representation of TelemetryData"""
        data = TelemetryData(
            time_ms=100,
            speed=50.0,
            rpm=5000,
            throttle=75.0,
            battery_temp=60.0,
            g_force_lat=0.0,
            g_force_long=0.0,
            g_force_vert=1.0,
            acceleration_x=0.0,
            acceleration_y=0.0,
            acceleration_z=0.0,
            gps_latitude=0.0,
            gps_longitude=0.0,
            gps_altitude=0.0,
            tire_temp_fl=0.0,
            tire_temp_fr=0.0,
            tire_temp_rl=0.0,
            tire_temp_rr=0.0
        )
        
        str_repr = str(data)
        assert "100ms" in str_repr or "Time: 100" in str_repr
        assert "50.0" in str_repr
