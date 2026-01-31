"""
Unit tests for telemetry manager module.
Tests data storage, history, and statistics.
"""

import pytest
from src.telemetry_manager import TelemetryManager
from src.csv_parser import TelemetryData


class TestTelemetryManager:
    """Tests for TelemetryManager class"""
    
    @pytest.fixture
    def manager(self):
        """Create a fresh manager for each test"""
        return TelemetryManager()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample telemetry data"""
        return TelemetryData(
            time_ms=1000,
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
    
    def test_manager_initialization(self, manager):
        """Test that manager initializes correctly"""
        assert manager.current is None
        assert manager.history == []
        assert manager.update_count == 0
    
    def test_single_update(self, manager, sample_data):
        """Test updating with a single data point"""
        manager.update(sample_data)
        
        assert manager.current == sample_data
        assert len(manager.history) == 1
        assert manager.update_count == 1
    
    def test_multiple_updates(self, manager, sample_data):
        """Test updating with multiple data points"""
        for i in range(10):
            data = TelemetryData(
                time_ms=1000 + i*100,
                speed=50.0 + i,
                rpm=5000 + i*100,
                throttle=75.0,
                battery_temp=60.0 + i*0.5,
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
            manager.update(data)
        
        assert manager.update_count == 10
        assert len(manager.history) == 10
        assert manager.current.time_ms == 1900
    
    def test_get_current(self, manager, sample_data):
        """Test getting current data"""
        manager.update(sample_data)
        current = manager.get_current()
        
        assert current == sample_data
        assert current.speed == 50.0
    
    def test_get_history(self, manager):
        """Test getting history"""
        data_list = [
            TelemetryData(
                time_ms=1000,
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
            ),
            TelemetryData(
                time_ms=2000,
                speed=55.0,
                rpm=5500,
                throttle=80.0,
                battery_temp=61.0,
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
            ),
            TelemetryData(
                time_ms=3000,
                speed=60.0,
                rpm=6000,
                throttle=85.0,
                battery_temp=62.0,
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
        ]
        
        for data in data_list:
            manager.update(data)
        
        history = manager.get_history()
        assert len(history) == 3
        assert history[0].speed == 50.0
        assert history[2].speed == 60.0
    
    def test_get_history_count(self, manager):
        """Test getting history count"""
        for i in range(10):
            data = TelemetryData(
                time_ms=i*100,
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
            manager.update(data)
        
        assert manager.get_history_count() == 10
    
    def test_get_stats_empty(self, manager):
        """Test statistics on empty history"""
        stats = manager.get_stats()
        assert stats == {}
    
    def test_get_stats_single_point(self, manager, sample_data):
        """Test statistics with single data point"""
        manager.update(sample_data)
        stats = manager.get_stats()
        
        assert stats['max_speed'] == 50.0
        assert stats['min_speed'] == 50.0
        assert stats['avg_speed'] == 50.0
        assert stats['data_points'] == 1
    
    def test_get_stats_multiple_points(self, manager):
        """Test statistics with multiple data points"""
        speeds = [30.0, 50.0, 70.0, 60.0, 40.0]
        rpms = [3000, 5000, 7000, 6000, 4000]
        temps = [55.0, 60.0, 65.0, 62.0, 58.0]
        
        for i, (speed, rpm, temp) in enumerate(zip(speeds, rpms, temps)):
            data = TelemetryData(
                time_ms=i*100,
                speed=speed,
                rpm=rpm,
                throttle=50.0,
                battery_temp=temp,
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
            manager.update(data)
        
        stats = manager.get_stats()
        
        assert stats['max_speed'] == 70.0
        assert stats['min_speed'] == 30.0
        assert stats['avg_speed'] == 50.0
        assert stats['max_rpm'] == 7000
        assert stats['min_rpm'] == 3000
        assert stats['max_temp'] == 65.0
        assert stats['min_temp'] == 55.0
        assert stats['data_points'] == 5
    
    def test_update_with_none(self, manager, sample_data):
        """Test updating with None (should be skipped)"""
        manager.update(sample_data)
        manager.update(None)
        
        assert manager.update_count == 1  # Still 1, not 2
        assert len(manager.history) == 1
        assert manager.current is not None
    
    def test_clear_history(self, manager):
        """Test clearing history"""
        for i in range(5):
            data = TelemetryData(
                time_ms=i*100,
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
            manager.update(data)
        
        assert manager.get_history_count() == 5
        
        manager.clear_history()
        
        assert manager.get_history_count() == 0
        assert manager.current is None
        assert manager.update_count == 0
