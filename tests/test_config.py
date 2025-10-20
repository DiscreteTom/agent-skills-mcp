"""Tests for config module."""

import os
from pathlib import Path
from unittest.mock import patch
import pytest

from agent_skills_mcp.config import Config, Mode


def test_mode_enum_values():
    """Test Mode enum has correct values."""
    assert Mode.TOOL.value == "tool"
    assert Mode.SYSTEM_PROMPT.value == "system_prompt"


def test_config_from_env_defaults():
    """Test Config.from_env with default values."""
    with patch.dict(os.environ, {}, clear=True):
        config = Config.from_env()

        assert config.skill_folder == Path("skills")
        assert config.mode == Mode.TOOL


def test_config_from_env_custom_values():
    """Test Config.from_env with custom environment variables."""
    with patch.dict(os.environ, {"SKILL_FOLDER": "/custom/path", "MODE": "tool"}):
        config = Config.from_env()

        assert config.skill_folder == Path("/custom/path")
        assert config.mode == Mode.TOOL


def test_config_from_env_invalid_mode():
    """Test Config.from_env with invalid mode raises ValueError."""
    with patch.dict(os.environ, {"MODE": "invalid_mode"}):
        with pytest.raises(ValueError, match="Invalid MODE value: invalid_mode"):
            Config.from_env()


def test_config_from_env_system_prompt_mode():
    """Test Config.from_env with system_prompt mode."""
    with patch.dict(os.environ, {"MODE": "system_prompt"}):
        config = Config.from_env()
        assert config.mode == Mode.SYSTEM_PROMPT


def test_config_from_env_invalid_mode_error_message():
    """Test Config.from_env with invalid mode shows all valid modes."""
    with patch.dict(os.environ, {"MODE": "bad_mode"}):
        with pytest.raises(ValueError) as exc_info:
            Config.from_env()

        error_msg = str(exc_info.value)
        assert "Invalid MODE value: bad_mode" in error_msg
        assert "tool" in error_msg
        assert "system_prompt" in error_msg
