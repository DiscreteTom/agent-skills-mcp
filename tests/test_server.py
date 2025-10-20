"""Tests for server module."""

from pathlib import Path
from unittest.mock import Mock, patch

from agent_skills_mcp.config import Config, Mode
from agent_skills_mcp.model import SkillData
from agent_skills_mcp.server import (
    _build_system_prompt_instructions,
    _format_tool_name,
    _format_tool_description,
    create_mcp_server,
)


def test_build_system_prompt_instructions():
    """Test building system prompt instructions."""
    skills = [
        SkillData("skill1", "Description 1", "Content 1", Path("skill1.md")),
        SkillData("skill2", "Description 2", "Content 2", Path("dir/skill2.md")),
    ]
    skill_folder = Path("/base")

    result = _build_system_prompt_instructions(iter(skills), skill_folder)

    assert "This MCP server is just a loader of skills" in result
    assert "## skill1" in result
    assert "Description 1" in result
    assert "Path: /base/skill1.md" in result
    assert "## skill2" in result
    assert "Description 2" in result
    assert "Path: /base/dir/skill2.md" in result


def test_format_tool_name():
    """Test tool name formatting."""
    assert _format_tool_name("test_skill") == "get_skill_test_skill"
    assert _format_tool_name("another") == "get_skill_another"


def test_format_tool_description():
    """Test tool description formatting."""
    assert _format_tool_description("Test description") == "Test description"
    assert _format_tool_description("") == ""


@patch("agent_skills_mcp.server.FastMCP")
def test_create_mcp_server_system_prompt_mode(mock_fastmcp):
    """Test creating MCP server in system prompt mode."""
    mock_mcp = Mock()
    mock_fastmcp.return_value = mock_mcp

    config = Config(skill_folder=Path("skills"), mode=Mode.SYSTEM_PROMPT)
    skills = [SkillData("test", "desc", "content", Path("test.md"))]

    result = create_mcp_server(config, iter(skills))

    mock_fastmcp.assert_called_once()
    call_args = mock_fastmcp.call_args
    assert call_args[1]["name"] == "agent-skills-mcp"
    assert "This MCP server is just a loader of skills" in call_args[1]["instructions"]
    assert result == mock_mcp


@patch("agent_skills_mcp.server.FastMCP")
def test_create_mcp_server_tool_mode(mock_fastmcp):
    """Test creating MCP server in tool mode."""
    mock_mcp = Mock()
    mock_tool_decorator = Mock()
    mock_mcp.tool.return_value = mock_tool_decorator
    mock_fastmcp.return_value = mock_mcp

    config = Config(skill_folder=Path("skills"), mode=Mode.TOOL)
    skills = [SkillData("test", "desc", "test_content", Path("test.md"))]

    result = create_mcp_server(config, iter(skills))

    mock_fastmcp.assert_called_once()
    call_args = mock_fastmcp.call_args
    assert call_args[1]["name"] == "agent-skills-mcp"
    assert call_args[1]["instructions"] == ""
    assert result == mock_mcp

    # Verify tool registration was called
    mock_mcp.tool.assert_called_once()
    tool_call_args = mock_mcp.tool.call_args
    assert tool_call_args[1]["name"] == "get_skill_test"
    assert tool_call_args[1]["description"] == "desc"

    # Test that the tool function returns the correct content
    # The tool decorator should have been called with a function
    tool_func = mock_tool_decorator.call_args[0][0]
    assert tool_func() == "test_content"
