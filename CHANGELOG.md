# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Lowered Python requirement from >=3.13 to >=3.10

## [0.1.2] - 2025-10-20

### Fixed

- Fixed closure bug where multiple tools would return the last tool's content instead of their own content

## [0.1.1] - 2025-10-20

### Added

- Configuration system with environment variables `SKILL_FOLDER` and `MODE`
- System prompt mode that includes skill information in MCP instructions
- Configurable skill folder path (defaults to `skills`)

## [0.1.0] - 2025-10-20

### Added

- Load skill files as MCP tools.

[unreleased]: https://github.com/DiscreteTom/agent-skills-mcp/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/DiscreteTom/agent-skills-mcp/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/DiscreteTom/agent-skills-mcp/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/DiscreteTom/agent-skills-mcp/releases/tag/v0.1.0
