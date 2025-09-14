# Directory Tree Generator - Build System
# Supports multiple platforms and packaging formats

.PHONY: all clean portable installer windows linux macos help

# Default target
all: portable installer

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf dist/
	@rm -rf build/
	@rm -f *.spec
	@rm -f installer.nsi

# Build portable executable
portable:
	@echo "Building portable executable..."
	@python build.py --portable-only

# Build installer for current platform
installer:
	@echo "Building installer..."
	@python build.py --installer-only

# Windows-specific builds
windows: clean
	@echo "Building for Windows..."
	@python build.py --portable-only
	@if command -v makensis >/dev/null 2>&1; then \
		echo "Building Windows installer..."; \
		makensis installer.nsi; \
	else \
		echo "NSIS not found. Install NSIS to build Windows installer."; \
	fi

# Linux-specific builds
linux: clean
	@echo "Building for Linux..."
	@python build.py --portable-only
	@echo "Building Linux packages..."
	@python build.py --installer-only

# macOS-specific builds
macos: clean
	@echo "Building for macOS..."
	@python build.py --portable-only
	@echo "Building macOS app bundle..."
	@python build.py --installer-only

# Development setup
setup:
	@echo "Setting up development environment..."
	@pip install -r requirements.txt
	@echo "Development environment ready!"

# Test builds
test: clean
	@echo "Running test build..."
	@python -c "import dir_tree; print('Basic import test passed')"
	@python -c "import updater; print('Updater import test passed')"
	@echo "Basic tests passed!"

# Create release package
release: clean all
	@echo "Creating release package..."
	@mkdir -p release/
	@cp -r dist/* release/ 2>/dev/null || true
	@cp README.md release/
	@cp LICENSE.txt release/
	@echo "Release package created in release/ directory"

# Install locally (for testing)
install-local: portable
	@echo "Installing locally..."
	@mkdir -p ~/.local/bin/
	@cp dist/dir_tree_portable ~/.local/bin/dir_tree
	@chmod +x ~/.local/bin/dir_tree
	@echo "Installed to ~/.local/bin/dir_tree"

# Uninstall local installation
uninstall-local:
	@echo "Uninstalling local installation..."
	@rm -f ~/.local/bin/dir_tree
	@echo "Local installation removed"

# Show help
help:
	@echo "Directory Tree Generator - Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  all          - Build everything (portable + installer)"
	@echo "  clean        - Remove build artifacts"
	@echo "  portable     - Build portable executable only"
	@echo "  installer    - Build installer only"
	@echo "  windows      - Build Windows-specific packages"
	@echo "  linux        - Build Linux-specific packages"
	@echo "  macos        - Build macOS-specific packages"
	@echo "  setup        - Set up development environment"
	@echo "  test         - Run basic tests"
	@echo "  release      - Create release package"
	@echo "  install-local- Install locally for testing"
	@echo "  uninstall-local- Remove local installation"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make setup          # Set up development environment"
	@echo "  make portable       # Build portable executable"
	@echo "  make windows        # Build Windows packages"
	@echo "  make release        # Create release package"