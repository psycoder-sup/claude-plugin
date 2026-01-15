---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*)
argument-hint: [-a|--auto] [message]
description: Create well-formatted commits with conventional commit format and emoji. Automatically groups related changes into logical commits.
model: haiku
disable-model-invocation: true
---

# Smart Git Commit

Create well-formatted commit(s): $ARGUMENTS

## Phase 1: Analyze Repository State

Gather current state information:

- Git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits (for style reference): !`git log --oneline -5`

## Phase 2: Determine Commit Strategy

Analyze the changes and decide on the commit strategy.

### Parse Arguments

Check if `$ARGUMENTS` contains `-a` or `--auto` flag:
- If `-a` or `--auto` is present: **Auto mode** - proceed without confirmation
- Otherwise: **Confirmation mode** - ask user before creating multiple commits

Extract any commit message hint from arguments (text after the flag, if any).

### Decision Tree

1. **If files are already staged**: Respect user's staging - only analyze and commit staged files
2. **If 4 or fewer files changed AND all changes are related**: Single commit
3. **If 5+ files changed OR changes span multiple unrelated concerns**: Analyze for grouping

### Grouping Analysis

When grouping is needed, analyze changes by:

1. **Shared purpose**: Files that together implement one feature or fix
2. **Change type**:
   - Documentation (*.md, docs/*)
   - Tests (*test*, *spec*, __tests__/*)
   - Configuration (*.json, *.yaml, *.config.*)
   - Source code (everything else)
3. **Module boundaries**: Changes to separate packages/directories
4. **Commit type alignment**: All files in a group should fit one conventional commit type

## Phase 3: Execute Commits

### Single Commit Flow

If changes should be a single commit:

1. Stage all changes if none staged: `git add -A`
2. Review the diff to understand changes: `git diff --cached`
3. Create commit with appropriate emoji + conventional commit format
4. Show result: `git log --oneline -1`

### Multiple Commits Flow

If changes should be split into groups:

**In Confirmation Mode (default):**

1. Present proposed groupings to user:
   ```
   I've analyzed the changes and recommend splitting into N commits:

   **Commit 1/N**: `emoji type: description`
   - file1.ts
   - file2.ts

   **Commit 2/N**: `emoji type: description`
   - file3.md

   ...

   Options:
   - "yes" or "proceed" - create all commits as proposed
   - "adjust" - modify the groupings
   - "single" - combine into one commit
   - "abort" - cancel commit operation
   ```

2. Wait for user confirmation before proceeding

3. For each confirmed group:
   a. Reset staging: `git reset HEAD` (if needed)
   b. Stage only group files: `git add <file1> <file2> ...`
   c. Create commit with appropriate message
   d. Report: "Created commit N/M: message"

4. After all commits, show summary: `git log --oneline -n <count>`

**In Auto Mode (`-a` or `--auto`):**

1. Analyze and group changes automatically
2. For each group:
   a. Stage group files: `git add <file1> <file2> ...`
   b. Create commit with appropriate message
   c. Report: "Created commit N/M: message"
3. Show summary: `git log --oneline -n <count>`

## Phase 4: Verification

After committing, show:
- `git log --oneline -n <number_of_commits_created>` to confirm commits
- `git status` to confirm working tree state

## Conventional Commit Format

Use the format `emoji type(scope): description` where type is one of:

| Emoji | Type | Description |
|-------|------|-------------|
| ✨ | feat | New feature |
| 🐛 | fix | Bug fix |
| 📝 | docs | Documentation |
| 💄 | style | Formatting/style |
| ♻️ | refactor | Code refactoring |
| ⚡️ | perf | Performance improvements |
| ✅ | test | Tests |
| 🔧 | chore | Tooling, configuration |
| 🚀 | ci | CI/CD improvements |

### Extended Emoji Reference

- 🚨 `fix`: Fix compiler/linter warnings
- 🔒️ `fix`: Fix security issues
- 🚚 `refactor`: Move or rename resources
- 🏗️ `refactor`: Make architectural changes
- ➕ `chore`: Add a dependency
- ➖ `chore`: Remove a dependency
- 🧑‍💻 `chore`: Improve developer experience
- 🏷️ `feat`: Add or update types
- 👔 `feat`: Add or update business logic
- 🚸 `feat`: Improve user experience / usability
- 🩹 `fix`: Simple fix for a non-critical issue
- 🔥 `fix`: Remove code or files
- 🎨 `style`: Improve structure/format of the code
- 🚑️ `fix`: Critical hotfix
- 💚 `fix`: Fix CI build
- ✏️ `fix`: Fix typos
- 💥 `feat`: Introduce breaking changes
- 💡 `docs`: Add or update comments in source code
- 🗃️ `db`: Database related changes
- ⚰️ `refactor`: Remove dead code
- 🦺 `feat`: Add or update validation

## Grouping Examples

### Example 1: Feature + Docs + Tests

Changed files:
- src/auth/login.ts
- src/auth/session.ts
- docs/auth.md
- tests/auth.test.ts

**Recommended grouping:**
1. `✨ feat(auth): add session management` → login.ts, session.ts
2. `📝 docs(auth): update authentication documentation` → auth.md
3. `✅ test(auth): add auth unit tests` → auth.test.ts

### Example 2: Related Feature Changes

Changed files:
- src/components/Button.tsx
- src/components/Button.css
- src/components/index.ts

**Recommended:** Single commit - all changes are related:
`✨ feat(components): add Button component with styling`

### Example 3: Multiple Unrelated Fixes

Changed files:
- src/api/users.ts (bug fix)
- package.json (dependency update)
- .gitignore (config change)

**Recommended grouping:**
1. `🐛 fix(api): resolve user API null check` → users.ts
2. `➕ chore(deps): update dependencies` → package.json
3. `🙈 chore: update gitignore patterns` → .gitignore

## Important Notes

- **Staged files take priority**: If you've staged specific files, only those will be committed
- **Message hint**: If you provide a message like `/commit fix auth bug`, it helps identify the primary change but splitting may still be suggested
- **Confirmation by default**: For multiple commits, you'll be asked to confirm unless `-a`/`--auto` flag is used
- **Atomic commits**: Each commit will be atomic and self-contained
- **Abort anytime**: Reply "abort" to stop the commit process at any point
- **Present tense, imperative mood**: Write commit messages as commands (e.g., "add feature" not "added feature")
- **Concise first line**: Keep the first line under 72 characters
