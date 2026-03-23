#!/bin/bash

# Directory Tree Generator - Automated Startup Script
# This script checks prerequisites, installs dependencies, and launches the tool

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print header
echo "=============================================="
echo "  Directory Tree Generator - Startup Script"
echo "=============================================="
echo ""

# 1. Check Python installation
log_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    log_success "Python found: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    log_success "Python found: $PYTHON_VERSION"
else
    log_error "Python is not installed!"
    log_info "Please install Python 3.7+ from https://www.python.org/"
    
    # Try to install Python on different systems
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_info "Attempting to install Python on Linux..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-tk
            PYTHON_CMD="python3"
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip python3-tkinter
            PYTHON_CMD="python3"
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip python3-tkinter
            PYTHON_CMD="python3"
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python python-pip tk
            PYTHON_CMD="python3"
        else
            log_error "Could not auto-install Python. Please install manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "Attempting to install Python on macOS..."
        if command -v brew &> /dev/null; then
            brew install python3 python-tk@3.11
            PYTHON_CMD="python3"
        else
            log_error "Homebrew not found. Please install Python manually."
            exit 1
        fi
    else
        log_error "Could not auto-install Python. Please install manually."
        exit 1
    fi
fi

# Check Python version (minimum 3.7)
PYTHON_VERSION_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_VERSION_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [[ $PYTHON_VERSION_MAJOR -lt 3 ]] || [[ $PYTHON_VERSION_MAJOR -eq 3 && $PYTHON_VERSION_MINOR -lt 7 ]]; then
    log_error "Python 3.7+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# 2. Check pip installation
log_info "Checking pip installation..."
if $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_VERSION=$($PYTHON_CMD -m pip --version | awk '{print $2}')
    log_success "pip found: $PIP_VERSION"
else
    log_warning "pip not found. Installing pip..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pip
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-pip
        fi
    fi
    
    # Verify pip installation
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        log_error "Failed to install pip"
        exit 1
    fi
    log_success "pip installed successfully"
fi

# 3. Check tkinter installation
log_info "Checking tkinter installation..."
if $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
    log_success "tkinter is installed"
else
    log_warning "tkinter not found. Installing tkinter..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-tk
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-tkinter
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm tk
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install python-tk@3.11
        fi
    fi
    
    # Verify tkinter installation
    if ! $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
        log_error "Failed to install tkinter. Please install it manually."
        exit 1
    fi
    log_success "tkinter installed successfully"
fi

# 4. Check if virtual environment exists
log_info "Checking virtual environment..."
if [ -d "venv" ]; then
    log_success "Virtual environment found"
else
    log_info "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    log_success "Virtual environment created"
fi

# 5. Activate virtual environment
log_info "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
log_success "Virtual environment activated"

# 6. Upgrade pip in virtual environment
log_info "Upgrading pip in virtual environment..."
python -m pip install --upgrade pip -q
log_success "pip upgraded"

# 7. Check and install dependencies from requirements.txt
log_info "Checking dependencies..."
if [ -f "requirements.txt" ]; then
    log_info "Installing dependencies from requirements.txt..."
    python -m pip install -r requirements.txt -q
    log_success "Dependencies installed"
else
    log_warning "requirements.txt not found. Installing core dependencies..."
    python -m pip install requests -q
    log_success "Core dependencies installed"
fi

# 8. Verify main script exists
log_info "Checking main script..."
if [ ! -f "dir_tree.py" ]; then
    log_error "dir_tree.py not found in $ROOT_DIR"
    exit 1
fi
log_success "Main script found"

# 9. Check for updates (if updater is available)
if [ -f "scripts/updater.py" ]; then
    log_info "Checking for updates..."
    python -c "from scripts.updater import check_for_updates_gui; check_for_updates_gui()" 2>/dev/null || true
fi

# 10. Launch the application
echo ""
log_success "All prerequisites met. Launching Directory Tree Generator..."
echo "=============================================="
echo ""

# Run the application
python dir_tree.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "=============================================="
if [ $EXIT_CODE -eq 0 ]; then
    log_success "Application closed successfully"
else
    log_error "Application exited with code: $EXIT_CODE"
fi

# Deactivate virtual environment
deactivate 2>/dev/null || true

exit $EXIT_CODE
