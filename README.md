# psycoder-tools

A plugin marketplace for Claude Code and Codex.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [review](./review) | 1.1.0 | Repo-specific `REVIEW.md`, optional PR reviewer (Actions with Claude/Codex, Claude Code Review, or local), local review |

## Installation

```
/plugin marketplace add psycoder-sup/claude-plugin
/plugin install review@psycoder-tools
```

For Codex:

```sh
codex plugin marketplace add psycoder-sup/claude-plugin
codex plugin add review@psycoder-tools
```

Invoke `$review-setup` or `$local-review` in Codex. See [review](./review/README.md)
for the differences in instruction files and PR-template enforcement between hosts.

## Available Commands

### Code Review (review)
- `/review-setup` - Write a repo-specific `REVIEW.md`, PR template and hook, and pick the PR-time reviewer: GitHub Actions with Claude or Codex, Claude Code Review, or local only
- `/local-review` - Review a diff, branch or PR against `REVIEW.md`; `--comment` posts inline, `--fix` applies

## Archived

`base`, `task` and `nearville-figma` are no longer maintained or listed in the
marketplace. Their last versions are kept under [archive/](./archive).

## Author

**Psycoder SUP** - parksang1993@gmail.com

## License

MIT
