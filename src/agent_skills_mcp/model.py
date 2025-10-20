from dataclasses import dataclass
from pathlib import Path


@dataclass
class SkillData:
    """Complete skill data loaded from markdown file.

    Attributes:
        name: Unique identifier for the skill
        description: Brief description of skill purpose
        content: Skill content from markdown file
        relative_path: Relative path from scan folder to the skill file
    """

    name: str
    description: str
    content: str
    relative_path: Path
