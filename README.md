
---

# Directory Tree Generator

The **Directory Tree Generator** is a lightweight Python-based tool designed to recursively generate a visual representation of a folder's structure (files and subfolders). The generated output can be saved in multiple formats (plain text, Markdown, or HTML) and optionally integrated into the Windows context menu for easy access.

---

## Features

- **Recursive Directory Traversal**: Generates a hierarchical tree structure of all files and subfolders within a selected folder.
- **Multiple Output Formats**:
  - Plain Text: Simple indented structure.
  - Markdown: Uses bullet points (`-`) for hierarchy.
  - HTML: Generates a styled HTML document with proper indentation.
- **Timestamped Output Files**: Each generated file includes a timestamp in its name for easy identification.
- **Context Menu Integration**: Adds a "Generate Directory Tree" option to the Windows context menu for quick access.
- **User-Friendly GUI**: A graphical interface allows users to select folders, choose output formats, and manage context menu entries.
- **Error Handling**: Handles invalid directories, permission errors, and other exceptions gracefully.

---

## Installation

### Prerequisites
- Python 3.7 or higher installed on your system.
- Administrator privileges (required for adding/removing context menu entries).

### Steps to Install

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/directory-tree-generator.git
   cd directory-tree-generator
   ```

2. **Install Dependencies**:
   Ensure you have `pyinstaller` installed to create an executable:
   ```bash
   pip install pyinstaller
   ```

3. **Create Executable**:
   Use `pyinstaller` to package the script into a standalone executable:
   ```bash
   pyinstaller --onefile dir_tree.py
   ```
   The executable will be located in the `dist/` folder.

4. **Run the Tool**:
   - Double-click the generated `dir_tree.exe` file to launch the GUI.
   - Alternatively, run the script directly using Python:
     ```bash
     python dir_tree.py
     ```

---

## Usage

### Using the GUI
1. Launch the tool by running the executable or Python script.
2. Click **Browse** to select the folder whose structure you want to generate.
3. Choose the desired output format (Plain Text, Markdown, or HTML).
4. Click **Generate Tree** to create the directory tree file.
5. The generated file will be saved in the selected folder with a timestamped filename (e.g., `Semester_tree_20231005_143022.txt`).

### Using the Context Menu
1. Add the context menu entry:
   - Open the GUI and click **Add Context Menu Entry**.
   - Alternatively, right-click any folder and select **Generate Directory Tree** if already added.
2. Right-click any folder in Windows Explorer and select **Generate Directory Tree**.
3. The tool will automatically generate the directory tree file in the selected folder.

### Removing the Context Menu Entry
To remove the context menu entry:
- Open the GUI and click **Remove Context Menu Entry**.

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

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions, feedback, or bug reports, feel free to reach out:

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

## Acknowledgments

- Inspired by tools like `tree` on Unix-based systems.
- Built using Python and `tkinter` for the GUI.
- Special thanks to the open-source community for their contributions and support.

---
