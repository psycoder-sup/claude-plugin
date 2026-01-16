# base

Git workflow commands for Claude Code with conventional commits and emoji support.

## Commands

### `/commit`

Create well-formatted commits with:
- Conventional commit format (`feat`, `fix`, `docs`, `refactor`, etc.)
- Emoji prefixes for visual clarity
- Automatic pre-commit checks (`pnpm lint`, `pnpm build`, `pnpm generate:docs`)
- Smart diff analysis to suggest splitting large changes
- Co-author attribution

**Usage:**
```
/commit
/commit --no-verify  # Skip pre-commit checks
```

**Commit Types:**
| Emoji | Type | Description |
|-------|------|-------------|
| ✨ | feat | New feature |
| 🐛 | fix | Bug fix |
| 📝 | docs | Documentation |
| ♻️ | refactor | Code refactoring |
| 🔧 | chore | Tooling/config |
| 🔖 | chore | Release/version tags |
| ⚡️ | perf | Performance |
| ✅ | test | Tests |

### `/create-pr`

Create pull requests with:
- Structured PR description
- Summary of changes from all commits
- Test plan checklist

**Usage:**
```
/create-pr
```

## Skills

### git-workflow
Provides guidance on git workflows, conventional commits, and safe git operations. Triggered when discussing commits, PRs, or branching strategies.

### worktree (Git Worktree Workspace)
Manages git worktrees with tmux window integration for working on multiple branches simultaneously.

## Hooks

### PreToolUse: Bash
Validates git commands before execution:
- Blocks force push to main/master
- Blocks hard reset on main/master
- Blocks deletion of main/master branch

## Agents

### git-operations
Handles all git workflow operations including:
- Creating commits with conventional format
- Creating pull requests with descriptions
- Safe merge/rebase operations
- Conflict resolution guidance

## Version

1.0.11
