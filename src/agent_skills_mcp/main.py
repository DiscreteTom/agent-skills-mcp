"""Main entry point for the MCP server."""

from fastmcp import FastMCP
from typing import List

from .file.scan import scan_skills
from .config import Config, Mode
from .model import SkillData


def build_system_prompt_instructions(skills: List[SkillData]) -> str:
    """Build instructions for system prompt mode."""
    instructions = "Here are the discovered skills:\n"
    for skill_data in skills:
        instructions += f"""
## {skill_data.name}

> Path: {skill_data.relative_path}

{skill_data.description}

"""
    return instructions


def format_tool_name(skill_name: str) -> str:
    """Format tool name for skill."""
    return f"get_skill_{skill_name}"


def format_tool_description(skill_description: str) -> str:
    """Format tool description for skill."""
    return skill_description


def register_tools(mcp: FastMCP, skills: List[SkillData]):
    """Register tools for each skill."""
    for skill_data in skills:

        @mcp.tool(
            name=format_tool_name(skill_data.name),
            description=format_tool_description(skill_data.description),
        )
        def _tool() -> str:
            return skill_data.content


def main():
    """Start the MCP server."""
    config = Config.from_env()
    skills = list(scan_skills(config.skill_folder))

    instructions = (
        build_system_prompt_instructions(skills)
        if config.mode == Mode.SYSTEM_PROMPT
        else ""
    )

    mcp = FastMCP(
        name="agent-skills-mcp",
        instructions=instructions,
    )

    if config.mode == Mode.TOOL:
        register_tools(mcp, skills)

    mcp.run()


if __name__ == "__main__":
    main()
