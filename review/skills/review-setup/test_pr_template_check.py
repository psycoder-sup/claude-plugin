"""Fixture cases for templates/pr-template-check.py, run through its stdin/exit contract.

    python3 -m unittest discover -s review/skills/review-setup
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "templates", "pr-template-check.py")
TEMPLATE = os.path.join(HERE, "templates", "pull_request_template.md")

with open(TEMPLATE, encoding="utf-8") as fh:
    GOOD = fh.read()
BAD = "## Summary\n- did a thing\n\n## Test plan\n- ran it\n"


def heredoc_body(text):
    return f"--body \"$(cat <<'EOF'\n{text}\nEOF\n)\""


class Repo:
    """A git repo in a temp dir, with the bundled template unless told otherwise."""

    def __init__(self, template=".github/pull_request_template.md", content=GOOD):
        self.root = tempfile.mkdtemp(prefix="prt-")
        subprocess.run(["git", "init", "-q", self.root], check=True)
        if template:
            self.write(template, content)
        self.write("good.md", GOOD)
        self.write("bad.md", BAD)

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def run(self, command, cwd=None, key="tool_input", raw=None):
        payload = raw if raw is not None else json.dumps(
            {"hook_event_name": "PreToolUse", "tool_name": "Bash",
             "cwd": cwd or self.root, key: {"command": command}})
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        p = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True,
                           text=True, cwd=cwd or self.root, env=env)
        return p.returncode, p.stdout, p.stderr

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


class HookTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.close()

    def allows(self, command, **kw):
        code, out, err = self.repo.run(command, **kw)
        self.assertEqual(code, 0, f"expected allow for {command!r}: {err}")
        self.assertEqual(out.strip(), "")

    def denies(self, command, **kw):
        code, out, err = self.repo.run(command, **kw)
        self.assertEqual(code, 2, f"expected deny for {command!r}")
        decision = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "deny")
        self.assertIn("pr-template-check", err)
        return err


class Bodies(HookTest):
    def test_heredoc_with_every_heading(self):
        self.allows("gh pr create --title t " + heredoc_body(GOOD))

    def test_default_format_denied_and_names_missing_headings(self):
        err = self.denies("gh pr create --title t " + heredoc_body(BAD))
        self.assertIn("## What and why", err)
        self.assertIn(".github/pull_request_template.md", err)

    def test_quoted_body(self):
        self.denies('gh pr create --body "## Summary\nstuff"')
        self.denies('gh pr create --body="## Summary"')
        self.denies('gh pr create -b "## Summary"')

    def test_body_file(self):
        self.allows("gh pr create -F good.md")
        self.allows("gh pr create --body-file=good.md")
        self.denies("gh pr create --body-file bad.md")

    def test_no_body_or_fill(self):
        self.denies("gh pr create --fill")
        self.denies("gh pr create --title t")

    def test_web(self):
        self.allows("gh pr create --web")
        self.allows("gh pr create -w --title t")


class CommandPosition(HookTest):
    """Finding 1: only a real `gh pr create` invocation is checked."""

    def test_mentions_pass(self):
        self.allows('grep -rn "gh pr create" plugins/')
        self.allows('git commit -m "hook: block gh pr create"')
        self.allows("echo gh pr create")
        self.allows("git status")

    def test_web_in_body_text_does_not_skip(self):
        self.denies("gh pr create " + heredoc_body("## Summary\nopen it with --web or -w"))

    def test_after_separators(self):
        self.denies("git push -u origin HEAD && gh pr create --fill")
        self.denies("git push; gh pr create --fill")
        self.denies("git push\ngh pr create --fill")
        self.denies("(gh pr create --fill)")

    def test_env_prefix(self):
        self.denies("GH_REPO=o/r gh pr create --fill")

    def test_every_invocation_checked(self):
        self.denies("gh pr create -F good.md; gh pr create -F bad.md")


class UnseenBodies(HookTest):
    """Finding 2: fail open when the body is not in the command or its file."""

    def test_stdin(self):
        self.allows("gh pr create --title x -F - < good.md")
        self.allows("cat good.md | gh pr create --body-file -")
        self.allows("cat bad.md | gh pr create --body-file -")

    def test_other_commands_body_file_ignored(self):
        self.allows("git commit -F bad.md && gh pr create -F good.md")
        self.denies("git commit -F good.md && gh pr create -F bad.md")

    def test_substitution_and_variables(self):
        self.allows('gh pr create --body "$(cat bad.md)"')
        self.allows('gh pr create --body "$BODY"')
        self.allows("gh pr create --body `cat bad.md`")

    def test_missing_file(self):
        self.allows("gh pr create -F nowhere.md")

    def test_heredoc_text_that_breaks_shlex(self):
        # An apostrophe or inner double quotes are literal inside a heredoc.
        written = "cat > /tmp/b.md <<'EOF'\nisn't \"it\"\nEOF\n"
        self.denies(written + "gh pr create --fill")
        self.denies(written + "gh pr create " + heredoc_body("## Summary\ndon't \"quote\""))
        self.allows(written + "gh pr create " + heredoc_body(GOOD + "\ndon't \"quote\""))

    def test_here_string_is_not_a_heredoc(self):
        self.denies("gh pr create --fill <<< x")

    def test_unbalanced_quote(self):
        self.allows('gh pr create --body "## Summary')


class Location(HookTest):
    """Finding 3: the template is found from the repo root, not the shell's cwd."""

    def test_from_subdirectory(self):
        sub = os.path.join(self.repo.root, "packages", "api")
        os.makedirs(sub)
        with open(os.path.join(sub, "bad.md"), "w") as fh:
            fh.write(BAD)
        self.denies("gh pr create -F bad.md", cwd=sub)
        self.allows("gh pr create -F ../../good.md", cwd=sub)


class Templates(unittest.TestCase):
    def check(self, repo, command, code):
        try:
            self.assertEqual(repo.run(command)[0], code)
        finally:
            repo.close()

    def test_no_template(self):
        self.check(Repo(template=None), "gh pr create --fill", 0)

    def test_directory_templates_inert(self):
        # Finding 4: several templates have no one set of headings; /review-setup reports it.
        self.check(Repo(template=".github/PULL_REQUEST_TEMPLATE/feature.md"),
                   "gh pr create --fill", 0)

    def test_template_without_headings(self):
        self.check(Repo(content="Describe the change.\n"), "gh pr create --fill", 0)

    def test_other_locations_and_case(self):
        self.check(Repo(template=".github/PULL_REQUEST_TEMPLATE.md"), "gh pr create --fill", 2)
        self.check(Repo(template="pull_request_template.md"), "gh pr create --fill", 2)
        self.check(Repo(template="docs/pull_request_template.md"), "gh pr create --fill", 2)


class Payload(HookTest):
    def test_malformed_json(self):
        self.assertEqual(self.repo.run("", raw="{bad")[0], 0)

    def test_camel_case_key(self):
        self.denies("gh pr create --fill", key="toolInput")


if __name__ == "__main__":
    unittest.main()
