---
argument-hint: [-a|--auto] [message]
description: Create well-formatted commits with conventional commit format and emoji. Automatically groups related changes into logical commits.
allowed-tools: Task, AskUserQuestion, Bash(git add:*), Bash(git commit:*), Bash(git status:*), Bash(git log:*)
disable-model-invocation: false
---

# Smart Git Commit

**Arguments:** $ARGUMENTS

## Step 1: Analyze Changes

Use the Task tool with `subagent_type: base:git-operations` to analyze the repository changes.

**Prompt for the agent:**
```
Analyze the current git changes and generate commit information.
- Run git status and git diff to understand the changes
- Group related changes logically if needed
- Generate commit message(s) using conventional commit format with emojis
- Return the files to stage and the commit message(s)
```

## Step 2: Create Commit(s)

After receiving the analysis from the agent:

1. **Display the proposal first** - Show the user:
   - Files to be staged
   - The complete commit message(s)

2. If `-a` or `--auto` flag is NOT present in the arguments, **after displaying the proposal**, use AskUserQuestion to ask for confirmation

3. If confirmed (or auto mode), execute the git commands:
   - `git add <files>` to stage the files
   - `git commit -m "<message>"` to create the commit

4. Show the result with `git log -1`

## Commit Message Format

Use HEREDOC for commit messages to preserve formatting:
```bash
git commit -m "$(cat <<'EOF'
<emoji> <type>(<scope>): <description>

[optional body]
EOF
)"
```
