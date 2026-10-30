# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code and Codex plugin marketplace ("psycoder-tools") with one active plugin:

- **review** - `/review-setup` (repo-specific REVIEW.md + optional PR reviewer) and `/local-review`

`archive/` holds retired plugins (base, task, nearville-figma). They are not in
`marketplace.json`; do not edit or version them.

## Architecture

```
claude-plugin/
├── .claude-plugin/
│   └── marketplace.json    # Plugin registry (versions here!)
├── review/
│   ├── .claude-plugin/plugin.json  # Claude metadata
│   ├── .codex-plugin/plugin.json   # Codex metadata (same version)
│   └── skills/             # review-setup (+ templates/, hook tests), local-review
└── archive/                # Retired plugins, not installable
```

Review hook tests: `python3 -m unittest discover -s review/skills/review-setup`.

## Version Management

When updating a plugin version, update all files:
1. `<plugin>/.claude-plugin/plugin.json` - Plugin's own version
2. `.claude-plugin/marketplace.json` - Marketplace registry entry
3. `<plugin>/.codex-plugin/plugin.json` - Codex metadata (same version)
4. Update the relevant documents.

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

