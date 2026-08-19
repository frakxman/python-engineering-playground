# 📂 File Organizer

> A production-minded CLI tool to automatically sort and organize files into subfolders based on configurable rules.

Part of the **Python Engineering Playground** – built with Clean Architecture, SOLID principles, and cross-platform compatibility.

---

## 🎯 Project Goals

- Automate the tedious task of cleaning up messy directories (e.g., `~/Downloads`).
- Separate **configuration**, **scanning**, and **execution** logic into distinct, testable modules.
- Implement a safe **Dry-Run** mode to preview changes before applying them.
- Practice professional error handling (permissions, duplicates, missing paths).
- Use `pathlib` for cross-platform file operations (Windows, Linux, macOS).

---

## 🏗 Architecture

```
file_organizer/
│
├── main.py           # Orchestrates the whole flow
├── cli.py            # Handles argparse and user input
├── config_loader.py  # Loads sorting rules from JSON
├── scanner.py        # Walks directories and classifies files
├── organizer.py      # Contains the moving/copying logic
├── logger.py         # Configures logging (console + file)
└── rules.json        # Default rule set (extension -> folder)
```

---

## 🚀 Installation & Usage

1. Navigate to the project folder:
   ```bash
   cd src/automation/file_organizer/
   ```

2. (Optional) Use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Run the organizer:
   ```bash
   # Dry-run (safe preview)
   python main.py --path ~/Downloads --dry-run

   # Real execution with custom rules
   python main.py --path ~/Downloads --config my_rules.json --recursive

   # Show help
   python main.py --help
   ```

---

## ⚙️ Configuration (rules.json)

Define your own rules as a simple JSON object:

```json
{
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "documents": [".pdf", ".docx", ".txt", ".md"],
    "spreadsheets": [".xlsx", ".csv", ".tsv"],
    "archives": [".zip", ".tar.gz", ".rar"],
    "code": [".py", ".js", ".html", ".css", ".json"],
    "others": []
}
```

- If a file extension doesn't match any rule, it goes to `others/`.
- You can customize folders and extensions freely.

---

## 🛠 Engineering Practices Demonstrated

| Concept | Implementation |
| :--- | :--- |
| **Single Responsibility** | One class/module per task (scanning ≠ organizing). |
| **Dependency Injection** | The organizer receives a config object instead of reading it itself. |
| **Type Hints** | Every function annotated (`-> list[Path]`, `-> None`). |
| **Safe Execution** | `--dry-run` flag simulates all operations without writing to disk. |
| **Exception Handling** | Graceful handling of `PermissionError`, `OSError`. |
| **Logging** | Both console output and persistent `.log` file for audit trails. |
| **Pathlib** | 100% `pathlib.Path` usage (no `os.path.join`). |

---

## 📝 Logging

All actions are logged both to the console and to a file named `file_organizer.log` in the current working directory. The log includes timestamps, action types (e.g., `MOVED`, `SKIPPED`, `ERROR`), and full source/destination paths for complete traceability.

---

## 🧪 Example Workflow

```bash
# 1. Preview what would happen
python main.py --path ~/Downloads --dry-run --recursive

# 2. Check the log file to see the plan
cat file_organizer.log

# 3. Execute for real
python main.py --path ~/Downloads --recursive

# 4. Verify the new structure
ls ~/Downloads
```

---

> *"A place for everything, and everything in its place."* 🗂️
```

---
