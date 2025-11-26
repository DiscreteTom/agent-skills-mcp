"""Tests for interfaces module."""

import sys
from io import StringIO
from agent_skills_mcp.interfaces import DefaultFileSystem, DefaultLogger


def test_default_filesystem_read_text(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello world", encoding="utf-8")

    fs = DefaultFileSystem()
    content = fs.read_text(test_file)

    assert content == "Hello world"


def test_default_filesystem_glob_skills(tmp_path):
    (tmp_path / "SKILL.md").write_text("skill1")
    (tmp_path / "other.md").write_text("other")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "SKILL.md").write_text("skill2")

    fs = DefaultFileSystem()
    skill_files = list(fs.glob_skills(tmp_path))

    assert len(skill_files) == 2
    assert all(f.name == "SKILL.md" for f in skill_files)


def test_default_filesystem_glob_skills_follows_symlinks(tmp_path):
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    (target_dir / "SKILL.md").write_text("skill_in_target")

    link_dir = tmp_path / "link"
    link_dir.symlink_to(target_dir)

    fs = DefaultFileSystem()
    skill_files = list(fs.glob_skills(tmp_path))

    assert len(skill_files) == 2
    paths = {f.parent.name for f in skill_files}
    assert paths == {"target", "link"}


def test_default_filesystem_exists(tmp_path):
    test_file = tmp_path / "exists.txt"
    test_file.write_text("content")

    fs = DefaultFileSystem()

    assert fs.exists(test_file) is True
    assert fs.exists(tmp_path / "nonexistent.txt") is False


def test_default_filesystem_is_dir(tmp_path):
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    test_dir = tmp_path / "subdir"
    test_dir.mkdir()

    fs = DefaultFileSystem()

    assert fs.is_dir(test_dir) is True
    assert fs.is_dir(test_file) is False


def test_default_logger_warning():
    logger = DefaultLogger()
    captured = StringIO()
    old_stderr = sys.stderr
    sys.stderr = captured

    logger.warning("test warning message")

    sys.stderr = old_stderr
    output = captured.getvalue()

    assert "Warning: test warning message" in output
