---
name: local-review
description: >
  Review a diff, PR, branch, or path locally against the repo's REVIEW.md: run its passes,
  report only findings verified by reading the surrounding code, rank most-severe first,
  cap nits at the file's number, skip what it says to skip. --comment posts inline PR
  comments; --fix applies findings and re-runs the repo's commands. A finding category
  seen twice becomes a line in the host instruction file under "Review lessons".
  Use before asking a human to review.
argument-hint: "[<PR number> | <branch> | <path>] [--comment] [--fix]"
allowed-tools: ["Read", "Edit", "MultiEdit", "Bash", "Glob", "Grep", "Agent", "AskUserQuestion"]
---

# /local-review

Apply the repo's written review policy to a change, on this machine. `REVIEW.md` at the
repo root is the policy: its failure modes, passes, definition of Important, nit cap and
do-not-report list. This skill is the reviewer that reads it. People and any PR-time
reviewer read the same file; that is the point.

## Host adaptation

Announce the review target before starting. Use available file and shell tools; the
Claude tool names in frontmatter do not require Codex tools with those names.
Invoke as `$local-review` in Codex or `/review:local-review` in Claude Code (the
unqualified name also works when unambiguous). Natural-language arguments are accepted.
Read both `AGENTS.md` and `CLAUDE.md` when present. Write recurring review lessons to
`AGENTS.md` in Codex or `CLAUDE.md` in Claude Code, under `## Review lessons`.
Use the host's native instruction file first when finding verification commands,
then the other instruction file, then the repo's documented test/lint/type-check commands.

## Target

| Argument | Diff reviewed |
| --- | --- |
| none | working tree vs `HEAD` (staged + unstaged); if clean, `HEAD` vs the default branch |
| a number | that PR: `gh pr diff <n>`; comments via `gh pr view <n> --comments` |
| a branch name | `<default>...<branch>` (`git merge-base` three-dot diff) |
| a path | current diff limited to that path, or the whole file if it has no diff |

Default branch: `git symbolic-ref refs/remotes/origin/HEAD` or, without a remote, `main`
then `master`, whichever exists. State the target and the diff size in the report.

## Process

1. **Read `REVIEW.md`.** No file → say so, use three passes (bugs, security, compliance
   with what the PR or commit says it does and with `CLAUDE.md`/`AGENTS.md`), a nit cap
   of three, and recommend `/review-setup`. If the PR body, commit messages or branch
   name cite an issue, spec or design doc you can read, the compliance pass checks the
   diff against it and treats an unrecorded deviation as a finding.
2. **Run each pass** over the diff, one at a time, reading the diff hunks and enough of
   the surrounding code to know what they do. The repo's failure modes come first.
   Candidate findings go on a list with the pass, file, line, and a one-sentence claim.
3. **Verify every candidate.** For each: open the file, follow the call, check the test,
   confirm the failure scenario is concrete (inputs → wrong output). A candidate you
   cannot verify is **dropped, not hedged**. Fewer, certain findings beat many maybes.
4. **Classify** with `REVIEW.md`'s tags (Important, Nit, Pre-existing, or whatever it
   defines). Drop anything on the do-not-report list or that CI already enforces.
5. **Rank** Important findings most-severe first. Keep at most the nit cap's worth of
   nits; summarise the rest as a count.
6. **Recurrence.** Give each finding a short category slug (`unquoted-csv-field`,
   `missing-null-check`, `test-asserts-internals`). If the same category was reported in
   an earlier review of this repo that you can see (earlier in this session, or in the
   PR's existing review comments), append one line to the host instruction file under
   `## Review lessons` stating the rule in imperative form, and say so in the report.
   Create the file or heading if missing; never duplicate an existing line.
7. **Output** in this order: the target and diff size; the count line `REVIEW.md` asks
   for (e.g. `2 Important, 1 Nit, 0 Pre-existing.`); Important findings as a numbered
   list, each with `file:line`, the claim, the concrete failure scenario, and the fix;
   then nits (capped) as one line each; then pre-existing findings; then the omitted-nit
   count; then a final line exactly of the form
   `LOCAL-REVIEW: important=<n> nits=<shown>/<total> categories=<a,b,c>`.

## Modes

- **`--comment`** (PR targets only): post each finding as an inline review comment on the
  PR through `gh api repos/{owner}/{repo}/pulls/<n>/comments` (path, line, commit_id of
  the PR head, body = tag + claim + scenario + fix), then one summary comment whose first
  line is the count line. On a re-review, read the existing comments first and skip any
  finding already open or answered. Never approve or request changes: findings inform the
  human reviewer, they do not gate.
- **`--fix`**: apply each Important finding's fix to the working tree (nits only when
  trivial and safe), then run the verification commands selected above (or the
  repo's test, lint and type-check commands if there is no such section) and paste the
  tail of the output. Red → revert the fix that broke it and report. Never edit a test to
  make a finding go away. Do not commit; the caller does.

## Rules

- **Verified or dropped.** No "might", "consider", or "possibly" in an Important finding.
- **The policy is the file.** If `REVIEW.md` says skip it, skip it, even if you disagree;
  suggest a policy change in one line at the end instead.
- **Findings do not approve.** Branch protection and a human do.
- **Self-contained.** This skill delegates to no other reviewer; its behaviour is fully
  described here.
