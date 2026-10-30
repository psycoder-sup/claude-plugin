---
name: review-setup
description: >
  Set up code review in a repo: read the code to write a repo-specific REVIEW.md
  (failure modes, risk tiers), CODEOWNERS, a PR template and a hook that keeps Claude's
  PRs on it, then pick the PR-time reviewer: a GitHub Actions workflow running Claude or
  Codex, Claude Code Review, or local review only. Opens a PR. Idempotent.
  Usage: /review-setup [path] [--yes] [--owners @a,@b] [--post-review <mode>]
disable-model-invocation: true
argument-hint: "[path] [--yes] [--owners @a,@b] [--post-review actions-claude|actions-codex|code-review|local]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "AskUserQuestion"]
---

# /review-setup

Give a repo a layered code review: a written review policy (`REVIEW.md`) that people,
`/local-review` and any PR-time reviewer all read, and, optionally, an automated reviewer
on every pull request that posts findings and never approves. This skill writes only what
is specific to the target repo.

`path` defaults to the current directory. `--yes` accepts detected values without asking.
`--owners` names the CODEOWNERS for High-tier paths (GitHub handles or `@org/team`).
`--post-review` picks the PR-time reviewer (below). Templates live at
`${CLAUDE_PLUGIN_ROOT}/skills/review-setup/templates/`.

## Post-review modes

The stage after a PR is opened is optional. Exactly one mode per repo:

| Mode | What runs on a PR | Written to the repo | Human must set |
| --- | --- | --- | --- |
| `actions-claude` | `anthropics/claude-code-action` in GitHub Actions; inline comments | `.github/workflows/claude-review.yml` | Secret `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`; Claude GitHub app on the repo |
| `actions-codex` | `openai/codex-action` in GitHub Actions; one summary comment | `.github/workflows/codex-review.yml` | Secret `OPENAI_API_KEY` |
| `code-review` | Claude Code Review, Anthropic's managed reviewer; inline comments | nothing (it reads `REVIEW.md`) | A Claude Team/Enterprise admin enables it for the repo; Claude GitHub app installed |
| `local` | nothing; reviews run on the author's machine with `/local-review` | nothing | nothing |

Default with `--yes` and no `--post-review`: `local`, since it needs no secret or admin.

## Rules

- **Only add.** Write a file only when it is absent, except an unedited `REVIEW.md`
  template (below), which is filled in place, and the lines added to `CLAUDE.md`. Never
  rewrite the repo's own files; suggest changes in the report instead. A second run on an
  unchanged repo makes no change.
- **Never change repository or organisation settings**: branch protection, rulesets,
  secrets, app installs, Claude Code Review enablement. Never ask for a token or key in
  the conversation. Say what the human must set and how, in the report.
- **One reviewer.** Write at most one review workflow, and only for an `actions-*` mode.
  Two PR-time reviewers review every PR twice; an existing one is reported, not removed.
- **Specific or dropped.** Every failure mode and High-tier path comes from code you read
  in this repo. One that would fit any repo is dropped.
- **Work on a branch.** Make the changes in a worktree at `.claude/worktrees/review-setup`
  on branch `review-setup` from the default branch, commit, push, and open a PR. Never
  commit to the default branch. Ensure `.gitignore` has a `.claude/worktrees/` line.

## Process

### 1. Detect

Read the repo without changing it:

- **Review state.** Is `REVIEW.md` absent, an unedited template (it still has
  `<!-- /review-setup fills` comments), or the repo's own? Also: `CODEOWNERS`
  (`.github/`, root, `docs/`), a PR template, `.claude/settings.json` and whether it
  already runs `pr-template-check.py`.
- **Existing PR reviewer.** Any workflow under `.github/workflows/` that runs on pull
  requests and uses `anthropics/claude-code-action`, `openai/codex-action`, or another
  AI review action; note its file and which mode it matches.
- **Where a mistake costs the most.** Read `CLAUDE.md`, `AGENTS.md`, the README and the
  entry points, and follow the flows that move money, grant access, write or delete data,
  call external services with side effects, sign or verify requests, run migrations, or
  deploy. Note each as a candidate failure mode with the files it lives in, and the paths
  that hold them as candidate High-tier paths. Attack surface specific to this repo
  (payments, auth, webhooks, signed requests, data export) is a candidate failure mode
  too, since `REVIEW.md` is the only brief the reviewer gets. CI workflows, infra and
  deploy config are always High.
- **Do-not-report paths**: generated files, lockfiles, build output, vendored code.
- **Owners**: from `--owners`, else none.

### 2. Confirm

Unless `--yes`, one `AskUserQuestion` round with everything at once: the candidate failure
modes (4-9), the High-tier paths, the do-not-report paths, the owners if none were given,
and the post-review mode if `--post-review` was not given (the four modes above, with
`local` first as the recommendation unless an existing reviewer was found, in which case
its mode comes first). With `--yes`, use the detected values, write no CODEOWNERS without
owners, and say so in the report.

### 3. Write

In the worktree:

- **`REVIEW.md`.** Absent or unedited template → write it from the template: the repo name
  in the title; "What failure looks like here" as the confirmed failure modes, numbered,
  each one sentence on the failure and one on where it lives; the High-tier row with the
  confirmed paths; the "Do not report" list. Remove the template's `<!--` instruction
  comments. The repo's own `REVIEW.md` → leave it, and list in the report any
  template section it lacks (failure modes, risk tiers, tags, re-review rounds).
- **`.github/CODEOWNERS`.** Only with owners and no existing CODEOWNERS: one line per
  High-tier path, owned by those handles. Check each person has write access
  (`gh api repos/<owner>/<repo>/collaborators/<login>/permission`) and each team is
  granted the repo; leave out and report any that fail.
- **`.github/pull_request_template.md`** from the template, if no PR template exists.
- **PR template hook.** `gh pr create --body` never applies the template, so Claude
  writes its own format unless stopped. Copy `pr-template-check.py` to
  `.claude/hooks/pr-template-check.py` if absent; it denies a `gh pr create` whose body
  lacks any `## ` heading of the repo's single-file PR template (`pull_request_template.md`
  in `.github/`, the root or `docs/`, any case). If `.claude/settings.json` is absent,
  write it from `claude-settings.json`. If it exists and does not already run the hook,
  leave it and put the `PreToolUse` entry from `claude-settings.json` in the report for
  the human to merge. Skip the hook when the repo's templates live only in a
  `PULL_REQUEST_TEMPLATE/` directory: there is no one set of headings, so it would check
  nothing. Say so in the report.
- **Review workflow**, by mode, only when no PR reviewer was found in step 1:
  - `actions-claude` → copy `workflows/claude-review.yml` to
    `.github/workflows/claude-review.yml`.
  - `actions-codex` → copy `workflows/codex-review.yml` to
    `.github/workflows/codex-review.yml`.
  - `code-review`, `local` → no workflow.
  If a reviewer was found and the chosen mode differs, write nothing and say in the report
  which file to delete to switch.
- **`CLAUDE.md`.** If it exists, add under `## Commands` (or at the end) each of these
  lines it lacks. If it does not mention `REVIEW.md`: `Review: REVIEW.md says what a bad
  change looks like here and how findings are reported. Run /local-review before asking
  for a human review.` followed, for any mode but `local`, by ` Every PR also gets
  <Claude via GitHub Actions | Codex via GitHub Actions | Claude Code Review>.` If it does
  not mention the PR template: `PRs: before gh pr create, read <template path> and fill
  every section in its order, keeping each heading as written; do not use a Summary/Test
  plan body.` with the repo's actual template path (for a `PULL_REQUEST_TEMPLATE/`
  directory: `read the matching template in <dir>`).

### 4. Pull request

Stage every file written. Run `git check-ignore -q` on each one under `.claude/`; a repo
that ignores `.claude/` would otherwise drop the hook from the commit without a word, so
stage those with `git add -f` and say so in the report. Commit with a message listing the
files, push, and open a PR whose body follows the PR template: risk tier High (it touches
`.github/` and `.claude/`), the post-review mode chosen, what each file is for, and
"Revert the commit" as the way back. Once the PR-time reviewer is live, this PR can be its
first review.

### 5. Report

List the files created, the ones left alone and why, the post-review mode, the PR link,
and what the human must do:

- Read `REVIEW.md`'s failure modes and tiers before merging; they are the reviewer's whole
  brief.
- If `.claude/settings.json` was left alone, merge the hook entry shown in the report;
  until then nothing runs `pr-template-check.py`.
- By mode:
  - `actions-claude`: add the `ANTHROPIC_API_KEY` repository secret (or
    `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`, and switch the input name as the
    workflow's header says), and install the Claude GitHub app (`/install-github-app` in
    Claude Code does both). Runs bill to that key or subscription.
  - `actions-codex`: add the `OPENAI_API_KEY` repository secret. Runs bill to that key.
  - `code-review`: a Claude Team or Enterprise admin enables Claude Code Review and
    selects this repo; the Claude GitHub app must be installed on it. No Actions secret is
    needed.
  - `local`: nothing to enable. Reviews happen only when someone runs `/local-review`
    (or `/local-review <PR> --comment` to post them on the PR).
- Any existing reviewer found in step 1 that duplicates or conflicts with the chosen mode:
  suggest deleting it.
- Branch protection on the default branch (required CI, code owner review, resolved
  conversations, stale approvals dismissed) is theirs to set.
