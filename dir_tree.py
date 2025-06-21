import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

def generate_tree(start_path, output_file, format="text", indentation=4):
    try:
        tree = []
        total_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(start_path)])
        progress_step = 100 / total_items if total_items > 0 else 100
        progress_value = 0

        for root, dirs, files in os.walk(start_path):
            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * (level * indentation)
            if format == "markdown":
                tree.append(f"{indent}- {os.path.basename(root)}/")
            elif format == "html":
                tree.append(f"<div style='margin-left: {level * indentation}px;'>{os.path.basename(root)}/</div>")
            else:
                tree.append(f"{indent}__{os.path.basename(root)}/")

            sub_indent = ' ' * ((level + 1) * indentation)
            for file in files:
                if format == "markdown":
                    tree.append(f"{sub_indent}- {file}")
                elif format == "html":
                    tree.append(f"<div style='margin-left: {(level + 1) * indentation}px;'>- {file}</div>")
                else:
                    tree.append(f"{sub_indent}__{file}")

                # Update progress bar
                progress_value += progress_step
                progress_var.set(min(progress_value, 100))
                root.update_idletasks()

        with open(output_file, 'w', encoding='utf-8') as f:
            if format == "html":
                f.write("<html><body>\n")
                f.write("\n".join(tree))
                f.write("\n</body></html>")
            else:
                f.write("\n".join(tree))

        return True, "\n".join(tree)
    except Exception as e:
        print(f"Error: {e}")
        return False, str(e)

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

def toggle_dark_mode():
    if dark_mode_var.get():
        root.config(bg="#2d2d2d")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#2d2d2d", fg="white")
            elif isinstance(widget, tk.Entry):
                widget.config(bg="#4d4d4d", fg="white", insertbackground="white")
            elif isinstance(widget, tk.Button):
                widget.config(bg="#4d4d4d", fg="white", activebackground="#5d5d5d", activeforeground="white")
            elif isinstance(widget, ttk.Progressbar):
                widget.config(style="Dark.Horizontal.TProgressbar")
    else:
        root.config(bg="white")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="white", fg="black")
            elif isinstance(widget, tk.Entry):
                widget.config(bg="white", fg="black", insertbackground="black")
            elif isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="black", activebackground="#d9d9d9", activeforeground="black")
            elif isinstance(widget, ttk.Progressbar):
                widget.config(style="Light.Horizontal.TProgressbar")

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
        success, tree_preview = generate_tree(path, output_file, format, indentation=indentation_scale.get())
        if success:
            preview_text.delete(1.0, tk.END)
            preview_text.insert(tk.END, tree_preview)
            messagebox.showinfo("Success", f"Tree structure saved to:\n{output_file}")
        else:
            messagebox.showerror("Error", f"Failed to generate tree structure:\n{tree_preview}")

    global root
    root = tk.Tk()
    root.title("ERD-TREE")
    root.geometry("600x500")

    # Dark mode variable
    dark_mode_var = tk.BooleanVar(value=False)

    # Folder selection
    folder_path = tk.StringVar()
    tk.Label(root, text="Select Folder:").pack(pady=5)
    tk.Entry(root, textvariable=folder_path, width=50).pack(pady=5)
    tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)

    # Output format
    tk.Label(root, text="Output Format:").pack(pady=5)
    format_var = tk.StringVar(value="text")
    tk.Radiobutton(root, text="Plain Text", variable=format_var, value="text").pack(anchor="w")
    tk.Radiobutton(root, text="Markdown", variable=format_var, value="markdown").pack(anchor="w")
    tk.Radiobutton(root, text="HTML", variable=format_var, value="html").pack(anchor="w")

    # Indentation customization
    tk.Label(root, text="Indentation Level:").pack(pady=5)
    indentation_scale = tk.Scale(root, from_=2, to=10, orient=tk.HORIZONTAL)
    indentation_scale.set(4)
    indentation_scale.pack(pady=5)

    # Progress bar
    global progress_var
    progress_var = tk.DoubleVar()
    ttk.Style().configure("Dark.Horizontal.TProgressbar", background="#4caf50")
    ttk.Style().configure("Light.Horizontal.TProgressbar", background="#4caf50")
    ttk.Progressbar(root, variable=progress_var, length=400, mode="determinate", style="Light.Horizontal.TProgressbar").pack(pady=10)

    # Preview pane
    tk.Label(root, text="Preview:").pack(pady=5)
    preview_text = tk.Text(root, height=10, width=70, wrap=tk.WORD)
    preview_text.pack(pady=5)

    # Generate button
    tk.Button(root, text="Generate Tree", command=generate).pack(pady=10)

    # Context menu buttons
    tk.Button(root, text="Add Context Menu Entry", command=add_context_menu).pack(side="left", padx=10)
    tk.Button(root, text="Remove Context Menu Entry", command=remove_context_menu).pack(side="right", padx=10)

    # Dark mode toggle
    tk.Checkbutton(root, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.basename(path)
            output_file = os.path.join(path, f"{base_name}_tree_{timestamp}.txt")
            if generate_tree(path, output_file)[0]:
                print(f"Tree structure saved to {output_file}")
            else:
                print("Failed to generate tree structure.")
        else:
            print(f"Invalid directory: {path}")
    else:
        gui()