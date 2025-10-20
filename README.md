# agent-skills-mcp - Load [agent skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) as MCP tools

[![PyPI - Version](https://img.shields.io/pypi/v/agent-skills-mcp)](https://pypi.org/project/agent-skills-mcp/)
![Codecov](https://img.shields.io/codecov/c/github/DiscreteTom/agent-skills-mcp)

## Usage

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=skills&config=eyJjb21tYW5kIjoidXZ4IGFnZW50LXNraWxscy1tY3AifQ%3D%3D)

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
