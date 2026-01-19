# base

Git workflow commands for Claude Code with conventional commits and emoji support.

## Commands

### `/commit`

Create well-formatted commits with:
- Conventional commit format (`feat`, `fix`, `docs`, `refactor`, etc.)
- Emoji prefixes for visual clarity
- Smart diff analysis to group related changes logically
- Confirmation prompt before committing

**Usage:**
```
/commit                    # Analyze changes and ask for confirmation
/commit -a                 # Auto mode: commit without confirmation
/commit --auto             # Auto mode: commit without confirmation
/commit [message]          # Include a message hint for the commit
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

### `/review-code`

Review code for bugs, security issues, and quality problems:
- Confidence-based filtering (80+ threshold)
- Reports grouped by severity
- Fix suggestions for each issue

**Usage:**
```
/review-code                  # Review unstaged changes
/review-code <files|scope>    # Review specific files or scope
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

### code-reviewer
Reviews code for bugs, security vulnerabilities, and quality issues:
- Uses confidence-based filtering (80+ threshold)
- Reports only high-priority issues
- Provides fix suggestions for each issue

## Version

1.0.14
