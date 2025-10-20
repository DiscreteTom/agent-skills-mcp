from dataclasses import dataclass
from pathlib import Path


@dataclass
class SkillData:
    """Complete prompt data loaded from markdown file.

    Attributes:
        name: Unique identifier for the prompt
        title: Display title for the prompt
        description: Brief description of prompt purpose
        arguments: Template arguments this prompt accepts
        content: Template content for variable substitution
        relative_path: Relative path from scan folder to the skill file
    """

    name: str
    description: str
    content: str
    relative_path: Path
