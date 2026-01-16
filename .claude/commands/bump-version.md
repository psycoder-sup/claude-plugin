---
allowed-tools: Read, Edit, Bash(git log:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git status:*)
description: Detect changed plugins and bump their patch versions
model: sonnet
---

# Bump Plugin Versions

Auto-detect plugins with changes since their last version bump and update their versions.

## Step 1: Gather Current State

First, read the plugin version files and check git history to determine what needs bumping.

### Files to Read
- `base/.claude-plugin/plugin.json`
- `task/.claude-plugin/plugin.json`
- `nearville-figma/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

### Git Commands to Run

For each plugin, find the last version bump commit and check for changes since then:

1. **Find last version bump commit:**
   ```
   git log --oneline --grep="chore(base): bump version" -1
   git log --oneline --grep="chore(task): bump version" -1
   git log --oneline --grep="chore(nearville-figma): bump version" -1
   ```

2. **Get the commit hash for diff comparison:**
   ```
   git log --grep="chore(base): bump version" -1 --format="%H"
   git log --grep="chore(task): bump version" -1 --format="%H"
   git log --grep="chore(nearville-figma): bump version" -1 --format="%H"
   ```

3. **Check for changes since last bump** (use the hash from step 2):
   - If hash found: `git diff <HASH>..HEAD --name-only -- base/`
   - If no hash: `git diff HEAD~10..HEAD --name-only -- base/`
   - Ignore `plugin.json` files in the results (those are version files)

## Step 2: Process Results

Based on the information above:

1. **Identify changed plugins** - Plugins with file changes (not "No changes") need version bumps

2. **Calculate new versions** - For each changed plugin, bump the patch version:
   - X.Y.Z becomes X.Y.(Z+1)
   - Example: 1.0.5 -> 1.0.6

3. **Update files** - For each changed plugin:
   - Edit `<plugin>/.claude-plugin/plugin.json` to update the `"version"` field
   - Edit `.claude-plugin/marketplace.json` to update that plugin's `"version"` entry

4. **Create commit (REQUIRED)** - After updating version files, you MUST create a commit:
   - Stage files: `git add <plugin>/.claude-plugin/plugin.json .claude-plugin/marketplace.json`
   - Single plugin: `git commit -m "🔧 chore(<plugin>): bump version to X.Y.Z"`
   - Multiple plugins: `git commit -m "🔧 chore: bump versions (base X.Y.Z, task A.B.C)"`

5. **Report results** - Show which plugins were bumped, their new versions, and the commit hash

If no plugins have changes, inform the user that no version bumps are needed.
