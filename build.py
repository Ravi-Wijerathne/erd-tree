#!/usr/bin/env python3
"""
Build script for Directory Tree Generator
Creates portable executable and installer packages
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Failed to run command: {cmd}")
        print(f"Error: {e}")
        return False

def create_portable_version():
    """Create portable executable using PyInstaller"""
    print("Creating portable version...")

    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # PyInstaller command for portable executable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",  # Use windowed mode for GUI
        "--name=dir_tree_portable",
        "--add-data=README.md;.",
        "--hidden-import=tkinter",
        "--hidden-import=platform",
        "--hidden-import=requests",
        "dir_tree.py"
    ]

    if platform.system() == "Windows":
        # Windows specific options
        pass
    elif platform.system() == "Darwin":  # macOS
        cmd.extend([
            "--hidden-import=AppKit",
            "--hidden-import=Foundation"
        ])
    elif platform.system() == "Linux":
        cmd.extend([
            "--hidden-import=gi",
            "--hidden-import=gi.repository"
        ])

    success = run_command(" ".join(cmd))
    if success:
        print("Portable version created successfully!")
        print("Location: dist/dir_tree_portable.exe" if platform.system() == "Windows" else "dist/dir_tree_portable")
    return success

def create_installer():
    """Create installer package"""
    print("Creating installer...")

    system = platform.system().lower()

    if system == "windows":
        return create_windows_installer()
    elif system == "darwin":
        return create_macos_installer()
    elif system == "linux":
        return create_linux_installer()
    else:
        print(f"Installer creation not supported for {system}")
        return False

def create_windows_installer():
    """Create Windows installer using NSIS"""
    print("Creating Windows NSIS installer...")

    # Check if makensis is available
    if not run_command("makensis /VERSION"):
        print("NSIS not found. Please install NSIS from https://nsis.sourceforge.io/")
        return False

    # Create NSIS script
    nsis_script = f"""
!include "MUI2.nsh"
!include "FileFunc.nsh"

Name "Directory Tree Generator"
OutFile "dist/DirectoryTreeGenerator_Setup.exe"
Unicode True
InstallDir "$PROGRAMFILES\\Directory Tree Generator"
InstallDirRegKey HKCU "Software\\DirectoryTreeGenerator" ""

!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File "dist\\dir_tree_portable.exe"
    File "README.md"

    # Create desktop shortcut
    CreateShortCut "$DESKTOP\\Directory Tree Generator.lnk" "$INSTDIR\\dir_tree_portable.exe"

    # Create start menu shortcut
    CreateDirectory "$SMPROGRAMS\\Directory Tree Generator"
    CreateShortCut "$SMPROGRAMS\\Directory Tree Generator\\Directory Tree Generator.lnk" "$INSTDIR\\dir_tree_portable.exe"
    CreateShortCut "$SMPROGRAMS\\Directory Tree Generator\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"

    # Registry information for add/remove programs
    WriteRegStr HKCU "Software\\DirectoryTreeGenerator" "" $INSTDIR
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\DirectoryTreeGenerator" "DisplayName" "Directory Tree Generator"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\DirectoryTreeGenerator" "UninstallString" "$INSTDIR\\Uninstall.exe"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\DirectoryTreeGenerator" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\DirectoryTreeGenerator" "NoRepair" 1

    WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\dir_tree_portable.exe"
    Delete "$INSTDIR\\README.md"
    Delete "$INSTDIR\\Uninstall.exe"

    Delete "$DESKTOP\\Directory Tree Generator.lnk"
    Delete "$SMPROGRAMS\\Directory Tree Generator\\Directory Tree Generator.lnk"
    Delete "$SMPROGRAMS\\Directory Tree Generator\\Uninstall.lnk"
    RMDir "$SMPROGRAMS\\Directory Tree Generator"

    DeleteRegKey HKCU "Software\\DirectoryTreeGenerator"
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\DirectoryTreeGenerator"

    RMDir "$INSTDIR"
SectionEnd
"""

    with open("installer.nsi", "w") as f:
        f.write(nsis_script)

    success = run_command("makensis installer.nsi")
    if success:
        print("Windows installer created: dist/DirectoryTreeGenerator_Setup.exe")
        os.remove("installer.nsi")
    return success

def create_macos_installer():
    """Create macOS installer"""
    print("Creating macOS installer...")

    # Create app bundle structure
    app_name = "Directory Tree Generator.app"
    contents_dir = f"dist/{app_name}/Contents"
    macos_dir = f"{contents_dir}/MacOS"
    resources_dir = f"{contents_dir}/Resources"

    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)

    # Copy executable
    shutil.copy("dist/dir_tree_portable", f"{macos_dir}/Directory Tree Generator")

    # Create Info.plist
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Directory Tree Generator</string>
    <key>CFBundleIdentifier</key>
    <string>com.directorytree.generator</string>
    <key>CFBundleName</key>
    <string>Directory Tree Generator</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
"""

    with open(f"{contents_dir}/Info.plist", "w") as f:
        f.write(info_plist)

    print(f"macOS app bundle created: dist/{app_name}")
    return True

def create_linux_installer():
    """Create Linux installer (AppImage or DEB)"""
    print("Creating Linux AppImage...")

    # For now, just create a simple tar.gz package
    # In a real scenario, you'd use tools like appimagetool or dpkg-deb

    package_name = "directory-tree-generator-linux"
    os.makedirs(f"dist/{package_name}", exist_ok=True)

    # Copy files
    shutil.copy("dist/dir_tree_portable", f"dist/{package_name}/dir_tree")
    shutil.copy("README.md", f"dist/{package_name}/")

    # Create desktop file
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Directory Tree Generator
Comment=Generate directory tree structure
Exec=./dir_tree
Icon=folder
Terminal=false
Categories=Utility;FileTools;
"""

    with open(f"dist/{package_name}/directory-tree-generator.desktop", "w") as f:
        f.write(desktop_content)

    # Create run script
    run_script = """#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"
./dir_tree "$@"
"""

    with open(f"dist/{package_name}/run.sh", "w") as f:
        f.write(run_script)

    os.chmod(f"dist/{package_name}/run.sh", 0o755)
    os.chmod(f"dist/{package_name}/dir_tree", 0o755)

    # Create tar.gz archive
    success = run_command(f"tar -czf dist/{package_name}.tar.gz -C dist {package_name}")
    if success:
        print(f"Linux package created: dist/{package_name}.tar.gz")
        shutil.rmtree(f"dist/{package_name}")
    return success

def main():
    """Main build function"""
    import argparse

    parser = argparse.ArgumentParser(description="Build Directory Tree Generator")
    parser.add_argument("--portable-only", action="store_true",
                       help="Build portable executable only")
    parser.add_argument("--installer-only", action="store_true",
                       help="Build installer only")

    args = parser.parse_args()

    print("Directory Tree Generator - Build Script")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("dir_tree.py"):
        print("Error: dir_tree.py not found. Please run this script from the project root.")
        sys.exit(1)

    # Determine what to build
    build_portable = not args.installer_only
    build_installer = not args.portable_only

    # Create portable version
    if build_portable:
        if not create_portable_version():
            print("Failed to create portable version")
            sys.exit(1)

    # Create installer
    if build_installer:
        if not create_installer():
            print("Failed to create installer")
            sys.exit(1)

    print("\nBuild completed successfully!")
    print("Files created:")
    for file in Path("dist").glob("*"):
        print(f"  - {file}")

if __name__ == "__main__":
    main()