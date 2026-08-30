from pathlib import Path
from typing import Dict, List


class FileScanner:
    """
    Scans a directory and classifies files into categories based on extension rules.

    In recursive mode, existing category directories are ignored so the
    organizer does not try to reorganize files that are already organized.
    """

    def __init__(self, rules: Dict[str, List[str]], recursive: bool = False):
        """
        Initialize the scanner.

        Args:
            rules: Dictionary mapping category names to lists of extensions.
            recursive: If True, scan subdirectories recursively.
        """
        self.rules = rules
        self.recursive = recursive

        # Build a reverse mapping: extension -> category
        self._extension_to_category: Dict[str, str] = {}

        for category, extensions in rules.items():
            for ext in extensions:
                self._extension_to_category[ext.lower()] = category

    def scan(self, directory: Path) -> Dict[str, List[Path]]:
        """
        Scan the given directory and classify files.

        Args:
            directory: Directory to scan.

        Returns:
            Dictionary where keys are category names and values are
            lists of file paths.
        """
        if not directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        if not directory.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {directory}"
            )

        classified: Dict[str, List[Path]] = {
            category: []
            for category in self.rules.keys()
        }

        # Ensure there is always an "others" category.
        if "others" not in classified:
            classified["others"] = []

        if self.recursive:
            category_directories = set(self.rules.keys())

            for item in directory.rglob("*"):
                if not item.is_file():
                    continue

                relative_parts = item.relative_to(directory).parts

                # Ignore files already inside a category directory.
                #
                # Example:
                # test_folder/images/photo.jpg
                #
                # "images" is a configured category, so this file
                # should not be scanned again.
                if (
                    relative_parts
                    and relative_parts[0] in category_directories
                ):
                    continue

                category = self._get_category(item)
                classified[category].append(item)

        else:
            for item in directory.iterdir():
                if not item.is_file():
                    continue

                category = self._get_category(item)
                classified[category].append(item)

        return classified

    def _get_category(self, file_path: Path) -> str:
        """
        Determine the category for a file based on its extension.

        Supports both normal extensions such as ".jpg" and multi-part
        extensions such as ".tar.gz".

        Args:
            file_path: Path to the file.

        Returns:
            Category name.
        """
        suffix = file_path.suffix.lower()

        # Normal extension lookup.
        if suffix in self._extension_to_category:
            return self._extension_to_category[suffix]

        # Multi-part extension lookup.
        #
        # Example:
        # archive.tar.gz
        # -> ".tar.gz"
        if "." in file_path.name:
            parts = file_path.name.split(".")

            if len(parts) > 2:
                double_extension = (
                    "." + ".".join(parts[-2:])
                ).lower()

                if double_extension in self._extension_to_category:
                    return self._extension_to_category[
                        double_extension
                    ]

        return "others"


# --- Self-test block ---

if __name__ == "__main__":
    import tempfile

    test_rules = {
        "images": [".jpg", ".png"],
        "documents": [".txt", ".pdf"],
        "others": [],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Files that should be discovered.
        (tmp_path / "photo.jpg").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "data.csv").touch()

        # Existing organized directory.
        (tmp_path / "images").mkdir()

        # This file should NOT be returned by the recursive scan.
        (tmp_path / "images" / "old_photo.jpg").touch()

        # Another unrelated subdirectory.
        (tmp_path / "subfolder").mkdir()
        (tmp_path / "subfolder" / "image.png").touch()

        # ---------------------------------------------------------
        # Non-recursive test
        # ---------------------------------------------------------

        scanner = FileScanner(
            test_rules,
            recursive=False,
        )

        result = scanner.scan(tmp_path)

        print("🔍 Non-recursive scan results:")

        for category, files in result.items():
            print(
                f"  📁 {category}: "
                f"{[file.name for file in files]}"
            )

        # Expected:
        # images: ['photo.jpg']
        # documents: ['notes.txt']
        # others: ['data.csv']

        # ---------------------------------------------------------
        # Recursive test
        # ---------------------------------------------------------

        scanner_recursive = FileScanner(
            test_rules,
            recursive=True,
        )

        result_recursive = scanner_recursive.scan(tmp_path)

        print("\n🔍 Recursive scan results:")

        for category, files in result_recursive.items():
            print(
                f"  📁 {category}: "
                f"{[file.name for file in files]}"
            )

        # Expected:
        #
        # images:
        #   photo.jpg
        #   image.png
        #
        # documents:
        #   notes.txt
        #
        # others:
        #   data.csv
        #
        # images/old_photo.jpg must NOT appear because it is
        # already inside the "images" category directory.
