"""Main entry point for the MCP server."""

from .config import Config
from .scan import scan_skills
from .server import create_mcp_server


def main():
    """Start the MCP server."""
    config = Config.from_env()
    skills = scan_skills(config.skill_folder)
    mcp = create_mcp_server(config, skills)
    mcp.run()


if __name__ == "__main__":
    main()
