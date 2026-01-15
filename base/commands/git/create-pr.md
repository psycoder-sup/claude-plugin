---
argument-hint: [-a|--auto] [message]
description: Create well-formatted pull request to remote repository
allowed-tools: Task, AskUserQuestion, Bash(git push:*), Bash(git status:*), Bash(git log:*), Bash(git branch:*), Bash(gh pr create:*)
disable-model-invocation: false
---

# Smart Git Pull Request Creation

**Arguments:** $ARGUMENTS

## Step 1: Analyze Branch Changes

Use the Task tool with `subagent_type: base:git-operations` to analyze the branch and generate PR information.

**Prompt for the agent:**
```
Analyze the branch changes and generate pull request information.
- Check current branch and commits since main/master
- Run git diff to understand all changes
- Read changed files if needed for full context
- Generate a PR title and comprehensive description
- Return the PR title, description, and any files that need to be pushed
- Do NOT create the PR yet - only return the proposed information
```

## Step 2: Create Pull Request

After receiving the analysis from the agent:

1. **Display the proposal first** - Show the user:
   - PR title
   - PR description (summary, changes, test plan)
   - Branch to be pushed (if not already pushed)

2. If `-a` or `--auto` flag is NOT present in the arguments, **after displaying the proposal**, use AskUserQuestion to ask for confirmation

3. If confirmed (or auto mode), execute the commands:
   - `git push -u origin <branch>` if needed
   - `gh pr create --title "<title>" --body "<description>"`

4. Show the PR URL to the user

## PR Description Format

Use HEREDOC for PR body to preserve formatting:
```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<brief summary>

## Changes
<bullet points of changes>

## Test Plan
<how to test>
EOF
)"
```
