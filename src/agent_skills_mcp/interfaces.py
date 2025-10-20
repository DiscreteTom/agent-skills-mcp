"""Interfaces for dependency injection and testing."""

import sys
from pathlib import Path
from typing import Iterator, Protocol


class FileSystemInterface(Protocol):
    """Protocol for file system operations."""

    def read_text(self, path: Path) -> str:
        """Read text content from a file."""
        ...

    def glob_skills(self, folder: Path) -> Iterator[Path]:
        """Find all skill files in folder recursively."""
        ...

    def exists(self, path: Path) -> bool:
        """Check if path exists."""
        ...

    def is_dir(self, path: Path) -> bool:
        """Check if path is a directory."""
        ...


class LoggerInterface(Protocol):
    """Protocol for logging operations."""

    def warning(self, message: str) -> None:
        """Log a warning message."""
        ...


class DefaultFileSystem:
    """Default file system implementation using pathlib."""

    def read_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def glob_skills(self, folder: Path) -> Iterator[Path]:
        return folder.rglob("SKILL.md")

    def exists(self, path: Path) -> bool:
        return path.exists()

    def is_dir(self, path: Path) -> bool:
        return path.is_dir()


class DefaultLogger:
    """Default logger implementation using stderr."""

    def warning(self, message: str) -> None:
        print(f"Warning: {message}", file=sys.stderr)
