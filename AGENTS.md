# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## Project Overview

This is a Claude Code plugin monorepo ("psycoder-tools") containing three plugins that extend Claude Code with custom commands, agents, and skills.

### Plugins

| Plugin | Purpose |
|--------|---------|
| **base** | Git workflow commands (commit, create-pr, review-code) with conventional commit format, emoji support, and code review |
| **task** | Task planning and execution system with code analysis agents (explorer, architect) |
| **nearville-figma** | Figma design-to-code implementation for React Native with MCP server integration |

### Repository Structure

```
claude-plugin/
├── .claude-plugin/marketplace.json    # Plugin registry (canonical versions)
├── base/                              # Git workflow plugin
├── task/                              # Task management plugin
├── nearville-figma/                   # Figma integration plugin
├── CLAUDE.md                          # Project documentation
└── AGENTS.md                          # This file
```

---

## Build/Lint/Test Commands

This is a documentation-only repository with no build system, automated tests, or linting.

| Action | Command |
|--------|---------|
| Validate JSON syntax | Manual review or JSON linter |
| Test plugins | Load via Claude Code and verify functionality |
| Validate markdown | Ensure YAML frontmatter parses correctly |

There are no `npm`, `pnpm`, or other package manager scripts in this repository.

---

## File Structure & Organization

### Plugin Directory Layout

Each plugin follows this structure:

```
<plugin>/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata and version
├── commands/
│   └── <category>/          # Optional subdirectory grouping
│       └── <command>.md     # Slash command definition
├── agents/
│   └── <agent-name>.md      # Agent definition
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md         # Skill definition (required filename)
│       └── references/      # Optional supporting files
├── hooks/                   # Optional Python pre-commit hooks
└── README.md                # Plugin documentation
```

### Root Configuration

- `.claude-plugin/marketplace.json` - Registry of all plugins with versions
- `CLAUDE.md` - Project overview and conventions
- `AGENTS.md` - AI agent instructions (this file)

---

## Markdown File Formats

### Commands (`commands/<name>.md`)

YAML frontmatter fields:

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | What the command does |
| `allowed-tools` | No | Tools the command can use (e.g., `Bash(git add:*)`) |
| `argument-hint` | No | Expected arguments shown to user |
| `model` | No | LLM model (`claude-haiku-4-5-20251001`, `sonnet`) |
| `disable-model-invocation` | No | Set `true` to prevent model auto-invocation |

Body content provides detailed instructions for command execution.

### Agents (`agents/<name>.md`)

YAML frontmatter fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier (lowercase, hyphenated) |
| `description` | Yes | What the agent does and when to use it |
| `tools` | Yes | Comma-separated list of available tools |
| `model` | Yes | LLM model (typically `sonnet`) |
| `color` | No | Visual indicator in UI |

Body content defines the agent's role, process, and output format.

### Skills (`skills/<name>/SKILL.md`)

YAML frontmatter fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (lowercase, hyphenated) |
| `description` | Yes | Trigger phrases and usage context |
| `allowed-tools` | No | MCP tools the skill can access |

Body content structure:
- Title with `#` header
- Introduction with core principles
- "Announce at start" instruction
- Phased workflow with `## Phase N: Title` headers
- Each phase has Goal and Actions subsections

---

## JSON Configuration

### Plugin Configuration (`<plugin>/.claude-plugin/plugin.json`)

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier |
| `description` | Yes | Brief plugin description |
| `version` | Yes | Semantic version (e.g., `1.0.2`) |
| `author` | Yes | Object with `name` field |
| `mcpServers` | No | MCP server configurations |

MCP server configuration (when needed):
- `type`: Connection type (`http`)
- `url`: Server endpoint URL

### Marketplace Registry (`.claude-plugin/marketplace.json`)

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Marketplace name |
| `owner` | Yes | Object with `name` and `email` |
| `plugins` | Yes | Array of plugin entries |

Each plugin entry mirrors `plugin.json` fields plus `source` (relative path).

Use 4-space indentation for all JSON files.

---

## Version Management

### Canonical Version Source

The authoritative version for each plugin is in `.claude-plugin/marketplace.json`.

### Version Sync Requirements

When updating a plugin version, update both files:

1. `.claude-plugin/marketplace.json` - Marketplace registry entry
2. `<plugin>/.claude-plugin/plugin.json` - Plugin's own metadata

The README.md version table is informational and may lag behind.

### Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH` (e.g., `1.1.5`)

---

## Naming & Style Conventions

### Naming Patterns

| Component | Convention | Examples |
|-----------|------------|----------|
| Plugin names | lowercase, hyphenated | `base`, `task`, `nearville-figma` |
| Command files | lowercase, hyphenated | `commit.md`, `create-pr.md` |
| Agent files | lowercase, hyphenated | `code-explorer.md`, `code-architect.md` |
| Skill directories | lowercase, hyphenated | `planning-tasks`, `implement-design` |

### Agent Color Coding

| Color | Role |
|-------|------|
| `green` | Architect (design, planning) |
| `yellow` | Explorer (analysis, discovery) |
| `red` | Reviewer (validation, quality) |

### Tool Reference Formats

- Standard tools: Comma-separated list (`Glob, Grep, LS, Read, WebFetch`)
- Bash tools: Pattern-based (`Bash(git add:*)`, `Bash(git status:*)`)
- MCP tools: Full path (`mcp__<plugin>_<server>__<tool>`)

### Skill Invocation Pattern

Commands that delegate to skills use this pattern in their body:
```
Invoke the <plugin>:<skill> skill and follow it exactly as presented to you.
```

### Skill Description Triggers

Include common trigger phrases in skill descriptions to help with automatic matching:
- "Use when user says..."
- "Use when implementing..."
- List variations: "plan a feature", "create a task plan", "break down this work"

---

## Common Modifications

### Adding a New Command

1. Create `<plugin>/commands/<name>.md` with YAML frontmatter
2. Define `description` (required) and other relevant fields
3. Write instruction body with clear steps

### Adding a New Agent

1. Create `<plugin>/agents/<name>.md` with YAML frontmatter
2. Define `name`, `description`, `tools`, `model`, and optionally `color`
3. Write role definition with process and output guidance

### Adding a New Skill

1. Create directory `<plugin>/skills/<skill-name>/`
2. Create `SKILL.md` with YAML frontmatter
3. Structure body with phases, goals, and actions
4. Add `references/` subdirectory if supporting files needed

### Releasing a New Version

1. Update version in `.claude-plugin/marketplace.json`
2. Update version in `<plugin>/.claude-plugin/plugin.json`
3. Optionally update `<plugin>/README.md` and root `README.md`
