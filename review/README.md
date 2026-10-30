# review

Repo-specific code review for Claude Code and Codex: a written review policy (`REVIEW.md`) that
people, `/local-review` and an optional PR-time reviewer all read. Findings are comments,
never approvals.

## Install

Claude Code:

```sh
/plugin marketplace add psycoder-sup/claude-plugin
/plugin install review@psycoder-tools
```

Codex CLI:

```sh
codex plugin marketplace add psycoder-sup/claude-plugin
codex plugin add review@psycoder-tools
```

For local development, pass this repository's absolute path instead of
`psycoder-sup/claude-plugin` when adding the marketplace. Both hosts share the same
`skills/` directory; `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
provide host-specific packaging. Version: **1.1.0**.

In Claude Code use `/review:review-setup` and `/review:local-review` (unqualified
names work when unambiguous). In Codex use `$review-setup` and `$local-review`,
followed by arguments or a natural-language request.

## Skills

### `/review-setup`

Reads the repo and writes what is specific to it, on a branch, then opens a PR:

- `REVIEW.md`: the failure modes that matter here, risk tiers by path, finding tags, nit
  cap, re-review rounds, do-not-report paths
- `.github/CODEOWNERS` for the High tier (with `--owners`)
- `.github/pull_request_template.md`
- Claude Code: `.claude/hooks/pr-template-check.py` blocks a `gh pr create` whose body skips the
  template's headings
- Codex: an explicit PR-body preflight before opening the setup PR; no Claude hook settings
- lines in `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex)
- the PR-time reviewer you pick (optional):

| `--post-review` | PR-time reviewer | Needs |
| --- | --- | --- |
| `actions-claude` | `.github/workflows/claude-review.yml` (`anthropics/claude-code-action`) | `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` secret, Claude GitHub app |
| `actions-codex` | `.github/workflows/codex-review.yml` (`openai/codex-action`) | `OPENAI_API_KEY` secret |
| `code-review` | Claude Code Review (Anthropic's managed reviewer) | Claude Team/Enterprise admin enables it for the repo |
| `local` | none; run `/local-review` yourself | nothing |

Only adds files; idempotent. Never sets secrets, settings or branch protection; the
report says what you must set.

```
/review-setup [path] [--yes] [--owners @a,@b] [--post-review actions-claude|actions-codex|code-review|local]
```

### `/local-review`

Reviews the working tree, a PR, a branch or a path against `REVIEW.md`. Every finding is
verified by reading the code; unverifiable ones are dropped. `--comment` posts inline PR
comments, `--fix` applies the fixes and re-runs the repo's commands.

```
/local-review [<PR number> | <branch> | <path>] [--comment] [--fix]
```

## Requirements

Git, `gh` (authenticated for PR operations), and `python3` for PR-template validation.
The setup skill creates a branch/worktree, commits, pushes, and opens a PR. Local
review without `--comment` needs no GitHub authentication when reviewing a local diff.

Claude Code enforces template headings through its `PreToolUse` hook. Codex runs
an explicit check before creating the setup PR and records template instructions in
`AGENTS.md` for future PRs; it does not install an automatic Codex hook. The validator
can also be run manually from any target repo:

```sh
python3 /absolute/path/to/review/skills/review-setup/templates/pr-template-check.py --check-body /path/to/pr-body.md
```

The explicit check exits 1 for missing headings, an unreadable body, or no single-file
template. The Claude hook retains its existing fail-open behavior for unseen bodies.
Neither mode checks whether the section content is meaningful.

Hook tests: `python3 -m unittest discover -s review/skills/review-setup`.
