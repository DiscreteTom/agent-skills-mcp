"""Local file-based prompt loader."""

import frontmatter
from pathlib import Path
from typing import Iterator
from ..model import SkillData
from ..interfaces import (
    FileSystemInterface,
    DefaultFileSystem,
    LoggerInterface,
    DefaultLogger,
)


def _extract_string_field(
    metadata: dict,
    field: str,
    default: str,
    file_path: Path,
    *,
    logger: LoggerInterface,
) -> str:
    """Extract and validate a string field from frontmatter metadata."""
    value = metadata.get(field)
    if value is None:
        return default
    elif isinstance(value, str):
        return value
    else:
        logger.warning(
            f"'{field}' field in {file_path} is not a string, converting to string"
        )
        return str(value)


def _parse_markdown_file(
    md_file: Path,
    folder: Path,
    content: str,
    *,
    logger: LoggerInterface,
) -> SkillData:
    """Parse a single markdown file into PromptData."""
    post = frontmatter.loads(content)

    name = _extract_string_field(
        post.metadata, "name", md_file.stem, md_file, logger=logger
    )
    description = _extract_string_field(
        post.metadata,
        "description",
        "",
        md_file,
        logger=logger,
    )

    return SkillData(name, description, post.content)


def scan_skills(
    folder: Path,
    *,
    fs: FileSystemInterface = DefaultFileSystem(),
    logger: LoggerInterface = DefaultLogger(),
) -> Iterator[SkillData]:
    """
    Scan folder recursively for markdown files.

    Args:
        folder_path: Path to folder to scan
        fs: File system interface for file operations
        logger: Logger interface for warning messages

    Yields:
        PromptData for each markdown file
    """
    if not fs.exists(folder) or not fs.is_dir(folder):
        logger.warning(
            f"folder path '{str(folder)}' does not exist or is not a directory"
        )
        return

    for md_file in fs.glob_skills(folder):
        try:
            content = fs.read_text(md_file)
            prompt_data = _parse_markdown_file(md_file, folder, content, logger=logger)
            yield prompt_data
        except Exception as e:
            logger.warning(f"failed to process {md_file}: {e}")
            continue
