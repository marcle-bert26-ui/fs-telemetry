"""
Unit tests for CSV source module.
Tests reading from CSV files.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.csv_source import CSVSource


class TestCSVSource:
    """Tests for CSVSource class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def sample_csv_file(self, temp_dir):
        """Create a sample CSV file for testing"""
        csv_path = Path(temp_dir) / "test_data.csv"
        
        with open(csv_path, 'w') as f:
            f.write("time_ms;speed_kmh;rpm;throttle;battery_temp\n")
            f.write("1000;45.2;8120;0.78;62.3\n")
            f.write("2000;50.0;8500;0.85;62.5\n")
            f.write("3000;55.0;9000;0.90;62.8\n")
        
        return csv_path
    
    def test_csv_source_opens_file(self, sample_csv_file):
        """Test that CSVSource opens file correctly"""
        source = CSVSource(str(sample_csv_file))
        
        assert source.is_connected()
        assert source.filename == str(sample_csv_file)
        
        source.close()
    
    def test_csv_source_reads_line(self, sample_csv_file):
        """Test reading a single line"""
        source = CSVSource(str(sample_csv_file))
        
        # Skip header
        line = source.read()
        assert line.startswith("time_ms")
        
        # Read first data line
        line = source.read()
        assert "1000;45.2;8120" in line
        
        source.close()
    
    def test_csv_source_reads_all_lines(self, sample_csv_file):
        """Test reading all lines"""
        source = CSVSource(str(sample_csv_file))
        
        lines = []
        while True:
            line = source.read()
            if not line:
                break
            lines.append(line)
        
        # Should have: header + 3 data lines = 4 total
        assert len(lines) == 4
        assert "time_ms" in lines[0]
        assert "1000" in lines[1]
        
        source.close()
    
    def test_csv_source_returns_empty_after_eof(self, sample_csv_file):
        """Test that EOF returns empty strings"""
        source = CSVSource(str(sample_csv_file))
        
        # Read all lines
        while True:
            line = source.read()
            if not line:
                break
        
        # Next read should return empty
        line = source.read()
        assert line == ""
        
        source.close()
    
    def test_csv_source_closes_file(self, sample_csv_file):
        """Test closing the file"""
        source = CSVSource(str(sample_csv_file))
        assert source.is_connected()
        
        source.close()
        assert not source.is_connected()
    
    def test_csv_source_file_not_found(self, temp_dir):
        """Test error handling for non-existent file"""
        nonexistent = Path(temp_dir) / "nonexistent.csv"
        
        with pytest.raises(FileNotFoundError):
            source = CSVSource(str(nonexistent))
    
    def test_csv_source_line_count(self, sample_csv_file):
        """Test line counting"""
        source = CSVSource(str(sample_csv_file))
        
        # Skip header
        source.read()
        
        # Read 3 data lines
        for i in range(3):
            source.read()
        
        assert source.line_count == 4
        
        source.close()
