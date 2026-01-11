#!/bin/bash
# Formula Student Telemetry - Linux/macOS Launcher
# This script sets up the Python environment and launches the application

echo ""
echo "========================================"
echo "  Formula Student Telemetry System"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Could not create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Could not activate virtual environment"
    exit 1
fi

# Install/update dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Could not install dependencies"
    echo "Try running: pip install -r requirements.txt"
    exit 1
fi

# Launch application
echo ""
echo "Starting Formula Student Telemetry System..."
echo ""
python app.py
