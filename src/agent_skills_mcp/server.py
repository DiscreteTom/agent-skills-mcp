"""MCP server setup and configuration."""

from fastmcp import FastMCP
from pathlib import Path
from typing import Iterator

from .config import Config, Mode
from .model import SkillData


def _build_system_prompt_instructions(
    skills: Iterator[SkillData], skill_folder: Path
) -> str:
    """Build instructions for system prompt mode."""

    instructions = """
This MCP server is just a loader of skills. 
The loading is completed.

Here are the discovered skills and their brief description. 
Read the corresponding SKILL.md file to get familiar with their details:

"""

    for skill_data in skills:
        full_path = skill_folder / skill_data.relative_path
        instructions += f"""
## {skill_data.name}

> Path: {full_path}

{skill_data.description}

"""
    return instructions


def _format_tool_name(skill_name: str) -> str:
    """Format tool name for skill."""
    return f"get_skill_{skill_name}"


def _format_tool_description(skill_description: str, skill_path: Path) -> str:
    """Format tool description for skill."""
    return f"""Returns the content of the skill file at: {skill_path}

## Skill Description
{skill_description}
"""


def _register_tool(mcp: FastMCP, name: str, description: str, content: str):
    """Register a tool function that returns the specified skill content."""

    @mcp.tool(name=name, description=description)
    def _tool() -> str:
        return content


def _register_tools(mcp: FastMCP, skills: Iterator[SkillData], skill_folder: Path):
    """Register tools for each skill."""
    for skill_data in skills:
        full_path = skill_folder / skill_data.relative_path

        _register_tool(
            mcp=mcp,
            name=_format_tool_name(skill_data.name),
            description=_format_tool_description(skill_data.description, full_path),
            content=skill_data.content,
        )


def create_mcp_server(config: Config, skills: Iterator[SkillData]) -> FastMCP:
    """Create and configure MCP server based on config."""
    if config.mode == Mode.SYSTEM_PROMPT:
        instructions = _build_system_prompt_instructions(skills, config.skill_folder)
        mcp = FastMCP(
            name="agent-skills-mcp",
            instructions=instructions,
        )
    else:
        mcp = FastMCP(
            name="agent-skills-mcp",
            instructions="",
        )
        _register_tools(mcp, skills, config.skill_folder)

    return mcp
