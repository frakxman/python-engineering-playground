import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Import the logger setup from our module
from logger import get_logger

# Get a logger instance for this module
logger = get_logger("Organizer")


class Organizer:
    """
    Handles the physical organization of files: moving them to categorized folders.
    Supports both real execution and dry-run simulation.
    """

    def __init__(self, base_path: Path, dry_run: bool = False):
        """
        Initialize the organizer.

        Args:
            base_path: The root directory where organized folders will be created.
            dry_run: If True, only simulate operations without actually moving files.
        """
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        self.stats = {
            "moved": 0,
            "skipped": 0,
            "errors": 0
        }

    def organize(self, classified_files: Dict[str, List[Path]]) -> None:
        """
        Organize files by moving them to their respective category folders.

        Args:
            classified_files: Dictionary mapping category names to lists of file paths.
        """
        if self.dry_run:
            logger.info("🚀 DRY-RUN MODE: No files will be actually moved.")
        else:
            logger.info("🚀 Starting file organization (real execution).")

        for category, files in classified_files.items():
            # Skip empty categories
            if not files:
                continue

            # Create the destination folder (e.g., "Images/")
            dest_folder = self.base_path / category
            self._ensure_folder_exists(dest_folder)

            for file_path in files:
                self._move_file(file_path, dest_folder)

        # Log summary
        if self.dry_run:
            logger.info(f"✅ DRY-RUN completed. {self.stats['moved']} files would be moved.")
        else:
            logger.info(f"✅ Organization completed. Moved {self.stats['moved']} files, skipped {self.stats['skipped']}, errors: {self.stats['errors']}.")

    def _ensure_folder_exists(self, folder: Path) -> None:
        """
        Create a folder if it doesn't exist.

        Args:
            folder: Path object of the folder to create.
        """
        try:
            folder.mkdir(exist_ok=True)
            if self.dry_run:
                logger.debug(f"[DRY-RUN] Would create folder: {folder}")
        except PermissionError as e:
            logger.error(f"Permission denied while creating {folder}: {e}")
            self.stats["errors"] += 1

    def _move_file(self, source: Path, dest_folder: Path) -> None:
        """
        Move a single file to the destination folder, handling name conflicts.

        Args:
            source: Path to the source file.
            dest_folder: Destination folder Path.
        """
        # Generate destination path
        dest_path = dest_folder / source.name

        # Handle name conflicts (add _1, _2, etc.)
        dest_path = self._resolve_conflict(dest_path)

        try:
            if self.dry_run:
                # Just log the intended action
                logger.info(f"[DRY-RUN] Would move: {source} → {dest_path}")
                self.stats["moved"] += 1
            else:
                # Actually move the file
                shutil.move(str(source), str(dest_path))
                logger.debug(f"Moved: {source} → {dest_path}")
                self.stats["moved"] += 1

        except PermissionError as e:
            logger.error(f"Permission denied moving {source}: {e}")
            self.stats["errors"] += 1
        except OSError as e:
            logger.error(f"OS error moving {source}: {e}")
            self.stats["errors"] += 1
        except Exception as e:
            logger.error(f"Unexpected error moving {source}: {e}")
            self.stats["errors"] += 1

    def _resolve_conflict(self, dest_path: Path) -> Path:
        """
        Resolve name conflicts by adding a numeric suffix if the file already exists.

        Example: If "photo.jpg" exists, returns "photo_1.jpg", then "photo_2.jpg", etc.

        Args:
            dest_path: The desired destination Path.

        Returns:
            A Path with a unique name (no conflict).
        """
        if not dest_path.exists():
            return dest_path

        # Separate stem (name without extension) and suffix (extension with dot)
        stem = dest_path.stem
        suffix = dest_path.suffix

        counter = 1
        while True:
            # Build new name: "name_1.ext", "name_2.ext", etc.
            new_name = f"{stem}_{counter}{suffix}"
            new_path = dest_path.parent / new_name

            if not new_path.exists():
                return new_path

            counter += 1


# --- Self-test block ---
if __name__ == "__main__":
    import tempfile
    import os

    print("🧪 Testing Organizer...")

    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create some dummy files
        (tmp_path / "photo.jpg").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "data.csv").touch()

        # Create a classified structure (as if scanned)
        classified = {
            "images": [tmp_path / "photo.jpg"],
            "documents": [tmp_path / "notes.txt"],
            "others": [tmp_path / "data.csv"]
        }

        # Test with dry-run first
        print("\n🔍 Testing DRY-RUN mode...")
        organizer_dry = Organizer(tmp_path, dry_run=True)
        organizer_dry.organize(classified)

        # Verify no files were actually moved
        print(f"   Files still in root: {[f.name for f in tmp_path.iterdir() if f.is_file()]}")
        print(f"   Dry-run moved count: {organizer_dry.stats['moved']} (should be 3)")

        # Test real execution
        print("\n🔍 Testing REAL execution...")
        organizer_real = Organizer(tmp_path, dry_run=False)
        organizer_real.organize(classified)

        # Verify files are now in subfolders
        print(f"   Root now contains: {[f.name for f in tmp_path.iterdir() if f.is_dir()]}")
        for category in ["images", "documents", "others"]:
            folder = tmp_path / category
            if folder.exists():
                print(f"   📁 {category}: {[f.name for f in folder.iterdir()]}")
            else:
                print(f"   ❌ {category} folder not found")

        print(f"\n✅ Real execution stats: {organizer_real.stats}")