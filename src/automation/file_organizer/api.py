from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.automation.file_organizer.config_loader import (
    ConfigError,
    load_rules,
)
from src.automation.file_organizer.models import (
    FileOperation,
    FileOrganizerPreview,
    FileOrganizerRequest,
    FileOrganizerResult,
)
from src.automation.file_organizer.organizer import Organizer
from src.automation.file_organizer.scanner import FileScanner


app = FastAPI(
    title="File Organizer API",
    description="API for previewing and organizing files.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


RULES_PATH = Path(__file__).parent / "rules.json"


def _load_scanner(recursive: bool) -> FileScanner:
    """
    Load the configured sorting rules and create a FileScanner.
    """
    try:
        rules = load_rules(RULES_PATH)
    except ConfigError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load File Organizer rules: {error}",
        ) from error

    return FileScanner(
        rules,
        recursive=recursive,
    )


def _validate_directory(path: str) -> Path:
    """
    Validate and normalize the target directory.
    """
    directory = Path(path).expanduser().resolve()

    if not directory.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Directory not found: {directory}",
        )

    if not directory.is_dir():
        raise HTTPException(
            status_code=400,
            detail=f"Path is not a directory: {directory}",
        )

    return directory


def _resolve_destination(
    destination_folder: Path,
    filename: str,
    reserved_destinations: set[Path] | None = None,
) -> Path:
    """
    Resolve a unique destination path for a file.

    A destination is considered unavailable if it either:
    - already exists on disk, or
    - has already been reserved by another operation in the
      current preview.

    Examples:

        photo.jpg
        photo_1.jpg
        photo_2.jpg
        ...
    """
    if reserved_destinations is None:
        reserved_destinations = set()

    destination = destination_folder / filename

    if (
        not destination.exists()
        and destination not in reserved_destinations
    ):
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = (
            destination_folder
            / f"{stem}_{counter}{suffix}"
        )

        if (
            not candidate.exists()
            and candidate not in reserved_destinations
        ):
            return candidate

        counter += 1


def _build_preview_operations(
    directory: Path,
    classified_files: dict[str, list[Path]],
) -> list[FileOperation]:
    """
    Build the filesystem operations that would be performed.

    This function only plans operations. It does not create folders
    or move files.

    All files are centralized directly into their category folder,
    even when they were discovered inside nested directories.
    """
    operations: list[FileOperation] = []

    # Track destinations planned during this preview.
    #
    # This is necessary because planned files do not exist on disk yet,
    # so checking Path.exists() alone is not enough to detect conflicts.
    planned_destinations: set[Path] = set()

    for category, files in classified_files.items():
        if not files:
            continue

        destination_folder = directory / category

        for file_path in files:
            destination = _resolve_destination(
                destination_folder,
                file_path.name,
                planned_destinations,
            )

            planned_destinations.add(destination)

            operations.append(
                FileOperation(
                    source=str(file_path),
                    destination=str(destination),
                    category=category,
                )
            )

    return operations


@app.post(
    "/file-organizer/preview",
    response_model=FileOrganizerPreview,
)
def preview_file_organization(
    request: FileOrganizerRequest,
):
    """
    Scan a directory and return the operations that would be performed.

    This endpoint never modifies the filesystem.
    """
    directory = _validate_directory(request.path)
    scanner = _load_scanner(request.recursive)

    try:
        classified_files = scanner.scan(directory)

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to scan directory: {error}",
        ) from error

    categories = {
        category: len(files)
        for category, files in classified_files.items()
    }

    total_files = sum(categories.values())

    operations = _build_preview_operations(
        directory,
        classified_files,
    )

    return FileOrganizerPreview(
        path=str(directory),
        recursive=request.recursive,
        total_files=total_files,
        categories=categories,
        operations=operations,
    )


@app.post(
    "/file-organizer/organize",
    response_model=FileOrganizerResult,
)
def organize_files(
    request: FileOrganizerRequest,
):
    """
    Scan and organize files by physically moving them.
    """
    directory = _validate_directory(request.path)
    scanner = _load_scanner(request.recursive)

    try:
        classified_files = scanner.scan(directory)

        organizer = Organizer(
            directory,
            dry_run=False,
        )

        organizer.organize(classified_files)

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: {error}",
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Filesystem error: {error}",
        ) from error

    return FileOrganizerResult(
    path=str(directory),
    recursive=request.recursive,
    dry_run=False,
    moved=organizer.stats["moved"],
    skipped=organizer.stats["skipped"],
    errors=organizer.stats["errors"],
)

