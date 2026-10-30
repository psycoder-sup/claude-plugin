# review

Repo-specific code review for Claude Code and Codex: a written review policy (`REVIEW.md`) that
people, `/local-review` and an optional PR-time reviewer all read. Findings are comments,
never approvals.

## Install

```
/plugin install review --marketplace psycoder-sup/claude-plugin
```

For Codex, run `codex plugin marketplace add psycoder-sup/claude-plugin`, then open
`/plugins` and install `review` from `psycoder-tools`. Start a new chat and invoke
`$review-setup` or `$local-review` with the same arguments shown below.

Both hosts load the same skills and explicitly read `AGENTS.md`. Setup writes review
and PR-template instructions there, and local review records recurring findings under
`## Recurring review findings`. Codex uses `.worktrees/review-setup` and checks PR
template headings manually. Claude Code uses `.claude/worktrees/review-setup` and
the existing hook.
PR-time reviewer choices are independent of the host running setup.

## Skills

### `/review-setup`

Reads the repo and writes what is specific to it, on a branch, then opens a PR:

- `REVIEW.md`: the failure modes that matter here, risk tiers by path, finding tags, nit
  cap, re-review rounds, do-not-report paths
- `.github/CODEOWNERS` for the High tier (with `--owners`)
- `.github/pull_request_template.md`
- Claude Code only: `.claude/hooks/pr-template-check.py`: blocks a `gh pr create` whose body skips the
  template's headings
- lines in `AGENTS.md` (both hosts)
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

`gh` (authenticated) and `python3` for the PR template hook.

Hook tests: `python3 -m unittest discover -s review/skills/review-setup`.
