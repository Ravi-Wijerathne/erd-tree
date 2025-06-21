import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

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

def add_context_menu():
    import winreg
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

def remove_context_menu():
    import winreg
    try:
        key_path = r"Directory\\shell\\GenerateTree"
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path + "\\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        messagebox.showinfo("Success", "Context menu entry removed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove context menu entry: {e}")

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

    root = tk.Tk()
    root.title("Directory Tree Generator")
    root.geometry("400x250")

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
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.basename(path)
            output_file = os.path.join(path, f"{base_name}_tree_{timestamp}.txt")
            if generate_tree(path, output_file):
                print(f"Tree structure saved to {output_file}")
            else:
                print("Failed to generate tree structure.")
        else:
            print(f"Invalid directory: {path}")
    else:
        gui()