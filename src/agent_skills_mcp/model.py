from dataclasses import dataclass


@dataclass
class SkillData:
    """Complete prompt data loaded from markdown file.

    Attributes:
        name: Unique identifier for the prompt
        title: Display title for the prompt
        description: Brief description of prompt purpose
        arguments: Template arguments this prompt accepts
        content: Template content for variable substitution
    """

    name: str
    description: str
    content: str
