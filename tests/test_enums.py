"""Tests for enums module."""

from agent_skills_mcp.enums import Mode


def test_mode_enum_values():
    """Test Mode enum has correct values."""
    assert Mode.TOOL.value == "tool"
    assert Mode.SYSTEM_PROMPT.value == "system_prompt"


def test_mode_enum_members():
    """Test Mode enum has expected members."""
    assert hasattr(Mode, "TOOL")
    assert hasattr(Mode, "SYSTEM_PROMPT")
    assert len(Mode) == 2
