# Directory Tree Generator

A cross-platform tool for generating visual directory tree structures.

![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Features

- Cross-platform: Windows, Linux, and macOS
- Multiple output formats: Text, Markdown, and HTML
- GUI and CLI interfaces
- Auto-updater for latest releases
- Lightweight and fast

## Quick Start

### Automated Startup (Recommended)

```bash
./scripts/start.sh
```

The startup script automatically checks and installs all prerequisites, then launches the application.

### Manual Usage

#### GUI Mode
```bash
python dir_tree.py
```

#### CLI Mode
```bash
python dir_tree.py /path/to/directory
python dir_tree.py /path/to/directory -f markdown -o output.md
```

## Installation

### Prerequisites
- Python 3.7+
- pip
- tkinter

### Setup

```bash
# Clone repository
git clone https://github.com/Ravi-Wijerathne/erd-tree.git
cd erd-tree

# Use automated startup script
./scripts/start.sh

# Or install manually
pip install -r requirements.txt
python dir_tree.py
```

## Usage

### Command Line

```bash
# Basic usage
python dir_tree.py /path/to/directory

# With format option
python dir_tree.py /path/to/directory -f markdown

# Custom output file
python dir_tree.py /path/to/directory -o tree.txt

# Force CLI mode (no GUI)
python dir_tree.py /path/to/directory --no-gui
```

### Options

| Option | Description |
|--------|-------------|
| `directory` | Path to directory |
| `-f, --format` | Output format: text, markdown, html |
| `-o, --output` | Custom output file path |
| `--no-gui` | Force CLI mode |

### GUI

1. Launch `python dir_tree.py` or `./scripts/start.sh`
2. Click **Browse** to select folder
3. Choose output format
4. Click **Generate Tree**

## Output Examples

### Text Format
```
    |__project/
    |    |__src/
    |    |    |__main.py
    |    |    |__utils.py
    |    |__README.md
```

### Markdown Format
```
    |- project/
    |    |- src/
    |    |    |- main.py
    |    |    |- utils.py
    |    |- README.md
```

## Building Portable Version

```bash
# Install pyinstaller
pip install pyinstaller

# Build executable
python scripts/build.py --portable-only
```

The executable will be in the `dist/` folder.

## Testing

```bash
python test_dir_tree.py
```

## License

MIT License - see [LICENSE.txt](LICENSE.txt)

## Contributing

Contributions welcome! Please open issues or submit pull requests on [GitHub](https://github.com/Ravi-Wijerathne/erd-tree).

---

*Simple, fast, cross-platform directory tree generation*
