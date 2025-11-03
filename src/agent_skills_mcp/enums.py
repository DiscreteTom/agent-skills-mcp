"""Enums for agent-skills-mcp."""

from enum import Enum


class Mode(Enum):
    """Operating mode for agent skills."""

    TOOL = "tool"
    SYSTEM_PROMPT = "system_prompt"
