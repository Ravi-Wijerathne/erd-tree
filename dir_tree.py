import os
import sys
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Platform detection
CURRENT_OS = platform.system().lower()

# Platform-specific imports
if CURRENT_OS == "windows":
    try:
        import winreg
    except ImportError:
        winreg = None
elif CURRENT_OS == "linux":
    pass  # No special imports needed for Linux
elif CURRENT_OS == "darwin":  # macOS
    pass  # No special imports needed for macOS

# Try to import updater
try:
    from updater import check_for_updates_gui
    UPDATER_AVAILABLE = True
except ImportError:
    UPDATER_AVAILABLE = False

def generate_tree(start_path, output_file, format="text"):
    try:
        tree = []
        for root, dirs, files in os.walk(start_path):
            level = root.replace(start_path, '').count(os.sep)
            indent = '    |' * (level)
            if format == "markdown":
                tree.append(f"{indent}- {os.path.basename(root)}/")
            elif format == "html":
                tree.append(f"<div style='margin-left: {level * 20}px;'>{os.path.basename(root)}/</div>")
            else:
                tree.append(f"{indent}__{os.path.basename(root)}/")
            
            sub_indent = '    |' * (level + 1)
            for file in files:
                if format == "markdown":
                    tree.append(f"{sub_indent}- {file}")
                elif format == "html":
                    tree.append(f"<div style='margin-left: {(level + 1) * 20}px;'>- {file}</div>")
                else:
                    tree.append(f"{sub_indent}__{file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            if format == "html":
                f.write("<html><body>\n")
                f.write("\n".join(tree))
                f.write("\n</body></html>")
            else:
                f.write("\n".join(tree))
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def add_context_menu_windows():
    if winreg is None:
        messagebox.showerror("Error", "winreg module not available")
        return
    
    key_path = r"Directory\\shell\\GenerateTree"
    command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1"'
    
    try:
        # Create context menu entry
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Generate Directory Tree")
        
        # Create command entry
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path + "\\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
        
        messagebox.showinfo("Success", "Context menu entry added. Right-click any folder to generate tree.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add context menu entry: {e}")

def remove_context_menu_windows():
    if winreg is None:
        messagebox.showerror("Error", "winreg module not available")
        return
    
    try:
        key_path = r"Directory\\shell\\GenerateTree"
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path + "\\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        messagebox.showinfo("Success", "Context menu entry removed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove context menu entry: {e}")

def add_context_menu_linux():
    # Create .desktop file for Nautilus/GNOME context menu integration
    desktop_file_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Generate Directory Tree
Comment=Generate directory tree structure
Exec={sys.executable} {os.path.abspath(__file__)} %F
Icon=folder
Terminal=false
MimeType=inode/directory;
"""
    
    # Create directory if it doesn't exist
    desktop_dir = os.path.expanduser("~/.local/share/applications")
    os.makedirs(desktop_dir, exist_ok=True)
    
    desktop_file_path = os.path.join(desktop_dir, "generate-directory-tree.desktop")
    
    try:
        with open(desktop_file_path, 'w', encoding='utf-8') as f:
            f.write(desktop_file_content)
        
        # Make the file executable
        os.chmod(desktop_file_path, 0o755)
        
        messagebox.showinfo("Success", f"Context menu integration added.\n.desktop file created at: {desktop_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create .desktop file: {e}")

def remove_context_menu_linux():
    desktop_file_path = os.path.expanduser("~/.local/share/applications/generate-directory-tree.desktop")
    
    try:
        if os.path.exists(desktop_file_path):
            os.remove(desktop_file_path)
            messagebox.showinfo("Success", "Context menu integration removed.")
        else:
            messagebox.showwarning("Warning", ".desktop file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove .desktop file: {e}")

def add_context_menu_macos():
    # Create plist file for Finder context menu integration
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>com.directorytree.generator</string>
    <key>CFBundleName</key>
    <string>Generate Directory Tree</string>
    <key>NSPrincipalClass</key>
    <string>DirectoryTreeGenerator</string>
    <key>NSServices</key>
    <array>
        <dict>
            <key>NSMenuItem</key>
            <dict>
                <key>default</key>
                <string>Generate Directory Tree</string>
            </dict>
            <key>NSMessage</key>
            <string>generateTree</string>
            <key>NSPortName</key>
            <string>DirectoryTreeGenerator</string>
            <key>NSRequiredContext</key>
            <dict>
                <key>NSTextContent</key>
                <string>FilePath</string>
            </dict>
            <key>NSSendTypes</key>
            <array>
                <string>NSFilenamesPboardType</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
"""
    
    plist_dir = os.path.expanduser("~/Library/Services")
    os.makedirs(plist_dir, exist_ok=True)
    
    plist_file_path = os.path.join(plist_dir, "Generate Directory Tree.workflow/Contents/Info.plist")
    os.makedirs(os.path.dirname(plist_file_path), exist_ok=True)
    
    try:
        with open(plist_file_path, 'w', encoding='utf-8') as f:
            f.write(plist_content)
        
        messagebox.showinfo("Success", f"Context menu integration added.\nService created at: {plist_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create service: {e}")

def remove_context_menu_macos():
    plist_file_path = os.path.expanduser("~/Library/Services/Generate Directory Tree.workflow/Contents/Info.plist")
    
    try:
        if os.path.exists(plist_file_path):
            os.remove(plist_file_path)
            # Remove the workflow directory if empty
            workflow_dir = os.path.dirname(os.path.dirname(plist_file_path))
            if os.path.exists(workflow_dir) and not os.listdir(workflow_dir):
                os.rmdir(workflow_dir)
            messagebox.showinfo("Success", "Context menu integration removed.")
        else:
            messagebox.showwarning("Warning", "Service file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove service: {e}")

def add_context_menu():
    if CURRENT_OS == "windows":
        return add_context_menu_windows()
    elif CURRENT_OS == "linux":
        return add_context_menu_linux()
    elif CURRENT_OS == "darwin":
        return add_context_menu_macos()
    else:
        messagebox.showerror("Error", f"Context menu integration not supported on {CURRENT_OS}")

def remove_context_menu():
    if CURRENT_OS == "windows":
        return remove_context_menu_windows()
    elif CURRENT_OS == "linux":
        return remove_context_menu_linux()
    elif CURRENT_OS == "darwin":
        return remove_context_menu_macos()
    else:
        messagebox.showerror("Error", f"Context menu integration not supported on {CURRENT_OS}")

def gui():
    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_path.set(folder_selected)

    def generate():
        path = folder_path.get()
        if not path:
            messagebox.showwarning("Warning", "Please select a folder.")
            return
        
        format = format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(path)
        output_file = os.path.join(path, f"{base_name}_tree_{timestamp}.{format}")
        
        if generate_tree(path, output_file, format):
            messagebox.showinfo("Success", f"Tree structure saved to:\n{output_file}")
        else:
            messagebox.showerror("Error", "Failed to generate tree structure.")

    def check_for_updates():
        if UPDATER_AVAILABLE:
            check_for_updates_gui(root)
        else:
            messagebox.showinfo("Updater Not Available",
                              "Auto-updater is not available.\n"
                              "Please check the project repository for updates.")

    def show_about():
        about_text = f"""Directory Tree Generator v1.0.0

A cross-platform tool for generating directory tree structures.

Platform: {CURRENT_OS.title()}
Python: {sys.version.split()[0]}

Features:
• Generate directory trees in multiple formats
• Cross-platform context menu integration
• Command-line interface
• Portable executable available

For more information, visit the project repository."""
        
        messagebox.showinfo("About", about_text)

    root = tk.Tk()
    root.title(f"Directory Tree Generator - {CURRENT_OS.title()}")
    root.geometry("400x250")

    # Create menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)

    # Tools menu
    tools_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tools", menu=tools_menu)
    tools_menu.add_command(label="Check for Updates", command=check_for_updates)

    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)

    folder_path = tk.StringVar()

    folder_path = tk.StringVar()

    tk.Label(root, text="Select Folder:").pack(pady=5)
    tk.Entry(root, textvariable=folder_path, width=50).pack(pady=5)
    tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)

    tk.Label(root, text="Output Format:").pack(pady=5)
    format_var = tk.StringVar(value="text")
    tk.Radiobutton(root, text="Plain Text", variable=format_var, value="text").pack(anchor="w")
    tk.Radiobutton(root, text="Markdown", variable=format_var, value="markdown").pack(anchor="w")
    tk.Radiobutton(root, text="HTML", variable=format_var, value="html").pack(anchor="w")

    tk.Button(root, text="Generate Tree", command=generate).pack(pady=20)
    tk.Button(root, text="Add Context Menu Entry", command=add_context_menu).pack(side="left", padx=10)
    tk.Button(root, text="Remove Context Menu Entry", command=remove_context_menu).pack(side="right", padx=10)

    root.mainloop()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate directory tree structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dir_tree.py /path/to/directory                    # Generate text tree
  python dir_tree.py /path/to/directory -f markdown       # Generate markdown tree
  python dir_tree.py /path/to/directory -o output.txt     # Specify output file
  python dir_tree.py /path/to/directory --no-gui          # Force CLI mode
  python dir_tree.py --setup-context-menu                 # Setup context menu
  python dir_tree.py --remove-context-menu                # Remove context menu
        """
    )
    
    parser.add_argument("directory", nargs="?", help="Directory path to generate tree for")
    parser.add_argument("-f", "--format", 
                       choices=["text", "markdown", "html"], 
                       default="text",
                       help="Output format (default: text)")
    parser.add_argument("-o", "--output", 
                       help="Output file path (default: auto-generated)")
    parser.add_argument("--no-gui", 
                       action="store_true",
                       help="Force CLI mode even if GUI is available")
    parser.add_argument("--setup-context-menu",
                       action="store_true", 
                       help="Setup context menu integration for current platform")
    parser.add_argument("--remove-context-menu",
                       action="store_true",
                       help="Remove context menu integration")
    
    args = parser.parse_args()
    
    # Handle context menu setup/removal
    if args.setup_context_menu:
        if CURRENT_OS == "windows":
            add_context_menu_windows()
        elif CURRENT_OS == "linux":
            add_context_menu_linux()
        elif CURRENT_OS == "darwin":
            add_context_menu_macos()
        else:
            print(f"Context menu integration not supported on {CURRENT_OS}")
        sys.exit(0)
    
    if args.remove_context_menu:
        if CURRENT_OS == "windows":
            remove_context_menu_windows()
        elif CURRENT_OS == "linux":
            remove_context_menu_linux()
        elif CURRENT_OS == "darwin":
            remove_context_menu_macos()
        else:
            print(f"Context menu integration not supported on {CURRENT_OS}")
        sys.exit(0)
    
    # Handle directory tree generation
    if args.directory:
        if not os.path.isdir(args.directory):
            print(f"Error: '{args.directory}' is not a valid directory")
            sys.exit(1)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.basename(args.directory)
            extension = "txt" if args.format == "text" else args.format
            output_file = os.path.join(args.directory, f"{base_name}_tree_{timestamp}.{extension}")
        
        if generate_tree(args.directory, output_file, args.format):
            print(f"Directory tree generated successfully: {output_file}")
        else:
            print("Failed to generate directory tree")
            sys.exit(1)
    else:
        # No directory provided, check if we should show GUI
        if not args.no_gui and CURRENT_OS in ["windows", "linux", "darwin"]:
            try:
                gui()
            except Exception as e:
                print(f"GUI not available: {e}")
                print("Use --help for CLI options")
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)