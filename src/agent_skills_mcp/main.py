"""Main entry point for the MCP server."""

from .config import Config
from .server import create_mcp_server


def main():
    """Start the MCP server."""
    config = Config.from_env()
    mcp = create_mcp_server(config)
    mcp.run()


if __name__ == "__main__":
    main()
