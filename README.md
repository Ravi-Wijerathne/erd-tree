# Directory Tree Generator v1.0.0

A powerful, cross-platform tool for generating visual directory tree structures with multiple output formats, context menu integration, and automatic updates.

![Cross-platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ✨ Features

- 🔄 **Cross-Platform**: Native support for Windows, Linux, and macOS
- 📁 **Multiple Formats**: Text, Markdown, and HTML output
- 🖥️ **Dual Interface**: GUI and Command-Line modes
- 📎 **Context Menu**: Right-click integration on all platforms
- 🔄 **Auto-Updater**: Automatic update checking and installation
- 📦 **Portable Version**: Run without installation
- 🏗️ **Professional Installer**: Windows installer with uninstaller
- ⚡ **Fast & Lightweight**: Minimal dependencies, quick execution

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Using the Portable Version](#-using-the-portable-version)
- [Command Line Interface](#-command-line-interface)
- [Graphical User Interface](#-graphical-user-interface)
- [Context Menu Integration](#-context-menu-integration)
- [Auto-Updater](#-auto-updater)
- [Building from Source](#-building-from-source)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

### Option 1: Download Pre-built Portable Version

1. **Download** the latest release from [GitHub Releases](https://github.com/Ravi-Wijerathne/erd-tree/releases)
2. **Extract** the portable executable
3. **Run** the executable directly - no installation required!

```bash
# Windows
dir_tree_portable.exe /path/to/directory

# Linux/macOS
./dir_tree_portable /path/to/directory
```

### Option 2: Install Professional Version

1. **Download** the installer for your platform
2. **Run** the installer (may require administrator privileges)
3. **Launch** from desktop shortcut or start menu

---

## 📥 Installation

### Method 1: Professional Installer (Recommended)

#### Windows
1. Download `DirectoryTreeGenerator_Setup.exe` from [Releases](https://github.com/Ravi-Wijerathne/erd-tree/releases)
2. Run the installer executable
3. Follow the installation wizard
4. Choose whether to add context menu integration
5. Launch from desktop shortcut or Start Menu

#### Linux
```bash
# Download the Linux package
wget https://github.com/Ravi-Wijerathne/erd-tree/releases/download/v1.0.0/directory-tree-generator-linux.tar.gz

# Extract and run
tar -xzf directory-tree-generator-linux.tar.gz
cd directory-tree-generator-linux
./run.sh /path/to/directory
```

#### macOS
```bash
# Download the macOS app bundle
curl -L -o DirectoryTreeGenerator.dmg https://github.com/Ravi-Wijerathne/erd-tree/releases/download/v1.0.0/DirectoryTreeGenerator.dmg

# Mount and install
hdiutil attach DirectoryTreeGenerator.dmg
cp -r /Volumes/DirectoryTreeGenerator/Directory\ Tree\ Generator.app /Applications/
```

### Method 2: From Source Code

#### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning)

#### Step-by-Step Installation

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/Ravi-Wijerathne/erd-tree.git
   cd erd-tree
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   # GUI Mode (default)
   python dir_tree.py

   # CLI Mode
   python dir_tree.py /path/to/directory
   ```

4. **Optional: Create Portable Executable**
   ```bash
   pip install pyinstaller
   python build.py --portable-only
   ```

### Method 3: System Package Managers

#### Using pip (Global Installation)
```bash
pip install git+https://github.com/Ravi-Wijerathne/erd-tree.git
dir_tree /path/to/directory
```

---

## 📱 Using the Portable Version

The portable version is perfect for:
- USB drives
- Shared computers
- Testing environments
- Systems without admin rights

### Getting the Portable Version

1. **Download** from [GitHub Releases](https://github.com/Ravi-Wijerathne/erd-tree/releases)
2. **Extract** the ZIP file to any location
3. **Run** the executable directly

### Portable Version Features

- ✅ **No Installation Required**: Just download and run
- ✅ **No Admin Rights Needed**: Works on restricted systems
- ✅ **Self-Contained**: All dependencies included
- ✅ **Cross-Platform**: Same executable works everywhere
- ✅ **USB-Friendly**: Perfect for portable drives

### Using Portable Version

#### Basic Usage
```bash
# Windows
dir_tree_portable.exe "C:\Users\YourName\Documents"

# Linux/macOS
./dir_tree_portable /home/username/Documents
```

#### Advanced Usage
```bash
# Generate Markdown format
./dir_tree_portable /path/to/folder -f markdown -o tree.md

# Use CLI mode without GUI
./dir_tree_portable /path/to/folder --no-gui

# Setup context menu (requires admin/sudo)
./dir_tree_portable --setup-context-menu
```

### Portable Version Limitations

- Context menu integration requires admin/sudo privileges
- Auto-updater may not work on restricted systems
- Some system integrations may be limited

---

## 💻 Command Line Interface

The CLI provides full functionality for power users and automation.

### Basic Syntax
```bash
python dir_tree.py [directory] [options]
```

### CLI Options

| Option | Description | Example |
|--------|-------------|---------|
| `directory` | Target directory path | `/home/user/docs` |
| `-f, --format` | Output format (text/markdown/html) | `-f markdown` |
| `-o, --output` | Custom output file path | `-o tree.md` |
| `--no-gui` | Force CLI mode | `--no-gui` |
| `--setup-context-menu` | Setup context menu | `--setup-context-menu` |
| `--remove-context-menu` | Remove context menu | `--remove-context-menu` |
| `--check-updates` | Check for updates | `--check-updates` |

### CLI Examples

#### Generate Tree in Different Formats
```bash
# Plain text (default)
python dir_tree.py /home/user/projects

# Markdown format
python dir_tree.py /home/user/projects -f markdown -o projects.md

# HTML format with custom output
python dir_tree.py /home/user/projects -f html -o projects.html
```

#### Context Menu Management
```bash
# Setup context menu integration
python dir_tree.py --setup-context-menu

# Remove context menu integration
python dir_tree.py --remove-context-menu
```

#### Advanced Usage
```bash
# Generate tree without GUI (headless)
python dir_tree.py /path/to/folder --no-gui

# Custom output location
python dir_tree.py /path/to/folder -o /tmp/my_tree.txt

# Combine multiple options
python dir_tree.py /path/to/folder -f markdown -o tree.md --no-gui
```

### CLI Output
```
Directory tree generated successfully: /path/to/folder/folder_tree_20250915_143022.txt
```

---

## 🖥️ Graphical User Interface

The GUI provides an intuitive interface for users who prefer visual interaction.

### Starting the GUI

#### From Installer
- Click desktop shortcut or Start Menu entry

#### From Source
```bash
python dir_tree.py
```

#### From Portable Version
```bash
./dir_tree_portable.exe  # Windows
./dir_tree_portable      # Linux/macOS
```

### GUI Features

#### Main Window
- **Folder Selection**: Browse button to choose directory
- **Format Selection**: Radio buttons for Text/Markdown/HTML
- **Generate Button**: Creates the directory tree
- **Context Menu Buttons**: Setup/remove integration

#### Menu Bar
- **File**: Exit application
- **Tools**: Check for updates
- **Help**: About dialog

### Step-by-Step GUI Usage

1. **Launch** the application
2. **Click "Browse"** to select a folder
3. **Choose output format** (Text/Markdown/HTML)
4. **Click "Generate Tree"** to create the file
5. **View the result** in the selected folder

### GUI Screenshots

```
Directory Tree Generator - Windows
┌─────────────────────────────────────┐
│ Select Folder: [C:\Users\... ] [Browse] │
│                                       │
│ Output Format:                        │
│ ○ Plain Text    ● Markdown    ○ HTML │
│                                       │
│ [Generate Tree]                       │
│                                       │
│ [Add Context Menu] [Remove Context Menu] │
└─────────────────────────────────────┘
```

---

## 📎 Context Menu Integration

Add the tool to your system's right-click context menu for quick access.

### Windows Context Menu

#### Automatic Setup (Recommended)
```bash
python dir_tree.py --setup-context-menu
```

#### Manual Setup
1. Right-click any folder in Windows Explorer
2. The "Generate Directory Tree" option appears
3. Click to generate tree automatically

#### Registry Location
```
HKEY_CLASSES_ROOT\Directory\shell\GenerateTree
```

### Linux Context Menu (GNOME/Nautilus)

#### Setup
```bash
python dir_tree.py --setup-context-menu
```

#### Usage
1. Right-click any folder in Nautilus
2. Select "Generate Directory Tree"
3. Tree file is created automatically

#### Desktop File Location
```
~/.local/share/applications/generate-directory-tree.desktop
```

### macOS Context Menu (Finder)

#### Setup
```bash
python dir_tree.py --setup-context-menu
```

#### Usage
1. Right-click any folder in Finder
2. Go to Services → Generate Directory Tree
3. Tree file is created automatically

#### Service Location
```
~/Library/Services/Generate Directory Tree.workflow/
```

### Removing Context Menu

#### All Platforms
```bash
python dir_tree.py --remove-context-menu
```

#### Platform-Specific Removal
- **Windows**: Removes registry entries
- **Linux**: Deletes .desktop file
- **macOS**: Removes service workflow

---

## 🔄 Auto-Updater

The built-in auto-updater keeps your installation current.

### How It Works

1. **Checks GitHub Releases** for new versions
2. **Compares versions** with current installation
3. **Downloads updates** automatically
4. **Installs updates** with backup
5. **Restarts application** if needed

### Using the Auto-Updater

#### GUI Method
1. Open the application
2. Go to **Tools → Check for Updates**
3. Follow the update wizard

#### CLI Method
```bash
python dir_tree.py --check-updates
```

#### Automatic Checking
- Runs on application startup (optional)
- Checks weekly for updates
- Notifies when updates are available

### Update Process

1. **Update Available Dialog**
   ```
   ┌─ Update Available ──────────────────┐
   │ A new version is available: v1.1.0   │
   │                                       │
   │ What's new:                           │
   │ • Bug fixes                          │
   │ • Performance improvements          │
   │                                       │
   │ [Download & Install] [Skip]          │
   └─────────────────────────────────────┘
   ```

2. **Download Progress**
   ```
   ┌─ Downloading Update ────────────────┐
   │ ┌─────────────────────────────────┐ │
   │ │███████████████████████░ 85%    │ │
   │ └─────────────────────────────────┘ │
   │                                       │
   │ Downloading update...                │
   └─────────────────────────────────────┘
   ```

3. **Installation Complete**
   ```
   ┌─ Update Complete ───────────────────┐
   │ Update installed successfully!       │
   │                                       │
   │ The application will restart now.    │
   │                                       │
   │ [OK]                                 │
   └─────────────────────────────────────┘
   ```

### Update Safety

- ✅ **Backup Creation**: Current version backed up
- ✅ **Rollback Support**: Can revert if needed
- ✅ **Version Validation**: Only installs compatible updates
- ✅ **Network Security**: HTTPS downloads with verification

---

## 🏗️ Building from Source

Build your own versions for development or custom deployment.

### Prerequisites
- Python 3.7+
- PyInstaller (for portable executables)
- NSIS (for Windows installer, optional)
- Make (optional)

### Quick Build
```bash
# Install build dependencies
pip install -r requirements.txt

# Build everything
python build.py

# Or use Make
make all
```

### Build Targets

| Command | Description |
|---------|-------------|
| `make portable` | Build portable executable only |
| `make installer` | Build installer only |
| `make windows` | Windows-specific build |
| `make linux` | Linux-specific build |
| `make macos` | macOS-specific build |
| `make clean` | Remove build artifacts |
| `make release` | Create release package |

### Build Output

```
dist/
├── dir_tree_portable.exe          # Portable executable
├── DirectoryTreeGenerator_Setup.exe  # Windows installer
├── directory-tree-generator-linux.tar.gz  # Linux package
└── Directory Tree Generator.app/   # macOS app bundle
```

### Custom Build Options

```bash
# Build portable only
python build.py --portable-only

# Build installer only
python build.py --installer-only

# Custom PyInstaller options
pyinstaller --onefile --windowed --name custom_name dir_tree.py
```

---

## ⚙️ Configuration

### Configuration Files

#### Settings File (Windows)
```
%APPDATA%\Directory Tree Generator\settings.ini
```

#### Settings File (Linux/macOS)
```
~/.config/directory-tree-generator/settings.ini
```

### Configuration Options

```ini
[Settings]
ContextMenu=1          ; 1=enabled, 0=disabled
AutoUpdate=1           ; 1=enabled, 0=disabled
DefaultFormat=text     ; text/markdown/html
OutputDirectory=       ; Custom output directory (empty=auto)
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DIRTREE_CONFIG` | Custom config file path | Auto-detected |
| `DIRTREE_DEBUG` | Enable debug logging | `false` |
| `DIRTREE_NO_UPDATE` | Disable auto-updater | `false` |

---

## 🔧 Troubleshooting

### Common Issues

#### Application Won't Start

**Problem**: GUI doesn't appear or crashes on startup

**Solutions**:
```bash
# Check Python version
python --version

# Install missing dependencies
pip install -r requirements.txt

# Run in CLI mode for debugging
python dir_tree.py --no-gui /path/to/folder

# Check for tkinter
python -c "import tkinter; print('Tkinter OK')"
```

#### Context Menu Not Working

**Problem**: Right-click option doesn't appear

**Solutions**:
```bash
# Windows: Run as administrator
python dir_tree.py --setup-context-menu

# Linux: Restart file manager
killall nautilus && nautilus &

# macOS: Restart Finder
killall Finder && open /System/Library/CoreServices/Finder.app
```

#### Permission Errors

**Problem**: "Access denied" or permission errors

**Solutions**:
```bash
# Windows: Run as administrator
# Linux/macOS: Use sudo for system-wide installation
sudo python dir_tree.py --setup-context-menu

# Check directory permissions
ls -la /path/to/directory
```

#### Update Download Fails

**Problem**: Auto-updater can't download updates

**Solutions**:
```bash
# Check internet connection
ping github.com

# Manual download from releases page
# Extract and replace executable manually

# Disable firewall/antivirus temporarily
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Set environment variable
export DIRTREE_DEBUG=true

# Run with debug output
python dir_tree.py
```

### Getting Help

1. **Check the logs** (if debug mode enabled)
2. **Try CLI mode** to isolate GUI issues
3. **Test with simple directory** to rule out permission issues
4. **Check GitHub Issues** for similar problems
5. **Create an issue** with system information

---

## 📖 Examples

### Basic Usage

#### Generate Simple Tree
```bash
python dir_tree.py /home/user/documents
```
Output: `documents_tree_20250915_143022.txt`

#### Generate Markdown Tree
```bash
python dir_tree.py /home/user/projects -f markdown -o projects.md
```
Output: Custom markdown file with project structure

### Advanced Examples

#### Batch Processing
```bash
# Process multiple directories
for dir in /home/user/*/; do
    python dir_tree.py "$dir" -f html
done
```

#### Integration with Other Tools
```bash
# Generate tree and open in editor
python dir_tree.py /home/user/code -f markdown -o tree.md
code tree.md  # Open in VS Code
```

#### Automated Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/home/user/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Generate tree of current state
python dir_tree.py /home/user/documents -f markdown -o "$BACKUP_DIR/tree_$TIMESTAMP.md"

# Create backup archive
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" /home/user/documents
```

### Output Format Examples

#### Plain Text Output
```
Documents/
    |__Reports/
    |     |__annual_report.pdf
    |     |__quarterly_review.pdf
    |__Presentations/
          |__project_demo.pptx
```

#### Markdown Output
```markdown
- Documents/
    - Reports/
        - annual_report.pdf
        - quarterly_review.pdf
    - Presentations/
        - project_demo.pptx
```

#### HTML Output
```html
<div style="margin-left: 0px;">Documents/</div>
<div style="margin-left: 20px;">Reports/</div>
<div style="margin-left: 40px;">- annual_report.pdf</div>
<div style="margin-left: 40px;">- quarterly_review.pdf</div>
<div style="margin-left: 20px;">Presentations/</div>
<div style="margin-left: 40px;">- project_demo.pptx</div>
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

### Development Setup

1. **Fork** the repository
2. **Clone** your fork
   ```bash
   git clone https://github.com/yourusername/erd-tree.git
   cd erd-tree
   ```
3. **Set up development environment**
   ```bash
   make setup
   ```
4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

### Testing

```bash
# Run basic tests
make test

# Test builds
make portable
./dist/dir_tree_portable --help
```

### Code Style

- Follow PEP 8 Python style guide
- Use descriptive variable names
- Add docstrings to functions
- Test on multiple platforms

### Pull Request Process

1. **Update documentation** for any new features
2. **Add tests** for new functionality
3. **Ensure cross-platform compatibility**
4. **Update version numbers** if needed
5. **Create pull request** with detailed description

### Reporting Issues

When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE.txt](LICENSE.txt) file for details.

### Permissions
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

### Limitations
- ❌ No liability
- ❌ No warranty

### Conditions
- 📄 License and copyright notice must be included

---

## 🙏 Acknowledgments

- **Python Community** for the amazing ecosystem
- **PyInstaller** for portable executable creation
- **NSIS** for Windows installer framework
- **GitHub** for hosting and release management
- **Open Source Contributors** for their valuable input

---

## 📞 Support

### Getting Help

- 📖 **Documentation**: This README and [Wiki](https://github.com/Ravi-Wijerathne/erd-tree/wiki)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Ravi-Wijerathne/erd-tree/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Ravi-Wijerathne/erd-tree/discussions)
- 📧 **Email**: For security issues only

### Community

- ⭐ **Star** the repository if you find it useful
- 🍴 **Fork** to contribute improvements
- 📢 **Share** with others who might benefit
- 🔔 **Watch** for updates and new releases

---

*Made with ❤️ for developers and system administrators worldwide*

## Features

- **Cross-Platform Support**: Works on Windows, Linux, and macOS
- **Recursive Directory Traversal**: Generates a hierarchical tree structure of all files and subfolders within a selected folder
- **Multiple Output Formats**:
  - Plain Text: Simple indented structure
  - Markdown: Uses bullet points (`-`) for hierarchy
  - HTML: Generates a styled HTML document with proper indentation
- **Timestamped Output Files**: Each generated file includes a timestamp in its name for easy identification
- **Context Menu Integration**:
  - Windows: Registry-based context menu
  - Linux: .desktop file integration with Nautilus/GNOME
  - macOS: Services menu integration with Finder
- **Command-Line Interface**: Full CLI support for power users
- **User-Friendly GUI**: A graphical interface allows users to select folders, choose output formats, and manage context menu entries
- **Error Handling**: Handles invalid directories, permission errors, and other exceptions gracefully

---

## Installation

### Prerequisites
- Python 3.7 or higher installed on your system
- Administrator/root privileges (required for adding/removing context menu entries on some platforms)

### Steps to Install

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ravi-Wijerathne/erd-tree.git
   cd erd-tree
   ```

2. **Install Dependencies**:
   Ensure you have `pyinstaller` installed to create an executable (optional):
   ```bash
   pip install pyinstaller
   ```

3. **Create Executable** (Optional):
   Use `pyinstaller` to package the script into a standalone executable:
   ```bash
   pyinstaller --onefile dir_tree.py
   ```
   The executable will be located in the `dist/` folder.

4. **Run the Tool**:
   - **GUI Mode**: Double-click the executable or run `python dir_tree.py`
   - **CLI Mode**: Use command-line options (see Usage section below)

---

## Usage

### Command-Line Interface (CLI)

The tool now includes a comprehensive CLI for power users:

```bash
python dir_tree.py [directory] [options]
```

#### CLI Options

- `directory`: Path to the directory to generate tree for
- `-f, --format`: Output format (`text`, `markdown`, `html`) - default: `text`
- `-o, --output`: Custom output file path
- `--no-gui`: Force CLI mode
- `--setup-context-menu`: Setup context menu integration
- `--remove-context-menu`: Remove context menu integration

#### CLI Examples

```bash
# Generate text tree for current directory
python dir_tree.py /path/to/directory

# Generate markdown tree with custom output
python dir_tree.py /path/to/directory -f markdown -o tree.md

# Setup context menu integration
python dir_tree.py --setup-context-menu

# Force CLI mode (no GUI)
python dir_tree.py /path/to/directory --no-gui
```

### Using the GUI

1. Launch the tool by running `python dir_tree.py`
2. Click **Browse** to select the folder whose structure you want to generate
3. Choose the desired output format (Plain Text, Markdown, or HTML)
4. Click **Generate Tree** to create the directory tree file
5. The generated file will be saved in the selected folder with a timestamped filename

### Context Menu Integration

#### Windows
1. Run `python dir_tree.py --setup-context-menu` or use the GUI button
2. Right-click any folder in Windows Explorer
3. Select **Generate Directory Tree** from the context menu

#### Linux (GNOME/Nautilus)
1. Run `python dir_tree.py --setup-context-menu`
2. A `.desktop` file will be created in `~/.local/share/applications/`
3. Restart Nautilus or log out/in to see the context menu option
4. Right-click any folder and select **Generate Directory Tree**

#### macOS (Finder)
1. Run `python dir_tree.py --setup-context-menu`
2. A service will be created in `~/Library/Services/`
3. Right-click any folder in Finder
4. Go to **Services** → **Generate Directory Tree**

### Removing Context Menu Integration

```bash
python dir_tree.py --remove-context-menu
```

Or use the **Remove Context Menu Entry** button in the GUI.

## Cross-Platform Compatibility

This tool has been designed to work seamlessly across different operating systems:

- **Windows**: Uses Windows Registry for context menu integration
- **Linux**: Creates `.desktop` files for GNOME/Nautilus integration
- **macOS**: Creates Services for Finder integration

The tool automatically detects your operating system and uses the appropriate integration method. All core functionality (tree generation, multiple formats) works identically across platforms.

---

## Example Outputs

### Plain Text
```
Semester/
    |__1st Semester/
    |     |__Computers.pdf
    |     |__Machines.pdf
    |__2nd Semester/
          |__Network.pdf
```

### Markdown
```markdown
- Semester/
    - 1st Semester/
        - Computers.pdf
        - Machines.pdf
    - 2nd Semester/
        - Network.pdf
```

### HTML
```html
<div style="margin-left: 0px;">Semester/</div>
<div style="margin-left: 20px;">1st Semester/</div>
<div style="margin-left: 40px;">- Computers.pdf</div>
<div style="margin-left: 40px;">- Machines.pdf</div>
<div style="margin-left: 20px;">2nd Semester/</div>
<div style="margin-left: 40px;">- Network.pdf</div>
```

---

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add some feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

This project is licensed under the **MIT License**.

---

## Contact

For questions, feedback, or bug reports, feel free to reach out:

- GitHub: [@Ravi-Wijerathne](https://github.com/Ravi-Wijerathne)

---

## Packaging and Distribution

The project includes comprehensive build and packaging tools for creating distributable versions of the application.

### Building from Source

#### Prerequisites
- Python 3.7+
- PyInstaller (for portable executables)
- NSIS (for Windows installer, optional)
- Make (optional, for using Makefile)

#### Quick Build
```bash
# Install build dependencies
pip install -r requirements.txt

# Build everything
python build.py

# Or use Make (if available)
make all
```

#### Build Options
```bash
# Build portable executable only
python build.py --portable-only
# or
make portable

# Build installer only
python build.py --installer-only
# or
make installer

# Platform-specific builds
make windows    # Windows packages
make linux      # Linux packages
make macos      # macOS packages
```

### Portable Version

The portable version is a single executable file that doesn't require installation:

**Features:**
- No installation required
- Can run from any directory
- Includes all dependencies
- Cross-platform compatible

**Building:**
```bash
python build.py --portable-only
```

**Output:** `dist/dir_tree_portable` (or `.exe` on Windows)

### Windows Installer

Professional Windows installer with uninstaller and system integration:

**Features:**
- Proper Windows installer with wizard
- Creates desktop and start menu shortcuts
- Adds uninstaller to Windows Add/Remove Programs
- Optional context menu integration
- Registry integration

**Building:**
```bash
# Requires NSIS (Nullsoft Scriptable Install System)
makensis installer.nsi
```

**Output:** `DirectoryTreeGenerator_Setup.exe`

### Linux Packages

**AppImage:** Portable Linux application
**Tar.gz:** Simple archive for manual installation

**Building:**
```bash
make linux
```

### macOS Packages

**App Bundle:** Native macOS application bundle
**DMG:** Disk image for distribution

**Building:**
```bash
make macos
```

### Auto-Updater

The application includes an automatic update system:

**Features:**
- Checks GitHub releases for updates
- Downloads and installs updates automatically
- Cross-platform update support
- Progress indicators
- Backup of current version

**Usage:**
- **GUI:** Tools → Check for Updates
- **CLI:** `python dir_tree.py --check-updates`
- **Automatic:** Runs on startup (optional)

### Distribution Files

After building, you'll find these files in the `dist/` directory:

| Platform | File | Description |
|----------|------|-------------|
| All | `dir_tree_portable*` | Portable executable |
| Windows | `DirectoryTreeGenerator_Setup.exe` | Windows installer |
| Linux | `directory-tree-generator-linux.tar.gz` | Linux package |
| macOS | `Directory Tree Generator.app/` | macOS app bundle |

### Release Process

1. **Update version numbers** in:
   - `dir_tree.py` (CURRENT_VERSION)
   - `updater.py` (CURRENT_VERSION)
   - `installer.nsi` (version numbers)

2. **Build all packages:**
   ```bash
   make clean
   make all
   ```

3. **Test the builds** on target platforms

4. **Create GitHub release** with the built packages

5. **Update version numbers** for next release

### Development Setup

```bash
# Clone repository
git clone https://github.com/Ravi-Wijerathne/erd-tree.git
cd erd-tree

# Set up development environment
make setup

# Run tests
make test

# Build and test
make portable
./dist/dir_tree_portable --help
```

---
