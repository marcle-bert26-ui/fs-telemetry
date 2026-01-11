# Installation Guide

Complete step-by-step installation guide for Formula Student Telemetry System on all platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Windows Installation](#windows-installation)
- [Linux Installation](#linux-installation)
- [macOS Installation](#macos-installation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)

### Optional
- Virtual environment tool (venv, conda)
- Arduino hardware (for LIVE mode)
- USB cable for Arduino connection

## Windows Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Clone Repository

```cmd
git clone https://github.com/yourusername/fs-telemetry.git
cd fs-telemetry
```

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

### Step 5: Configure Arduino Port

Edit `config.py`:
```python
SERIAL_PORT = "COM3"  # Check Device Manager for your port
SERIAL_BAUDRATE = 115200
```

To find your Arduino port:
1. Connect Arduino via USB
2. Open Device Manager
3. Look under "Ports (COM & LPT)"
4. Arduino will appear as "COM3" (or similar)

### Step 6: Run Application

```cmd
python app.py
```

### Windows: Standalone EXE

If you prefer a standalone Windows executable (no Python required), a build is provided in `dist/FormulaTelementry.exe` when using the provided build scripts. To run the EXE:

```cmd
dist\FormulaTelementry.exe
```

To build the EXE locally (requires Python and PyInstaller):

```cmd
py -m pip install pyinstaller
py -m PyInstaller --onefile --windowed --name FormulaTelementry --hidden-import=PyQt5 --hidden-import=pyserial app.py
```

The generated file will be at `dist\FormulaTelementry.exe`.

You can distribute that EXE directly to other Windows users.

---

## Build Checklist for Linux

- [ ] Install Python 3.8+ and pip
- [ ] Create and activate a virtual environment
- [ ] pip install -r requirements.txt (note: CI uses `requirements-ci.txt` without PyQt5)
- [ ] Install `pyinstaller` and optional `appimagetool` for AppImage packaging
- [ ] Build with PyInstaller on Linux runner:

```bash
python3 -m pip install pyinstaller
python3 -m PyInstaller --onefile --name FormulaTelementry app.py
```

- [ ] (Optional) Create AppImage from the one-file binary or from a directory build

Notes:
- Linux builds should be produced on Linux (e.g., `ubuntu-latest` in GitHub Actions). Building on other OSes may produce incompatible binaries.

---

## Build Checklist for macOS

- [ ] Use a macOS machine or `macos-latest` GitHub Actions runner
- [ ] Install Python 3.8+ and pip
- [ ] Create and activate a virtual environment
- [ ] pip install -r requirements.txt
- [ ] Install `pyinstaller` or `py2app` for native .app bundling
- [ ] Build with PyInstaller on macOS runner:

```bash
python3 -m pip install pyinstaller
python3 -m PyInstaller --onefile --name FormulaTelementry app.py
```

- [ ] To create a `.app` bundle use `py2app` or PyInstaller with `--windowed` and `--onedir`, then package to `.dmg` if desired.

Notes:
- macOS builds must be performed on macOS to be compatible with macOS users.
- Code signing and notarization may be required for distribution to end users (Apple Developer account).

## Linux Installation

### Step 1: Install Python and Git

Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv git
```

Fedora/RHEL:
```bash
sudo dnf install python3 python3-pip git
```

Arch:
```bash
sudo pacman -S python python-pip git
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/fs-telemetry.git
cd fs-telemetry
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Arduino Port

Edit `config.py`:
```python
SERIAL_PORT = "/dev/ttyUSB0"  # or /dev/ttyACM0
SERIAL_BAUDRATE = 115200
```

To find your Arduino port:
```bash
ls /dev/tty*
# or
dmesg | grep -i usb
```

### Step 6: Set USB Permissions (if needed)

```bash
sudo usermod -a -G dialout $USER
newgrp dialout
```

### Step 7: Run Application

```bash
python app.py
```

## macOS Installation

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

```bash
brew install python3 git
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/fs-telemetry.git
cd fs-telemetry
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Arduino Port

Edit `config.py`:
```python
SERIAL_PORT = "/dev/cu.usbserial-1410"  # Check your port
SERIAL_BAUDRATE = 115200
```

To find your Arduino port:
```bash
ls /dev/cu.*
```

### Step 7: Run Application

```bash
python app.py
```

## Post-Installation

### Verify Installation

```bash
# Test imports
python -c "import PyQt5; print('PyQt5 OK')"
python -c "import serial; print('pyserial OK')"
python -c "import pytest; print('pytest OK')"

# Run tests
pytest tests/ -v
```

### First Run Checklist

- [ ] Python and pip installed
- [ ] Dependencies installed successfully
- [ ] Arduino port configured correctly
- [ ] All tests passing
- [ ] Application launches successfully
- [ ] Can access both LIVE and REPLAY modes

## Troubleshooting

### Python not found

**Error**: `python: command not found`

**Windows**:
- Reinstall Python with "Add Python to PATH" checked
- Or add Python to PATH manually

**Linux/macOS**:
```bash
which python3
alias python=python3
```

### Module not found

**Error**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solution**:
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Then install
pip install PyQt5
```

### Arduino not detected

**Error**: `Failed to connect: could not open port 'COM3'`

**Solutions**:
1. Check USB cable connection
2. Verify Arduino port in Device Manager/terminal
3. Install USB drivers (CH340 if needed)
4. Update `config.py` with correct port
5. Test with Arduino IDE to verify port

**Linux specific**:
```bash
# Check permissions
ls -l /dev/ttyUSB*
# Fix permissions
sudo usermod -a -G dialout $USER
```

### PyQt5 installation fails

**Error**: `Could not build wheels for PyQt5`

**Windows**:
- Ensure Visual C++ Build Tools installed
- Or use pre-built wheel: `pip install --only-binary :all: PyQt5`

**Linux**:
```bash
sudo apt-get install python3-dev
pip install PyQt5
```

**macOS**:
```bash
brew install qt5
pip install PyQt5
```

### Permission denied errors

**Linux/macOS**:
```bash
# Make scripts executable
chmod +x *.py
```

### Virtual environment issues

**Recreate virtual environment**:
```bash
# Linux/macOS
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Updating Installation

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Update packages
pip install --upgrade -r requirements.txt
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Remove cloned repository
rm -rf fs-telemetry  # Linux/macOS
rmdir /s fs-telemetry  # Windows
```

## Getting Help

- Check [README_APP.md](README_APP.md) for general info
- Review [Common Issues](#troubleshooting)
- Check GitHub [Issues](https://github.com/yourusername/fs-telemetry/issues)
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development help

---

For additional help, please open an issue on GitHub with:
- Your operating system and version
- Python version (`python --version`)
- Error message and stack trace
- Steps to reproduce
