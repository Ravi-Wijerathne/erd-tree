import os
import sys
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# Platform detection
CURRENT_OS = platform.system().lower()

# Try to import updater
try:
    from scripts.updater import check_for_updates_gui
    UPDATER_AVAILABLE = True
except ImportError:
    try:
        # Backward compatibility for older layouts
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
    
    args = parser.parse_args()
    
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