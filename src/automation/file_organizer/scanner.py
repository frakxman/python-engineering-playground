from pathlib import Path
from typing import Dict, List, Optional

class FileScanner:
    """
    Scans a directory and classifies files into categories based on extension rules.
    """

    def __init__(self, rules: Dict[str, List[str]], recursive: bool = False):
        """
        Initialize the scanner with a set of rules.

        Args:
            rules: Dictionary mapping category names to lists of extensions (lowercase).
            recursive: If True, scan subdirectories recursively.
        """
        self.rules = rules
        self.recursive = recursive
        # Build a reverse mapping: extension -> category for quick lookup
        self._extension_to_category = {}
        for category, extensions in rules.items():
            for ext in extensions:
                self._extension_to_category[ext] = category

    def scan(self, directory: Path) -> Dict[str, List[Path]]:
        """
        Scan the given directory and classify files.

        Args:
            directory: Path object of the directory to scan.

        Returns:
            Dictionary where keys are category names and values are lists of Path objects.
        """
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        if not directory.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")

        classified = {category: [] for category in self.rules.keys()}
        # Ensure we have a category for uncategorized files
        if "others" not in classified:
            classified["others"] = []

        # Choose the appropriate iteration method
        if self.recursive:
            iterator = directory.rglob('*')  # Recursive: all files and folders
        else:
            iterator = directory.iterdir()   # Non-recursive: only direct children

        for item in iterator:
            if item.is_file():
                category = self._get_category(item)
                classified[category].append(item)

        return classified

    def _get_category(self, file_path: Path) -> str:
        """
        Determine the category for a given file based on its extension.

        Args:
            file_path: Path object of the file.

        Returns:
            Category name as string.
        """
        suffix = file_path.suffix.lower()
        # If the extension is in the mapping, return its category
        if suffix in self._extension_to_category:
            return self._extension_to_category[suffix]
        # Otherwise, check if there's a category for extensions with dots (e.g., .tar.gz)
        # For multi-dot extensions, try the last two suffixes combined
        if '.' in file_path.name:
            parts = file_path.name.split('.')
            if len(parts) > 2:
                # Try with the last two parts (e.g., ".tar.gz")
                double_ext = '.' + '.'.join(parts[-2:])
                double_ext = double_ext.lower()
                if double_ext in self._extension_to_category:
                    return self._extension_to_category[double_ext]
        # Default: uncategorized
        return "others"


# --- Self-test block ---
if __name__ == "__main__":
    # Quick test using a temporary directory
    import tempfile
    import os

    # Create a dummy ruleset
    test_rules = {
        "images": [".jpg", ".png"],
        "documents": [".txt", ".pdf"],
        "others": []
    }

    # Create a temporary directory with some dummy files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "photo.jpg").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "data.csv").touch()  # no rule → goes to "others"
        (tmp_path / "subfolder").mkdir()
        (tmp_path / "subfolder" / "image.png").touch()

        # Test non-recursive scan
        scanner = FileScanner(test_rules, recursive=False)
        result = scanner.scan(tmp_path)

        print("🔍 Non-recursive scan results:")
        for cat, files in result.items():
            print(f"  📁 {cat}: {[f.name for f in files]}")

        # Test recursive scan
        scanner_rec = FileScanner(test_rules, recursive=True)
        result_rec = scanner_rec.scan(tmp_path)

        print("\n🔍 Recursive scan results:")
        for cat, files in result_rec.items():
            print(f"  📁 {cat}: {[f.name for f in files]}")
