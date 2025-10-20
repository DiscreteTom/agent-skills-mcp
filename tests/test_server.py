"""Tests for server module."""

from pathlib import Path
from unittest.mock import Mock, patch

from agent_skills_mcp.config import Config, Mode
from agent_skills_mcp.model import SkillData
from agent_skills_mcp.server import (
    _build_system_prompt_instructions,
    _format_tool_name,
    _format_tool_description,
    _register_tools,
    _register_tool,
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
    from pathlib import Path

    expected = """Returns the content of the skill file at: /test/path.md

## Skill Description
Test description
"""
    assert (
        _format_tool_description("Test description", Path("/test/path.md")) == expected
    )


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
    expected_desc = """Returns the content of the skill file at: skills/test.md

## Skill Description
desc
"""
    assert tool_call_args[1]["description"] == expected_desc

    # Test that the tool function returns the correct content
    # The tool decorator should have been called with a function
    tool_func = mock_tool_decorator.call_args[0][0]
    assert tool_func() == "test_content"


def test_register_tools():
    """Test _register_tools function directly."""
    mock_mcp = Mock()
    mock_tool_decorator = Mock()
    mock_mcp.tool.return_value = mock_tool_decorator

    skills = [
        SkillData("skill1", "desc1", "content1", Path("skill1.md")),
        SkillData("skill2", "desc2", "content2", Path("skill2.md")),
    ]
    skill_folder = Path("test_folder")

    _register_tools(mock_mcp, iter(skills), skill_folder)

    # Should have called tool decorator twice
    assert mock_mcp.tool.call_count == 2

    # Check first tool registration
    first_call = mock_mcp.tool.call_args_list[0]
    assert first_call[1]["name"] == "get_skill_skill1"
    assert "test_folder/skill1.md" in first_call[1]["description"]
    assert "desc1" in first_call[1]["description"]


def test_register_tools_multiple_tools_content_isolation():
    """Test that multiple tools return their own content, not the last tool's content."""
    mock_mcp = Mock()

    # Store the actual tool functions that get registered
    registered_tools = []

    def mock_tool_decorator(name, description):
        def decorator(func):
            registered_tools.append((name, description, func))
            return func

        return decorator

    mock_mcp.tool.side_effect = mock_tool_decorator

    skills = [
        SkillData("skill1", "desc1", "content1", Path("skill1.md")),
        SkillData("skill2", "desc2", "content2", Path("skill2.md")),
    ]
    skill_folder = Path("test_folder")

    _register_tools(mock_mcp, iter(skills), skill_folder)

    # Should have registered 2 tools
    assert len(registered_tools) == 2

    # Check that each tool returns its own content
    tool1_name, tool1_desc, tool1_func = registered_tools[0]
    tool2_name, tool2_desc, tool2_func = registered_tools[1]

    assert tool1_name == "get_skill_skill1"
    assert tool2_name == "get_skill_skill2"

    # This is the critical test - each tool should return its own content
    assert tool1_func() == "content1"
    assert tool2_func() == "content2"


def test_register_tool():
    """Test _register_tool function directly."""
    mock_mcp = Mock()
    mock_tool_decorator = Mock()

    def mock_tool_func(name, description):
        def decorator(func):
            mock_tool_decorator(name, description, func)
            return func

        return decorator

    mock_mcp.tool.side_effect = mock_tool_func

    _register_tool(mock_mcp, "test_tool", "Test description", "test_content")

    # Verify tool was registered with correct parameters
    mock_tool_decorator.assert_called_once()
    name, description, func = mock_tool_decorator.call_args[0]

    assert name == "test_tool"
    assert description == "Test description"
    assert func() == "test_content"
