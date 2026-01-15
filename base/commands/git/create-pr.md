---
argument-hint: [message]
description: Create well-formatted pull request to remote repository
model: haiku
disable-model-invocation: true
---

# Smart Git Pull Request Creation

Use the Task tool with `subagent_type: base:git-operations` to create a well-formatted pull request.

**Arguments:** $ARGUMENTS

**Prompt for the agent:**
Analyze the branch changes and create a comprehensive pull request.
- Check current branch and commits since main
- Read changed files to understand the full context
- Push the branch if not already pushed
- Create PR with clear title and comprehensive description
- Include what changed, why, and how to test
