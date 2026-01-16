---
name: Git Worktree Workspace
description: This skill should be used when the user asks to "create a worktree", "set up a worktree workspace", "work on multiple branches", "manage worktrees", "list worktrees", "remove worktree", or mentions needing to work on multiple branches simultaneously with tmux integration.
---

# Git Worktree Workspace Manager

This skill manages git worktrees with tmux window integration, enabling work on multiple branches simultaneously without stashing changes.

## Overview

Git worktrees allow checking out multiple branches of the same repository into separate directories. This skill creates organized workspaces at `~/.worktree/{project-name}/{branch-name}` and opens tmux windows for each worktree when running inside tmux.

## Helper Script

Use the helper script at `scripts/worktree.sh` for all operations:

```bash
# Create worktree with tmux window
${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh create <branch-name>

# List existing worktrees and tmux windows
${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh list

# Remove worktree and kill associated tmux window
${CLAUDE_PLUGIN_ROOT}/scripts/worktree.sh remove <name>
```

## Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| Create | `create <branch>` | Creates worktree, opens tmux window with dev layout |
| List | `list` | Shows all worktrees and tmux windows |
| Remove | `remove <name>` | Removes worktree and kills tmux window |

## Tmux Layout

When creating a worktree in tmux, the script sets up a dev layout:

```
┌─────────────────────────┐
│      Terminal (top)     │  ← Focus here for work
├─────────────────────────┤
│      Claude (bottom)    │  ← Claude running
└─────────────────────────┘
```

## User Interaction

When the user requests worktree operations:

- **No arguments**: Ask what operation to perform (create/list/remove)
- **Branch name only**: Create worktree for that branch
- **"list" or "show"**: List existing worktrees
- **"remove" or "delete"**: Show worktrees and ask which to remove

## Notes

- Worktrees share the same `.git` directory, so commits made in any worktree are visible to all
- Each worktree has its own working directory and index
- Use `Ctrl+b w` in tmux to view and switch between windows
- If not in tmux, the script still creates the worktree and shows the path
