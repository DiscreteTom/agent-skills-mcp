"""Configuration management for agent-skills-mcp."""

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Mode(Enum):
    """Operating mode for agent skills."""

    TOOL = "tool"
    SYSTEM_PROMPT = "system_prompt"


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    skill_folder: Path
    mode: Mode

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        skill_folder_str = os.getenv("SKILL_FOLDER", "skills")
        skill_folder = Path(skill_folder_str)

        mode_str = os.getenv("MODE", "system_prompt")
        try:
            mode = Mode(mode_str)
        except ValueError:
            raise ValueError(
                f"Invalid MODE value: {mode_str}. Must be one of: {', '.join([m.value for m in Mode])}"
            )

        return cls(
            skill_folder=skill_folder,
            mode=mode,
        )
