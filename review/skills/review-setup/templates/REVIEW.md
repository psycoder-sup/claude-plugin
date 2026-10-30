# Reviewing <repo name>

Policy for every review of this repo: by a person, by `/local-review`, and by
the PR reviewer, if the repo has one. `CLAUDE.md` covers the stack and layout; this file covers what a bad
change looks like here and how to report it. Owned by the tech lead; tuned when findings
are rated.

## What failure looks like here

<!-- /review-setup fills this from the code: 4-9 numbered failure modes specific to this
     repo, each naming the files or flow it lives in. What makes this repo lose money,
     data, trust or availability? Never generic advice. -->

## Passes

- **Bugs**: the failure modes above first, then logic errors, broken edge cases,
  regressions, unhandled failure paths.
- **Security**: injection, authentication or authorisation gaps, secrets or personal
  data in logs, errors and responses.
- **Compliance**: the change does what its PR says, follows the conventions in
  `CLAUDE.md` and the decisions in `docs/adr/`, and matches any spec or plan it cites
  (an issue, a spec or a design doc, where an unrecorded deviation is a
  finding).

## Risk tiers

The change sets the tier, not the author. A PR takes the tier of its riskiest file.

| Tier | Paths | Human approvals |
|---|---|---|
| High | <!-- paths where a mistake costs money, data, security or production --> | One, plus a careful read of the evidence |
| Medium | Everything else that ships | One |
| Low | Docs, comments, tests only, fixtures, scripts | None once CI and the review are clean |

An agent's approval never counts as a person's. The person who prompted the agent that
wrote a PR is its first reviewer.

## How to report

- **Evidence or it did not happen.** Every finding names a file and line in this diff or
  the code it calls, and a concrete input or sequence that goes wrong. Do not infer a bug
  from a name or a comment. If you could not confirm it by reading the code, drop it.
- **Tag every finding** with one of:
  - **Important**: one of the failure modes above, or a correctness bug a user would hit.
  - **Nit**: style, naming, simplification. At most **3** per review; skip the rest.
  - **Pre-existing**: a real bug in code this PR did not change. Say so, so it is not
    blamed on the author, and do not block on it.
- **Flag the class, not the line.** If the same mistake appears in several places, say
  so once and list them all.
- **Do not repeat yourself.** On a re-review, read your earlier comments first. Do not
  post a finding that is already open or that the author answered.
- **Summary first line** is a count: `2 Important, 1 Nit, 0 Pre-existing.` If there is
  nothing to fix, say `No issues found.` and stop.

## Every finding gets an answer

The author fixes it or resolves the thread with a one-line reason (wrong, intentional,
not worth it). A thread left open blocks the merge.

## Re-review rounds

After the first review, review only the commits pushed since the last review. After three
rounds on one PR, stop posting line comments and ask the author whether the approach
itself is the problem.

## Do not report

<!-- /review-setup lists the generated files, lockfiles, build output and vendored code. -->
- Anything CI already enforces (formatting, lint rules, type errors).

## When a review repeats itself

If the same kind of comment comes up on two PRs, it belongs in a rule, not in a third
comment: add it to `CLAUDE.md` "Things Claude gets wrong", to this file, or to a test.
