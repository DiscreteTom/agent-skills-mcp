"""Tests for scan module."""

from pathlib import Path
from agent_skills_mcp.scan import scan_skills, _parse_markdown_file


class MockFileSystem:
    def __init__(self, files=None):
        self.files = files or {}
        self.skill_files = []

    def read_text(self, path: Path) -> str:
        return self.files.get(str(path), "")

    def glob_skills(self, folder: Path):
        return iter(self.skill_files)

    def exists(self, path: Path) -> bool:
        return str(path) in self.files or str(path) == "/skills"

    def is_dir(self, path: Path) -> bool:
        return str(path) == "/skills"


class MockLogger:
    def __init__(self):
        self.warnings = []

    def warning(self, message: str) -> None:
        self.warnings.append(message)


def test_parse_markdown_file_with_frontmatter():
    content = """---
name: test_skill
description: A test skill
---
This is the skill content."""

    logger = MockLogger()
    result = _parse_markdown_file(Path("test.md"), Path("."), content, logger=logger)

    assert result.name == "test_skill"
    assert result.description == "A test skill"
    assert result.content == "This is the skill content."
    assert result.relative_path == Path("test.md")


def test_parse_markdown_file_without_frontmatter():
    content = "Just plain content"

    logger = MockLogger()
    result = _parse_markdown_file(Path("test.md"), Path("."), content, logger=logger)

    assert result.name == "test"
    assert result.description == ""
    assert result.content == "Just plain content"
    assert result.relative_path == Path("test.md")


def test_parse_markdown_file_with_non_string_fields():
    """Test parsing with non-string frontmatter fields."""
    content = """---
name: 123
description: 456
---
Content"""

    logger = MockLogger()
    result = _parse_markdown_file(Path("test.md"), Path("."), content, logger=logger)

    assert result.name == "123"
    assert result.description == "456"
    assert len(logger.warnings) == 2
    assert "'name' field in test.md is not a string" in logger.warnings[0]
    assert "'description' field in test.md is not a string" in logger.warnings[1]


def test_scan_skills_success():
    fs = MockFileSystem(
        {
            "/skills/SKILL.md": """---
name: example
description: Example skill
---
Example content"""
        }
    )
    fs.skill_files = [Path("/skills/SKILL.md")]

    logger = MockLogger()
    skills = list(scan_skills(Path("/skills"), fs=fs, logger=logger))

    assert len(skills) == 1
    assert skills[0].name == "example"
    assert skills[0].description == "Example skill"


def test_scan_skills_nonexistent_folder():
    fs = MockFileSystem()
    logger = MockLogger()

    skills = list(scan_skills(Path("/nonexistent"), fs=fs, logger=logger))

    assert len(skills) == 0
    assert len(logger.warnings) == 1


def test_scan_skills_with_file_processing_error():
    """Test scan_skills handles file processing errors gracefully."""

    class ErrorFileSystem(MockFileSystem):
        def read_text(self, path: Path) -> str:
            raise IOError("File read error")

    fs = ErrorFileSystem()
    fs.skill_files = [Path("/skills/error.md")]

    logger = MockLogger()
    skills = list(scan_skills(Path("/skills"), fs=fs, logger=logger))

    assert len(skills) == 0
    assert len(logger.warnings) == 1
    assert "failed to process" in logger.warnings[0]
    assert "File read error" in logger.warnings[0]
