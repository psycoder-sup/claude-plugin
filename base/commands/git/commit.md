---
argument-hint: [-a|--auto] [message]
description: Create well-formatted commits with conventional commit format and emoji. Automatically groups related changes into logical commits.
model: haiku
disable-model-invocation: true
---

# Smart Git Commit

Use the Task tool with `subagent_type: base:git-operations` to create well-formatted commits.

**Arguments:** $ARGUMENTS

**Prompt for the agent:**
Analyze the repository changes and create commit(s) with conventional commit format.
- If `-a` or `--auto` flag is present, proceed without confirmation
- If files are already staged, only commit those files
- Group related changes into logical commits
- Use conventional commit format with emojis
- Show the result after committing
