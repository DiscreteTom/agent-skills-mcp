"""Main entry point for the MCP server."""

from fastmcp import FastMCP
from pathlib import Path

from .file.scan import scan_skills


def main():
    """Start the MCP server."""
    mcp = FastMCP(name="agent-skills-mcp")

    for skill_data in scan_skills(Path("skills")):

        @mcp.tool(
            name=f"get_skill_{skill_data.name}", description=skill_data.description
        )
        def _tool() -> str:
            return skill_data.content

    mcp.run()


if __name__ == "__main__":
    main()
