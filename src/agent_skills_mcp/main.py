"""Main entry point for the MCP server."""

import typer
from pathlib import Path
from typing_extensions import Annotated
from typing import Optional

from . import __version__
from .enums import Mode
from .scan import scan_skills
from .server import create_mcp_server


def version_callback(value: bool):
    if value:
        print(f"Agent Skills MCP Version: {__version__}")
        raise typer.Exit()


def app(
    skill_folder: Annotated[
        str,
        typer.Option(
            envvar="SKILL_FOLDER",
            help="Path to folder containing skill markdown files",
        ),
    ] = "skills",
    mode: Annotated[
        Mode,
        typer.Option(envvar="MODE", help="Operating mode"),
    ] = Mode.TOOL,
    _version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=version_callback, help="Show version and exit"
        ),
    ] = None,
):
    """Agent Skills MCP - Load Agent Skills for your agents"""
    skill_folder_path = Path(skill_folder)
    skills = scan_skills(skill_folder_path.expanduser().resolve())
    mcp = create_mcp_server(mode, skills, skill_folder_path)
    mcp.run()


def main():
    """Start the MCP server."""
    typer.run(app)


if __name__ == "__main__":
    main()
