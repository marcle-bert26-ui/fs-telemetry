@echo off
REM Formula Student Telemetry - Windows Launcher
REM This script sets up the Python environment and launches the application

echo.
echo ========================================
echo  Formula Student Telemetry System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Could not create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Could not activate virtual environment
    pause
    exit /b 1
)

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error: Could not install dependencies
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Launch application
echo.
echo Starting Formula Student Telemetry System...
echo.
python app.py

REM If app exits, pause to see any error messages
pause
