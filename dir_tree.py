import os
import sys

def generate_tree(start_path, output_file):
    tree = []
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = '    |' * (level)
        tree.append(f"{indent}__{os.path.basename(root)}/")
        sub_indent = '    |' * (level + 1)
        for file in files:
            tree.append(f"{sub_indent}__{file}")
    with open(output_file, 'w') as f:
        f.write('\n'.join(tree))

def add_context_menu():
    import winreg
    key_path = r"Directory\\shell\\GenerateTree"
    command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1"'
    
    # Create context menu entry
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Generate Directory Tree")
        
    # Create command entry
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path + "\\command") as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        output = os.path.join(path, f"{os.path.basename(path)}_tree.txt")
        generate_tree(path, output)
        print(f"Tree structure saved to {output}")
    else:
        print("Installing context menu entry...")
        add_context_menu()
        print("Context menu entry added. Right-click any folder to generate tree.")