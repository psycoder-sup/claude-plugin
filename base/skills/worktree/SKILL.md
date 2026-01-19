---
name: Git Worktree Workspace
description: This skill should be used when the user asks to "create a worktree", "set up a worktree workspace", "work on multiple branches", "manage worktrees", "list worktrees", "remove worktree", or mentions needing to work on multiple branches simultaneously with Ghostty integration.
model: haiku
---

# Git Worktree Workspace Manager

This skill manages git worktrees with Ghostty terminal integration, enabling work on multiple branches simultaneously without stashing changes.

## Overview

Git worktrees allow checking out multiple branches of the same repository into separate directories. This skill creates organized workspaces at `~/.worktree/{project-name}/{branch-name}` and opens new Ghostty tabs for each worktree when Ghostty is running.

## Helper Script

Use the helper script at `scripts/worktree.sh` for all operations:

```bash
# Create worktree with Ghostty tab
${CLAUDE_PLUGIN_ROOT}/skills/worktree/scripts/worktree.sh create <branch-name>

# List existing worktrees
${CLAUDE_PLUGIN_ROOT}/skills/worktree/scripts/worktree.sh list

# Remove worktree
${CLAUDE_PLUGIN_ROOT}/skills/worktree/scripts/worktree.sh remove <name>
```

## Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| Create | `create <branch>` | Creates worktree, opens Ghostty tab with Claude |
| List | `list` | Shows all git worktrees |
| Remove | `remove <name>` | Removes worktree (close Ghostty tab manually) |

## Ghostty Integration

When creating a worktree, the script:
1. Creates the git worktree at `~/.worktree/{project}/{branch}`
2. Opens a new Ghostty tab (if Ghostty is running)
3. Changes to the worktree directory
4. Automatically starts `claude`

## User Interaction

When the user requests worktree operations:

- **No arguments**: Ask what operation to perform (create/list/remove)
- **Branch name only**: Create worktree for that branch
- **"list" or "show"**: List existing worktrees
- **"remove" or "delete"**: Show worktrees and ask which to remove

## Notes

- Worktrees share the same `.git` directory, so commits made in any worktree are visible to all
- Each worktree has its own working directory and index
- Use `Cmd+Shift+[` / `Cmd+Shift+]` to switch between Ghostty tabs
- If Ghostty is not running, the script still creates the worktree and shows the path
- Ghostty tabs must be closed manually when removing worktrees
