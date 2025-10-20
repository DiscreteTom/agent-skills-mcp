"""Tests for model module."""

from pathlib import Path
from agent_skills_mcp.model import SkillData


def test_skill_data_creation():
    skill = SkillData(
        name="test_skill",
        description="A test skill",
        content="This is test content",
        relative_path=Path("test.md"),
    )

    assert skill.name == "test_skill"
    assert skill.description == "A test skill"
    assert skill.content == "This is test content"
    assert skill.relative_path == Path("test.md")


def test_skill_data_equality():
    skill1 = SkillData("name", "desc", "content", Path("test.md"))
    skill2 = SkillData("name", "desc", "content", Path("test.md"))
    skill3 = SkillData("other", "desc", "content", Path("test.md"))

    assert skill1 == skill2
    assert skill1 != skill3
