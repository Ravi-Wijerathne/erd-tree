"""
Auto-updater module for Directory Tree Generator
Checks for updates from GitHub releases and handles downloads
"""

import os
import sys
import json
import requests
import platform
import subprocess
import tempfile
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from tkinter import messagebox, simpledialog
import tkinter as tk

try:
    from tkinter import ttk
except ImportError:
    # ttk might not be available in some Python installations
    ttk = None

# GitHub repository information
GITHUB_REPO = "Ravi-Wijerathne/erd-tree"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
CURRENT_VERSION = "1.0.0"  # Update this when releasing new versions

class AutoUpdater:
    def __init__(self, parent_window=None):
        self.parent = parent_window
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()

    def check_for_updates(self, silent=False):
        """Check for updates from GitHub releases"""
        try:
            response = requests.get(GITHUB_API_URL, timeout=10)
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')

            if self._is_newer_version(latest_version, CURRENT_VERSION):
                if not silent:
                    self._show_update_dialog(release_data)
                return True, release_data
            else:
                if not silent:
                    messagebox.showinfo("No Updates", "You are running the latest version!")
                return False, None

        except requests.RequestException as e:
            if not silent:
                messagebox.showerror("Update Check Failed",
                                   f"Failed to check for updates:\n{str(e)}")
            return False, None
        except Exception as e:
            if not silent:
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            return False, None

    def _is_newer_version(self, latest, current):
        """Compare version strings"""
        def version_tuple(v):
            return tuple(map(int, v.split('.')))

        try:
            return version_tuple(latest) > version_tuple(current)
        except ValueError:
            return False

    def _show_update_dialog(self, release_data):
        """Show update available dialog"""
        version = release_data['tag_name']
        changelog = release_data.get('body', 'No changelog available')

        # Create update dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Available")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        # Center the dialog
        dialog.transient(self.parent)
        dialog.grab_set()

        # Title
        title_label = tk.Label(dialog, text=f"Update Available: {version}",
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Changelog
        changelog_frame = tk.Frame(dialog)
        changelog_frame.pack(fill="both", expand=True, padx=20, pady=10)

        changelog_label = tk.Label(changelog_frame, text="What's new:",
                                  font=("Arial", 10, "bold"), anchor="w")
        changelog_label.pack(anchor="w")

        changelog_text = tk.Text(changelog_frame, height=10, wrap="word")
        changelog_text.insert("1.0", changelog)
        changelog_text.config(state="disabled")

        scrollbar = tk.Scrollbar(changelog_frame)
        scrollbar.pack(side="right", fill="y")
        changelog_text.pack(side="left", fill="both", expand=True)

        changelog_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=changelog_text.yview)

        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill="x", padx=20, pady=10)

        def download_update():
            dialog.destroy()
            self.download_and_install_update(release_data)

        def skip_update():
            dialog.destroy()

        download_btn = tk.Button(button_frame, text="Download & Install",
                                command=download_update, width=15)
        download_btn.pack(side="left", padx=5)

        skip_btn = tk.Button(button_frame, text="Skip", command=skip_update, width=15)
        skip_btn.pack(side="right", padx=5)

        # Wait for dialog to close
        self.parent.wait_window(dialog)

    def download_and_install_update(self, release_data):
        """Download and install the update"""
        try:
            # Find the appropriate asset for this platform
            asset = self._find_compatible_asset(release_data['assets'])
            if not asset:
                messagebox.showerror("Update Failed",
                                   "No compatible update found for your platform.")
                return

            download_url = asset['browser_download_url']
            filename = asset['name']

            # Create progress dialog
            progress_dialog = tk.Toplevel(self.parent)
            progress_dialog.title("Downloading Update")
            progress_dialog.geometry("300x100")
            progress_dialog.resizable(False, False)

            progress_label = tk.Label(progress_dialog, text="Downloading update...")
            progress_label.pack(pady=10)

            progress_var = tk.DoubleVar()
            if ttk:
                progress_bar = ttk.Progressbar(progress_dialog, variable=progress_var,
                                             maximum=100)
            else:
                # Fallback to simple label if ttk not available
                progress_bar = tk.Label(progress_dialog, text="Downloading...")
                def update_progress_display(percent):
                    progress_bar.config(text=f"Downloading... {percent:.1f}%")
                progress_var.trace_add("write", lambda *args: update_progress_display(progress_var.get()))
            progress_bar.pack(fill="x", padx=20, pady=5)

            def update_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(100, (downloaded / total_size) * 100)
                progress_var.set(percent)
                progress_dialog.update()

            # Download the update
            with tempfile.TemporaryDirectory() as temp_dir:
                update_path = os.path.join(temp_dir, filename)

                # Download with progress
                urlretrieve(download_url, update_path, update_progress)

                progress_dialog.destroy()

                # Install the update
                self._install_update(update_path, filename)

        except Exception as e:
            if 'progress_dialog' in locals():
                progress_dialog.destroy()
            messagebox.showerror("Update Failed", f"Failed to download update:\n{str(e)}")

    def _find_compatible_asset(self, assets):
        """Find the appropriate asset for this platform"""
        system_map = {
            'windows': ['windows', 'win'],
            'darwin': ['macos', 'darwin', 'osx'],
            'linux': ['linux']
        }

        arch_map = {
            'x86_64': ['x64', 'amd64', 'x86_64'],
            'arm64': ['arm64', 'aarch64'],
            'i386': ['x86', 'i386']
        }

        system_keywords = system_map.get(self.system, [self.system])
        arch_keywords = arch_map.get(self.arch, [self.arch])

        for asset in assets:
            name = asset['name'].lower()

            # Check if asset matches our platform
            system_match = any(keyword in name for keyword in system_keywords)
            arch_match = any(keyword in name for keyword in arch_keywords)

            if system_match and arch_match:
                return asset

        # Fallback: return first asset if no specific match found
        return assets[0] if assets else None

    def _install_update(self, update_path, filename):
        """Install the downloaded update"""
        try:
            if filename.endswith('.exe') and self.system == 'windows':
                # Windows installer
                subprocess.run([update_path], check=True)
            elif filename.endswith('.dmg') and self.system == 'darwin':
                # macOS DMG
                subprocess.run(['hdiutil', 'attach', update_path], check=True)
                # Note: Would need more complex logic to install from DMG
            elif filename.endswith(('.tar.gz', '.zip')):
                # Extract and replace current executable
                extract_dir = tempfile.mkdtemp()

                if filename.endswith('.tar.gz'):
                    subprocess.run(['tar', '-xzf', update_path, '-C', extract_dir], check=True)
                else:
                    shutil.unpack_archive(update_path, extract_dir)

                # Find the executable in the extracted files
                exe_name = self._find_executable(extract_dir)
                if exe_name:
                    current_exe = sys.executable
                    backup_exe = current_exe + '.backup'

                    # Create backup
                    shutil.copy2(current_exe, backup_exe)

                    # Replace executable
                    shutil.copy2(exe_name, current_exe)

                    messagebox.showinfo("Update Complete",
                                      "Update installed successfully!\n"
                                      "The application will restart.")

                    # Restart application
                    os.execv(current_exe, sys.argv)
                else:
                    raise Exception("Could not find executable in update package")

            else:
                raise Exception(f"Unsupported update format: {filename}")

        except Exception as e:
            messagebox.showerror("Installation Failed", f"Failed to install update:\n{str(e)}")

    def _find_executable(self, directory):
        """Find the main executable in the extracted directory"""
        exe_names = ['dir_tree', 'dir_tree.exe', 'Directory Tree Generator',
                    'Directory Tree Generator.exe']

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file in exe_names or (file.startswith('dir_tree') and os.access(os.path.join(root, file), os.X_OK)):
                    return os.path.join(root, file)

        return None

def check_for_updates_gui(parent=None):
    """Convenience function to check for updates with GUI"""
    updater = AutoUpdater(parent)
    return updater.check_for_updates()

def check_for_updates_silent():
    """Convenience function to check for updates silently"""
    updater = AutoUpdater()
    has_update, release_data = updater.check_for_updates(silent=True)
    return has_update

if __name__ == "__main__":
    # Test the updater
    updater = AutoUpdater()
    has_update, release_data = updater.check_for_updates()
    if has_update:
        print(f"Update available: {release_data['tag_name']}")
    else:
        print("No updates available")