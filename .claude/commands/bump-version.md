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
- `base/.claude-plugin/plugin.json`
- `task/.claude-plugin/plugin.json`
- `nearville-figma/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

### For Each Plugin (base, task, nearville-figma)

Run these commands to determine if the plugin has **actual code changes**:

1. **Get the last version bump commit hash:**
   ```
   git log --grep="chore(PLUGIN): bump version" -1 --format="%H"
   ```
   Replace `PLUGIN` with the plugin name.

2. **Get changed files since last bump (excluding version files):**
   ```
   git diff <HASH>..HEAD --name-only -- PLUGIN/ | grep -v "plugin.json" | grep -v "marketplace.json"
   ```
   - If no hash found, use: `git diff HEAD~20..HEAD --name-only -- PLUGIN/ | grep -v "plugin.json"`
   - **CRITICAL**: The `grep -v` filters out version files so only actual code changes are counted

3. **Decision logic for this plugin:**
   - If the filtered output is **empty** (no lines) → **DO NOT BUMP** this plugin
   - If the filtered output has **any files** → **BUMP** this plugin

## Step 2: Process Results

**IMPORTANT**: Only bump plugins that have actual code changes (non-empty filtered diff output).

For each plugin that **needs bumping** (has actual code changes):

1. **Calculate new version** - Bump patch version: X.Y.Z → X.Y.(Z+1)

2. **Update files**:
   - Edit `<plugin>/.claude-plugin/plugin.json` - update `"version"` field
   - Edit `.claude-plugin/marketplace.json` - update that plugin's `"version"` entry

3. **Create commit (REQUIRED)**:
   - Stage: `git add <plugin>/.claude-plugin/plugin.json .claude-plugin/marketplace.json`
   - Single plugin: `git commit -m "🔧 chore(<plugin>): bump version to X.Y.Z"`
   - Multiple plugins: `git commit -m "🔧 chore: bump versions (base X.Y.Z, task A.B.C)"`

4. **Report results** - Show which plugins were bumped and their new versions

## No Changes Scenario

If **ALL plugins** have empty filtered diffs (no actual code changes), report:
"No version bumps needed - no plugins have code changes since their last version bump."

**DO NOT bump versions just because a plugin exists or was checked.**
