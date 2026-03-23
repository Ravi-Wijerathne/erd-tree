#!/usr/bin/env python3

import sys
import os
import subprocess
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
os.chdir(ROOT_DIR)

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def log_info(msg):
    print(f"{BLUE}[INFO]{NC} {msg}")


def log_success(msg):
    print(f"{GREEN}[SUCCESS]{NC} {msg}")


def log_warning(msg):
    print(f"{YELLOW}[WARNING]{NC} {msg}")


def log_error(msg):
    print(f"{RED}[ERROR]{NC} {msg}")


def run_command(cmd, check=True, capture=True, shell=False):
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture,
            text=True,
            shell=shell,
        )
        return result
    except subprocess.CalledProcessError as e:
        if capture:
            return e
        raise


def check_command(cmd):
    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd.split(),
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_python_command():
    if check_command(["python3", "--version"]):
        version_result = run_command(["python3", "--version"], check=False)
        log_success(f"Python found: {version_result.stdout.strip()}")
        return "python3"
    elif check_command(["python", "--version"]):
        version_result = run_command(["python", "--version"], check=False)
        log_success(f"Python found: {version_result.stdout.strip()}")
        return "python"
    return None


def get_python_version(python_cmd):
    result = run_command([python_cmd, "-c", "import sys; print(sys.version_info.major)"], check=False)
    major = int(result.stdout.strip()) if result.returncode == 0 else 0
    result = run_command([python_cmd, "-c", "import sys; print(sys.version_info.minor)"], check=False)
    minor = int(result.stdout.strip()) if result.returncode == 0 else 0
    return major, minor


def check_pip(python_cmd):
    result = run_command([python_cmd, "-m", "pip", "--version"], check=False)
    if result.returncode == 0:
        log_success(f"pip found: {result.stdout.split()[1]}")
        return True
    return False


def check_tkinter(python_cmd):
    result = run_command([python_cmd, "-c", "import tkinter"], check=False)
    return result.returncode == 0


def get_venvActivate_path():
    if sys.platform == "win32" or os.environ.get("OSTYPE", "").startswith("msys"):
        return ROOT_DIR / "venv" / "Scripts" / "activate"
    return ROOT_DIR / "venv" / "bin" / "activate"


def main():
    print("=" * 50)
    print("  Directory Tree Generator - Startup Script")
    print("=" * 50)
    print()

    log_info("Checking Python installation...")
    python_cmd = get_python_command()

    if not python_cmd:
        log_error("Python is not installed!")
        log_info("Please install Python 3.7+ from https://www.python.org/")
        sys.exit(1)

    major, minor = get_python_version(python_cmd)
    if major < 3 or (major == 3 and minor < 7):
        log_error(f"Python 3.7+ is required. Current version: {major}.{minor}")
        sys.exit(1)

    log_info("Checking pip installation...")
    if not check_pip(python_cmd):
        log_warning("pip not found. Please install pip manually.")
        sys.exit(1)

    log_info("Checking tkinter installation...")
    if not check_tkinter(python_cmd):
        log_warning("tkinter not found. Please install it manually.")
        log_info("On Linux: sudo apt-get install python3-tk")
        log_info("On macOS: brew install python-tk@3.11")
        sys.exit(1)
    log_success("tkinter is installed")

    log_info("Checking virtual environment...")
    if (ROOT_DIR / "venv").is_dir():
        log_success("Virtual environment found")
    else:
        log_info("Creating virtual environment...")
        run_command([python_cmd, "-m", "venv", "venv"], check=False)
        log_success("Virtual environment created")

    log_info("Activating virtual environment...")

    venv_python = None
    if sys.platform == "win32":
        venv_python = ROOT_DIR / "venv" / "Scripts" / "python.exe"
    else:
        venv_python = ROOT_DIR / "venv" / "bin" / "python"

    if not venv_python.exists():
        log_error("Virtual environment python not found")
        sys.exit(1)
    log_success("Virtual environment activated")

    log_info("Upgrading pip in virtual environment...")
    run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=False)
    log_success("pip upgraded")

    log_info("Checking dependencies...")
    requirements_file = ROOT_DIR / "requirements.txt"
    if requirements_file.exists():
        log_info("Installing dependencies from requirements.txt...")
        run_command([str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)], check=False)
        log_success("Dependencies installed")
    else:
        log_warning("requirements.txt not found. Installing core dependencies...")
        run_command([str(venv_python), "-m", "pip", "install", "requests"], check=False)
        log_success("Core dependencies installed")

    log_info("Checking main script...")
    main_script = ROOT_DIR / "dir_tree.py"
    if not main_script.exists():
        log_error(f"dir_tree.py not found in {ROOT_DIR}")
        sys.exit(1)
    log_success("Main script found")

    updater_script = ROOT_DIR / "scripts" / "updater.py"
    if updater_script.exists():
        log_info("Checking for updates...")
        try:
            sys.path.insert(0, str(ROOT_DIR))
            from scripts.updater import check_for_updates_gui
            check_for_updates_gui()
        except Exception:
            pass

    print()
    log_success("All prerequisites met. Launching Directory Tree Generator...")
    print("=" * 50)
    print()

    try:
        exit_code = subprocess.call([str(venv_python), str(main_script)])
    except KeyboardInterrupt:
        exit_code = 0

    print()
    print("=" * 50)
    if exit_code == 0:
        log_success("Application closed successfully")
    else:
        log_error(f"Application exited with code: {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
