# psycoder-tools

A plugin marketplace for Claude Code and Codex.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [review](./review) | 1.1.0 | Repo-specific `REVIEW.md`, optional PR reviewer (Actions with Claude/Codex, Claude Code Review, or local), local review |

## Installation

Claude Code:

```
/plugin marketplace add psycoder-sup/claude-plugin
/plugin install review@psycoder-tools
```

Codex: add this repository as a marketplace:

```sh
codex plugin marketplace add psycoder-sup/claude-plugin
```

Open `/plugins`, select `review` from `psycoder-tools`, install it, and start a new
chat. Invoke `$review-setup` or `$local-review` in Codex; the slash syntax below is
for Claude Code. For local development, run `codex plugin marketplace add .` from
this checkout, then install through the plugin browser.

Both hosts share the skills in `review/skills/`. Codex uses
`review/.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`.
The setup skill writes shared review instructions to `AGENTS.md` in both hosts.
The PR template enforcement hook is Claude Code only; Codex checks headings manually.

Packaging follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

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
