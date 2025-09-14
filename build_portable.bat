@echo off
echo Building Directory Tree Generator Portable Version...
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
py -m pip install pyinstaller requests

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build portable executable
echo Building portable executable...
py -m PyInstaller --onefile --windowed --name dir_tree_portable --hidden-import tkinter --hidden-import platform --hidden-import requests dir_tree.py

REM Check if build was successful
if exist "dist\dir_tree_portable.exe" (
    echo.
    echo ✅ Build successful!
    echo Portable executable created: dist\dir_tree_portable.exe
    echo File size: 
    powershell -command "Get-ChildItem 'dist\dir_tree_portable.exe' | Select-Object Length"
    echo.
    echo You can now distribute this file - no installation required!
) else (
    echo.
    echo ❌ Build failed! Check the output above for errors.
)

pause