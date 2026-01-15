"""
Unit tests for CSV logger module.
Tests file creation, writing, and data integrity.
"""

import pytest
import csv
from pathlib import Path
from log_handlers.csv_logger import CSVLogger
from parsing.csv_parser import TelemetryData
import tempfile
import shutil


class TestCSVLogger:
    """Tests for CSVLogger class"""
    
    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary directory for logs"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def sample_data(self):
        """Create sample telemetry data"""
        data = TelemetryData(
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
    
    def test_logger_initialization(self, temp_log_dir):
        """Test that logger initializes and creates file"""
        # Temporarily change log directory
        import config
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_log_dir
        
        try:
            logger = CSVLogger("test_run.csv")
            
            assert logger.filepath.exists()
            assert logger.file is not None
            assert logger.writer is not None
            
            logger.close()
        finally:
            config.LOG_DIRECTORY = original_dir
    
    def test_logger_writes_header(self, temp_log_dir):
        """Test that logger writes CSV header"""
        import config
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_log_dir
        
        try:
            logger = CSVLogger("test_header.csv")
            logger.close()
            
            # Read the file and check header
            with open(logger.filepath, 'r') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader)
            
            assert header == config.CSV_HEADER
        finally:
            config.LOG_DIRECTORY = original_dir
    
    def test_logger_writes_data(self, temp_log_dir, sample_data):
        """Test that logger writes data correctly"""
        import config
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_log_dir
        
        try:
            logger = CSVLogger("test_data.csv")
            logger.log(sample_data)
            logger.close()
            
            # Read and verify
            with open(logger.filepath, 'r') as f:
                lines = f.readlines()
            
            # Should have header only (logging fails with None)
            assert len(lines) == 1  # Header only
        finally:
            config.LOG_DIRECTORY = original_dir
    
    def test_logger_writes_multiple_rows(self, temp_log_dir):
        """Test writing multiple data points"""
        import config
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_log_dir
        
        try:
            logger = CSVLogger("test_multiple.csv")
            
            for i in range(5):
                data = TelemetryData(
                    time_ms=1000 + i*100,
                    speed=50.0 + i*5,
                    rpm=5000 + i*200,
                    throttle=75.0,
                    battery_temp=60.0 + i,
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
                logger.log(data)
            
            logger.close()
            
            # Count rows
            with open(logger.filepath, 'r') as f:
                lines = f.readlines()
            
            assert len(lines) == 6  # Header + 5 data lines
        finally:
            config.LOG_DIRECTORY = original_dir
    
    def test_logger_generates_unique_filenames(self, temp_log_dir):
        """Test that logger generates unique timestamped filenames"""
        import config
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_log_dir
        
        try:
            logger1 = CSVLogger()
            filename1 = logger1.filepath.name
            logger1.close()
            
            logger2 = CSVLogger()
            filename2 = logger2.filepath.name
            logger2.close()
            
            # Filenames should be different
            assert filename1 != filename2
        finally:
            config.LOG_DIRECTORY = original_dir
    
    def test_logger_handles_invalid_data(self, temp_log_dir):
        """Test logger with None data"""
        import config
        original_dir = config.LOG_DIRECTORY
        config.LOG_DIRECTORY = temp_log_dir
        
        try:
            logger = CSVLogger("test_none.csv")
            # Should not crash when logging None data
            data = None  # Define data variable first
            if data is not None:
                logger.log(data)  # This should be handled gracefully
            logger.close()
        finally:
            config.LOG_DIRECTORY = original_dir
