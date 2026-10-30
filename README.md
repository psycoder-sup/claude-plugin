# psycoder-tools

A collection of Claude Code plugins for enhanced development workflows.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [base](./base) | 1.0.19 | Git workflow commands with conventional commits and emoji support |
| [task](./task) | 1.1.11 | Task planning and execution system with code analysis agents |
| [nearville-figma](./nearville-figma) | 1.0.10 | Figma design-to-code implementation for React Native |
| [review](./review) | 1.0.0 | Repo-specific REVIEW.md, optional PR reviewer (Actions with Claude/Codex, Claude Code Review, or local), local review |

## Installation

Add this marketplace to your Claude Code configuration:

```json
{
  "plugins": {
    "marketplaces": [
      {
        "name": "psycoder-tools",
        "source": "path/to/claude-plugin"
      }
    ]
  }
}
```

## Available Commands

### Git Workflows (base)
- `/commit` - Create well-formatted commits with conventional format and emoji
- `/create-pr` - Create pull requests with structured descriptions
- `/review-code` - Review code for bugs, security issues, and quality problems

### Task Management (task)
- `/plan-task` - Plan features with codebase analysis and task file generation
- `/execute-task` - Execute planned tasks in batches with review checkpoints

### Code Review (review)
- `/review-setup` - Write a repo-specific `REVIEW.md`, PR template and hook, and pick the PR-time reviewer: GitHub Actions with Claude or Codex, Claude Code Review, or local only
- `/local-review` - Review a diff, branch or PR against `REVIEW.md`; `--comment` posts inline, `--fix` applies

### Figma Integration (nearville-figma)
- `/implement-design` - Translate Figma designs to React Native code

## Author

**Psycoder SUP** - parksang1993@gmail.com

## License

MIT
