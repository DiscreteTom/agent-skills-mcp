# agent-skills-mcp - Load [agent skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) as MCP tools

[![PyPI - Version](https://img.shields.io/pypi/v/agent-skills-mcp)](https://pypi.org/project/agent-skills-mcp/)

<!-- ![Codecov](https://img.shields.io/codecov/c/github/DiscreteTom/agent-skills-mcp) -->

## Usage

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["agent-skills-mcp"]
    }
  }
}
```

## [CHANGELOG](./CHANGELOG.md)
