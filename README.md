# agent-skills-mcp - Load [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) for your agents

[![PyPI - Version](https://img.shields.io/pypi/v/agent-skills-mcp)](https://pypi.org/project/agent-skills-mcp/)
![Codecov](https://img.shields.io/codecov/c/github/DiscreteTom/agent-skills-mcp)

## Usage

### Installation

[![Add to Kiro](https://kiro.dev/images/add-to-kiro.svg)](kiro://kiro.mcp/add?name=skills&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22agent-skills-mcp%22%5D%2C%22env%22%3A%7B%22SKILL_FOLDER%22%3A%22skills%22%2C%22MODE%22%3A%22tool%22%7D%7D)

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

> For Cursor, add the configuration to `.cursor/mcp.json` in your workspace to read from workspace's `skills` folder.

### Modes

- `system_prompt`: Include skill information in MCP instructions (recommended if your agent regards MCP server instructions)
- `tool`: Register skills as MCP tools (fallback mode since many agents ignore MCP server instructions)

### Environment Variables

- `SKILL_FOLDER`: Path to folder containing skill markdown files (optional, defaults to `skills`)
- `MODE`: Operating mode (optional, defaults to `tool`)

## [CHANGELOG](./CHANGELOG.md)
