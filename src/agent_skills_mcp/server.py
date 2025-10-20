"""MCP server setup and configuration."""

from fastmcp import FastMCP
from pathlib import Path
from typing import List

from .scan import scan_skills
from .config import Config, Mode
from .model import SkillData


def _build_system_prompt_instructions(
    skills: List[SkillData], skill_folder: Path
) -> str:
    """Build instructions for system prompt mode."""
    instructions = "Here are the discovered skills:\n"
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


def _format_tool_description(skill_description: str) -> str:
    """Format tool description for skill."""
    return skill_description


def _register_tools(mcp: FastMCP, skills: List[SkillData]):
    """Register tools for each skill."""
    for skill_data in skills:

        @mcp.tool(
            name=_format_tool_name(skill_data.name),
            description=_format_tool_description(skill_data.description),
        )
        def _tool() -> str:
            return skill_data.content


def create_mcp_server(config: Config) -> FastMCP:
    """Create and configure MCP server based on config."""
    skills = list(scan_skills(config.skill_folder))

    instructions = (
        _build_system_prompt_instructions(skills, config.skill_folder)
        if config.mode == Mode.SYSTEM_PROMPT
        else ""
    )

    mcp = FastMCP(
        name="agent-skills-mcp",
        instructions=instructions,
    )

    if config.mode == Mode.TOOL:
        _register_tools(mcp, skills)

    return mcp
