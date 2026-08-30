from pathlib import Path

from pydantic import BaseModel, Field


class FileOrganizerRequest(BaseModel):
    path: str = Field(
        ...,
        description="Target directory to scan or organize.",
    )
    recursive: bool = Field(
        default=False,
        description="Whether to scan subdirectories recursively.",
    )


class FileOperation(BaseModel):
    source: str
    destination: str
    category: str


class FileOrganizerPreview(BaseModel):
    path: str
    recursive: bool
    total_files: int
    categories: dict[str, int]
    operations: list[FileOperation]


class FileOrganizerResult(BaseModel):
    path: str
    recursive: bool
    dry_run: bool
    moved: int
    skipped: int
    errors: int
