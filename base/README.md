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

## Hooks

- `python_black_ruff.py` - Pre-commit hook for Python linting/formatting with Black and Ruff

## Version

1.0.1
