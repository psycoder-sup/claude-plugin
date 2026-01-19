# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code Plugin monorepo ("psycoder-tools") containing three plugins:

- **base** - Git workflow commands (commit, create-pr, review-code) with conventional commit format, emoji support, and code review
- **task** - Task planning and execution system with code analysis agents
- **nearville-figma** - Figma design-to-code implementation for React Native

## Architecture

```
claude-plugin/
├── .claude-plugin/
│   └── marketplace.json    # Plugin registry (versions here!)
├── base/
│   ├── .claude-plugin/plugin.json  # Plugin version
│   ├── agents/             # git-operations, code-reviewer
│   ├── commands/           # git/ (commit.md, create-pr.md), code/ (review-code.md)
│   ├── skills/             # git-workflow, worktree
│   └── hooks/              # Shell pre-commit hooks
├── task/
│   ├── .claude-plugin/plugin.json
│   ├── agents/             # code-architect, code-explorer
│   ├── commands/           # plan-task.md, execute-task.md
│   └── skills/             # planning-tasks, executing-tasks
└── nearville-figma/
    ├── .claude-plugin/plugin.json  # Includes MCP server config
    ├── agents/             # design-analyzer, component-matcher
    ├── commands/           # implement-design.md
    └── skills/             # implement-figma-design
```

## Version Management

When updating a plugin version, update all files:
1. `<plugin>/.claude-plugin/plugin.json` - Plugin's own version
2. `.claude-plugin/marketplace.json` - Marketplace registry entry
3. Update the relevant documents.

## Plugin Component Conventions

### Commands (`.md` files)
YAML frontmatter with:
- `description` - What the command does
- `allowed-tools` - Tools the command can use
- `model` - LLM model (haiku, sonnet)
- `argument-hint` - Expected arguments

### Agents (`.md` files)
YAML frontmatter with:
- `name`, `description`, `tools`, `model`
- `color` - Visual indicator (green=architect, yellow=explorer, red=reviewer)

### Skills (`SKILL.md` files)
YAML frontmatter with `name` and `description`, followed by structured phases.

