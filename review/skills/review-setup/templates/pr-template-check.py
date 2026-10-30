#!/usr/bin/env python3
"""PreToolUse hook (Bash): deny `gh pr create` when the body skips a `## ` heading
of this repo's PR template. Written by /review-setup to .claude/hooks/.

`gh pr create --body` never applies the template, so a body Claude writes itself
falls back to its own format. This makes it read the template instead.

Only a `gh pr create` in command position is checked, with its own arguments; a
command that merely mentions the phrase passes. Fails open whenever the body cannot
be seen: read from stdin (`-F -`), built by command substitution, or an unreadable
file. Inert without a single-file PR template with `## ` headings (a
PULL_REQUEST_TEMPLATE/ directory has no one set of headings), and with `--web`.

Contract: stdin is JSON with tool_input.command and cwd. Deny = exit 2 with the
reason on stderr, plus the permissionDecision JSON on stdout.
Tests: test_pr_template_check.py beside review-setup in the psycoder-tools review plugin.
"""
import json
import os
import re
import shlex
import subprocess
import sys

TEMPLATES = [".github/pull_request_template.md", "pull_request_template.md",
             "docs/pull_request_template.md"]
SEPARATORS = set(";&|()\n")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
MARKER = re.compile(r"__PRT_HEREDOC_\d+__")


def repo_root(cwd):
    """The git top level of cwd, else CLAUDE_PROJECT_DIR, else cwd."""
    try:
        out = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.environ.get("CLAUDE_PROJECT_DIR") or cwd


def find_template(root):
    for rel in TEMPLATES:
        d, name = os.path.split(os.path.join(root, rel))
        try:
            hit = next((f for f in os.listdir(d) if f.lower() == name), None)
        except OSError:
            continue
        if hit and os.path.isfile(os.path.join(d, hit)):
            return os.path.join(d, hit)
    return None


def headings(path):
    with open(path, encoding="utf-8") as fh:
        return [ln.strip() for ln in fh if re.match(r"^##\s+\S", ln)]


def lift_heredocs(command):
    """Swap each heredoc for a marker word and return (command, {marker: body}).

    A heredoc's free text (quotes inside `$(cat <<'EOF' ... EOF)`, an apostrophe)
    is literal to bash but breaks shlex, which does not know heredocs.
    """
    out, bodies, current, delim = [], {}, None, None
    for ln in command.split("\n"):
        if delim is not None:
            if ln.strip() == delim:
                delim = None
            else:
                bodies[current].append(ln)
            continue
        m = HEREDOC.search(ln)
        if m:
            current, delim = f"__PRT_HEREDOC_{len(bodies)}__", m.group(2)
            bodies[current] = []
            ln = ln[:m.start()] + "<<" + current + ln[m.end():]
        out.append(ln)
    return "\n".join(out), {k: "\n".join(v) for k, v in bodies.items()}


def invocations(command):
    """Argument lists of each `gh pr create` in command position."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    segment, found = [], []
    for tok in list(lex) + [";"]:
        if tok and set(tok) <= SEPARATORS:
            words = segment
            while words and ASSIGNMENT.match(words[0]):
                words = words[1:]
            if words[:3] == ["gh", "pr", "create"]:
                found.append(words[3:])
            segment = []
        else:
            segment.append(tok)
    return found


def body_of(args):
    """("web", None) | ("text", body) | ("file", path) | ("none", None)."""
    kind, value = "none", None
    i = 0
    while i < len(args):
        a = args[i]
        nxt = args[i + 1] if i + 1 < len(args) else ""
        if a in ("--web", "-w"):
            return "web", None
        if a in ("--body", "-b"):
            kind, value, i = "text", nxt, i + 1
        elif a.startswith("--body="):
            kind, value = "text", a.split("=", 1)[1]
        elif a in ("--body-file", "-F"):
            kind, value, i = "file", nxt, i + 1
        elif a.startswith("--body-file="):
            kind, value = "file", a.split("=", 1)[1]
        i += 1
    return kind, value


def unseen(text):
    """True when the shell, not the command text, decides the body."""
    return "$(" in text or "`" in text or re.search(r"\$\{?[A-Za-z_]", text) is not None


def deny(reason):
    out = {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                  "permissionDecision": "deny",
                                  "permissionDecisionReason": reason}}
    return 2, out, reason


def decide(payload):
    """Return (exit_code, stdout_json_or_None, reason_or_None)."""
    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    command = tool_input.get("command") or ""
    if "create" not in command:
        return 0, None, None
    lifted, bodies = lift_heredocs(command)
    try:
        calls = invocations(lifted)
    except ValueError:
        return 0, None, None  # unbalanced quotes: the shell will reject it anyway
    if not calls:
        return 0, None, None
    cwd = payload.get("cwd") or os.getcwd()
    root = repo_root(cwd)
    template = find_template(root)
    if not template:
        return 0, None, None
    try:
        wanted = headings(template)
    except OSError:
        return 0, None, None  # an unreadable template must never block work
    if not wanted:
        return 0, None, None
    rel = os.path.relpath(template, root)
    for args in calls:
        kind, value = body_of(args)
        if kind == "web":
            continue
        if kind == "none":
            return deny(f"pr-template-check: gh pr create has no --body or --body-file, "
                        f"so the body would not follow {rel}. Read it and pass a body "
                        f"that fills every section, keeping each heading as written.")
        if kind == "file":
            if value in ("", "-"):
                continue  # stdin: the body is not visible here
            try:
                with open(os.path.join(cwd, value), encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                continue  # gh will report the missing file itself
        else:
            text = value or ""
            if MARKER.search(text):  # a heredoc's lines are the body
                text = MARKER.sub(lambda m: bodies[m.group(0)], text)
            elif unseen(text):
                continue
        missing = [h for h in wanted if h not in text]
        if missing:
            return deny(f"pr-template-check: the PR body is missing {', '.join(missing)}. "
                        f"Read {rel} and fill every section in its order, keeping each "
                        f"heading as written, then run gh pr create again.")
    return 0, None, None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # not our shape; never block on a parse error
    try:
        code, out, reason = decide(payload)
    except Exception as e:  # a bug here must never block work
        print(f"pr-template-check: {e}", file=sys.stderr)
        return 0
    if out is not None:
        print(json.dumps(out))
    if reason:
        print(reason, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
