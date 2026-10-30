---
allowed-tools: Read, Edit, Bash(git log:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git status:*)
description: Detect changed plugins and bump their patch versions
model: sonnet
---

# Bump Plugin Versions

Auto-detect plugins with changes since their last version bump and update their versions.

## Step 1: Gather Current State

Read the version files and check git history for each plugin.

### Files to Read
- `.claude-plugin/marketplace.json` - its `plugins` list is the set of active plugins
- `<plugin>/.claude-plugin/plugin.json` for each plugin listed there

Never bump anything under `archive/`.

### For Each Active Plugin

Run these commands to determine if the plugin has **actual code changes**:

1. **Get the last version bump commit hash:**
   ```
   git log -E --grep="chore\(PLUGIN\): bump version|bump versions.*PLUGIN" -1 --format="%H"
   ```
   Replace `PLUGIN` with the plugin name.

   This pattern matches both commit formats:
   - Single: `🔧 chore(base): bump version to X.Y.Z`
   - Multiple: `🔧 chore: bump versions (base X.Y.Z, task A.B.C)`

2. **Get changed files since last bump (excluding version/doc files):**
   ```
   git diff <HASH>..HEAD --name-only -- PLUGIN/ | grep -v "plugin.json" | grep -v "marketplace.json" | grep -v "README.md"
   ```
   - If no hash found, use: `git diff HEAD~20..HEAD --name-only -- PLUGIN/ | grep -v "plugin.json" | grep -v "README.md"`
   - **CRITICAL**: The `grep -v` filters out version and documentation files so only actual code changes are counted

3. **Decision logic for this plugin:**
   - If the filtered output is **empty** (no lines) → **DO NOT BUMP** this plugin
   - If the filtered output has **any files** → **BUMP** this plugin

## Step 2: Process Results

**IMPORTANT**: Only bump plugins that have actual code changes (non-empty filtered diff output).

For each plugin that **needs bumping** (has actual code changes):

1. **Calculate new version** - Bump patch version: X.Y.Z → X.Y.(Z+1)

2. **Update version files**:
   - Edit `<plugin>/.claude-plugin/plugin.json` - update `"version"` field
   - Edit `.claude-plugin/marketplace.json` - update that plugin's `"version"` entry

3. **Update documentation files**:
   - Edit `<plugin>/README.md` - update the version number in the `## Version` section at the end of the file
     ```markdown
     ## Version

     X.Y.Z
     ```
   - Edit `README.md` (root) - update the version column in the plugins table
     ```markdown
     | [<plugin>](./<plugin>) | X.Y.Z | Description... |
     ```

4. **Create commit (REQUIRED)**:
   - Stage: `git add <plugin>/.claude-plugin/plugin.json .claude-plugin/marketplace.json <plugin>/README.md README.md`
   - Single plugin: `git commit -m "🔧 chore(<plugin>): bump version to X.Y.Z"`
   - Multiple plugins: `git commit -m "🔧 chore: bump versions (review X.Y.Z, other A.B.C)"`

5. **Report results** - Show which plugins were bumped and their new versions

## No Changes Scenario

If **ALL plugins** have empty filtered diffs (no actual code changes), report:
"No version bumps needed - no plugins have code changes since their last version bump."

**DO NOT bump versions just because a plugin exists or was checked.**
