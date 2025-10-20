"""Tests for model module."""

from agent_skills_mcp.model import SkillData


def test_skill_data_creation():
    skill = SkillData(
        name="test_skill", description="A test skill", content="This is test content"
    )

    assert skill.name == "test_skill"
    assert skill.description == "A test skill"
    assert skill.content == "This is test content"


def test_skill_data_equality():
    skill1 = SkillData("name", "desc", "content")
    skill2 = SkillData("name", "desc", "content")
    skill3 = SkillData("other", "desc", "content")

    assert skill1 == skill2
    assert skill1 != skill3
