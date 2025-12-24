# agent-skills-mcp - Load [Agent Skills](https://agentskills.io/home) for your agents

[![PyPI - Version](https://img.shields.io/pypi/v/agent-skills-mcp)](https://pypi.org/project/agent-skills-mcp/)
![Codecov](https://img.shields.io/codecov/c/github/DiscreteTom/agent-skills-mcp)

## Usage

### Full CLI Usage

<details>

<summary><code>uvx agent-skills-mcp --help</code></summary>

```sh
 Usage: agent-skills-mcp [OPTIONS]

 Agent Skills MCP - Load Agent Skills for your agents

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --skill-folder  TEXT                  Path to folder containing skill markdown files [env var: SKILL_FOLDER] [default: skills] │
│ --mode          [tool|system_prompt]  Operating mode [env var: MODE] [default: tool]                                           │
│ --version                             Show version and exit                                                                    │
│ --help                                Show this message and exit.                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

</details>

### Setup

First, put your skills in `~/skills`, e.g.

```sh
git clone https://github.com/anthropics/skills.git ~/skills
```

The server recursively searches for `SKILL.md` files and follows symlinks, allowing flexible skill organization.

Then, add this to your MCP client configuration:

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=skills&config=eyJlbnYiOnsiU0tJTExfRk9MREVSIjoifi9za2lsbHMifSwiY29tbWFuZCI6InV2eCBhZ2VudC1za2lsbHMtbWNwIn0%3D)
[![Add to Kiro](https://kiro.dev/images/add-to-kiro.svg)](https://kiro.dev/launch/mcp/add?name=skills&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22agent-skills-mcp%22%5D%2C%22env%22%3A%7B%22SKILL_FOLDER%22%3A%22~%2Fskills%22%7D%7D)

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["agent-skills-mcp"],
      "env": {
        "SKILL_FOLDER": "~/skills"
      }
    }
  }
}
```

### Modes

- `system_prompt`: Include skill information in MCP instructions (recommended if your agent regards MCP server instructions)
- `tool`: Register skills as MCP tools (fallback mode since many agents ignore MCP server instructions)

## [CHANGELOG](./CHANGELOG.md)
