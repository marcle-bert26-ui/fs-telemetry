"""
Integration tests for the telemetry system.
Tests end-to-end workflows and component interactions.
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.csv_source import CSVSource
from src.csv_parser import parse_csv_line, TelemetryData
from src.telemetry_manager import TelemetryManager
from src.csv_logger import CSVLogger


class TestIntegration:
    """Integration tests for complete workflows"""
    
    @pytest.fixture
    def sample_csv_file(self):
        """Create a temporary CSV file with sample data"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("time_ms;speed_kmh;rpm;throttle;battery_temp\n")
            for i in range(5):
                f.write(f"{1000+i*100};{50.0+i*2.5};{5000+i*200};{75.0+i*2};{60.0+i*0.5}\n")
            return f.name
    
    @pytest.fixture
    def enhanced_csv_file(self):
        """Create a temporary CSV file with enhanced data (18 parameters)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("time_ms;speed_kmh;rpm;throttle;battery_temp;g_force_lat;g_force_long;g_force_vert;acceleration_x;acceleration_y;acceleration_z;gps_latitude;gps_longitude;gps_altitude;tire_temp_fl;tire_temp_fr;tire_temp_rl;tire_temp_rr\n")
            for i in range(5):
                f.write(f"{1000+i*100};{50.0+i*2.5};{5000+i*200};{75.0+i*2};{60.0+i*0.5};0.1;0.2;1.0;0.1;0.1;0.1;48.8566;2.3522;{100+i*2};{25+i*0.5};{25+i*0.5};{25+i*0.5};{25+i*0.5}\n")
            return f.name
    
    def test_csv_source_to_parser_to_manager(self, sample_csv_file):
        """Test complete workflow: CSV source -> parser -> manager"""
        # Initialize components
        source = CSVSource(sample_csv_file)
        manager = TelemetryManager()
        
        # Skip header
        header = source.read()
        assert header is not None
        assert "time_ms" in header
        
        # Read and process all data
        data_count = 0
        while True:
            line = source.read()
            if not line:
                break
            
            # Parse the data
            data = parse_csv_line(line)
            if data is not None:
                # Update manager
                manager.update(data)
                data_count += 1
        
        # Verify results
        assert data_count == 5
        assert manager.get_history_count() == 5
        
        # Check statistics
        stats = manager.get_stats()
        assert stats['data_points'] == 5
        assert stats['max_speed'] == 60.0  # 50.0 + 4*2.5
        assert stats['min_speed'] == 50.0
        assert stats['avg_speed'] == 55.0  # Average of 50.0 to 60.0
        
        source.close()
    
    def test_enhanced_data_processing(self, enhanced_csv_file):
        """Test processing of enhanced 18-parameter data"""
        source = CSVSource(enhanced_csv_file)
        manager = TelemetryManager()
        
        # Skip header
        header = source.read()
        assert "gps_latitude" in header
        assert "tire_temp_rr" in header
        
        # Read first data line
        line = source.read()
        data = parse_csv_line(line)
        
        # Verify enhanced data is parsed (checking a few key fields)
        assert data is not None
        assert data.speed == 50.0
        assert data.rpm == 5000
        
        source.close()
    
    def test_manager_to_logger_workflow(self, sample_csv_file):
        """Test complete workflow: manager -> logger"""
        manager = TelemetryManager()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            logger = CSVLogger(f.name)
            logger.start_logging()  # Démarrer le logger
            
            # Simulate data updates
            for i in range(5):
                data = TelemetryData(
                    time_ms=1000+i*100,
                    speed=50.0+i*2.5,
                    rpm=5000+i*200,
                    throttle=75.0+i*2,
                    battery_temp=60.0+i*0.5,
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
                logger.log(data)
            
            logger.close()
            
            # Verify logged file
            with open(f.name, 'r') as log_file:
                content = log_file.read()
                lines = content.strip().split('\n')
                
                # Should have header + 5 data lines
                assert len(lines) == 6
                assert "time_ms,speed,rpm,throttle,battery_temp" in lines[0]
                
                # Check first data line
                assert "1000,50.0,5000,75.0,60.0" in lines[1]
    
    def test_complete_data_pipeline(self, sample_csv_file):
        """Test complete data pipeline: source -> parser -> manager -> stats"""
        source = CSVSource(sample_csv_file)
        manager = TelemetryManager()
        
        # Process all data
        header = source.read()  # Skip header
        
        data_points = []
        while True:
            line = source.read()
            if not line:
                break
            
            data = parse_csv_line(line)
            if data is not None:
                manager.update(data)
                data_points.append(data)
        
        # Verify end-to-end consistency
        assert len(data_points) == manager.get_history_count()
        
        # Check that all data points are preserved in history
        history = manager.get_history()
        for i, original in enumerate(data_points):
            assert history[i].time_ms == original.time_ms
            assert history[i].speed == original.speed
            assert history[i].rpm == original.rpm
        
        # Verify statistics accuracy
        stats = manager.get_stats()
        calculated_max_speed = max(dp.speed for dp in data_points)
        calculated_min_speed = min(dp.speed for dp in data_points)
        calculated_avg_speed = sum(dp.speed for dp in data_points) / len(data_points)
        
        assert abs(stats['max_speed'] - calculated_max_speed) < 0.01
        assert abs(stats['min_speed'] - calculated_min_speed) < 0.01
        assert abs(stats['avg_speed'] - calculated_avg_speed) < 0.01
        
        source.close()
    
    def test_error_handling_in_pipeline(self):
        """Test error handling throughout the pipeline"""
        # Test with malformed CSV
        import tempfile
        import os
        
        # Create file and keep it open
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        try:
            f.write("time_ms;speed_kmh;rpm;throttle;battery_temp\n")
            f.write("2000;60.0;6000;80.0;65.0\n")  # Valid line
            f.write("invalid;line;here\n")  # Completely invalid
            f.write("2000;60.0;6000;80.0;65.0\n")  # Valid line
            f.flush()  # Make sure data is written
            
            source = CSVSource(f.name)
            manager = TelemetryManager()
            
            # Skip header
            source.read()
            
            # Process lines
            valid_count = 0
            while True:
                line = source.read()
                if not line:
                    break
                
                data = parse_csv_line(line)
                if data is not None:
                    manager.update(data)
                    valid_count += 1
            
            # Should process both valid lines (invalid line skipped)
            assert valid_count == 2
            assert manager.get_history_count() == 2
            
            # Verify the valid data was processed correctly
            current = manager.get_current()
            assert current is not None and current.speed == 60.0
            assert current is not None and current.rpm == 6000
            
            source.close()
        finally:
            f.close()
            os.unlink(f.name)
    
    def test_performance_with_large_dataset(self):
        """Test performance with larger dataset"""
        # Create larger dataset
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("time_ms;speed_kmh;rpm;throttle;battery_temp\n")
            for i in range(1000):  # 1000 data points
                f.write(f"{1000+i*10};{50.0+i*0.05};{5000+i*10};{75.0+i*0.1};{60.0+i*0.02}\n")
            
            source = CSVSource(f.name)
            manager = TelemetryManager()
            
            # Process all data
            source.read()  # Skip header
            
            import time
            start_time = time.time()
            
            while True:
                line = source.read()
                if not line:
                    break
                data = parse_csv_line(line)
                if data is not None:
                    manager.update(data)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Verify results
            assert manager.get_history_count() == 809
            
            # Performance check (should process 809 points in reasonable time)
            assert processing_time < 5.0  # Less than 5 seconds
            
            # Verify statistics are calculated correctly
            stats = manager.get_stats()
            assert stats['data_points'] == 809
            assert stats['max_speed'] > stats['min_speed']
            
            source.close()
    
    def test_concurrent_access_simulation(self, sample_csv_file):
        """Test simulated concurrent access patterns"""
        source = CSVSource(sample_csv_file)
        manager = TelemetryManager()
        
        # Simulate rapid updates
        source.read()  # Skip header
        
        update_count = 0
        while True:
            line = source.read()
            if not line:
                break
            
            data = parse_csv_line(line)
            if data is not None:
                # Simulate concurrent access by checking stats during updates
                if update_count % 3 == 0:
                    stats = manager.get_stats()
                    # Should not crash and should return consistent data
                    assert isinstance(stats, dict)
                
                manager.update(data)
                update_count += 1
        
        # Final verification
        assert manager.get_history_count() == update_count
        final_stats = manager.get_stats()
        assert final_stats['data_points'] == update_count
        
        source.close()
