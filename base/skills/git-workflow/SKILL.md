---
name: git-workflow
description: Use this skill when the user asks about git workflows, creating commits, making pull requests, branching strategies, conventional commits, or git best practices. Provides guidance on using the git-operations agent for commit creation, PR workflows, and safe git operations.
allowed-tools: Task, Read, Glob, Grep
user-invocable: false
---

# Git Workflow Skill

This skill provides guidance for git operations using conventional commit format with emoji prefixes.

## When to Use This Skill

- Creating commits with proper formatting
- Creating pull requests with comprehensive descriptions
- Understanding branching strategies
- Git best practices and safe operations

## Conventional Commit Format

All commits follow this format:
```
<emoji> <type>(<scope>): <description>
```

### Commit Types and Emojis

| Type | Emoji | Description |
|------|-------|-------------|
| feat | ✨ | New feature |
| fix | 🐛 | Bug fix |
| docs | 📝 | Documentation |
| style | 💄 | Formatting, styling |
| refactor | ♻️ | Code restructuring |
| perf | ⚡️ | Performance improvement |
| test | ✅ | Adding tests |
| chore | 🔧 | Maintenance tasks |
| ci | 👷 | CI/CD changes |
| security | 🔒️ | Security fix |
| deps | ➕/➖ | Add/remove dependencies |
| breaking | 💥 | Breaking changes |

## Using the Git Operations Agent

For complex git operations, delegate to the `base:git-operations` agent:

```
Use the Task tool with:
- subagent_type: "base:git-operations"
- prompt: Describe the git operation needed
```

The agent handles:
- Analyzing changes and grouping related files
- Creating properly formatted commits
- Generating PR descriptions with context
- Safe merge/rebase operations
- Conflict resolution guidance

## Safety Guidelines

1. **Never force push to main/master** without explicit user confirmation
2. **Check for uncommitted changes** before checkout/rebase
3. **Suggest backup branches** before risky operations
4. **Show state before and after** operations

## Commands Available

- `/commit` - Create commits with conventional format
- `/create-pr` - Create pull requests with descriptions
