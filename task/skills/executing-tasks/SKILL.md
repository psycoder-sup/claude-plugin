---
name: executing-tasks
description: This skill should be used when the user has a task plan file and asks to "execute the plan", "run the tasks", "implement the plan", "work through the tasks", "start execution", or wants to systematically execute planned work items with review checkpoints.
allowed-tools:
  - mcp__plugin_figma_figma-desktop__get_design_context
  - mcp__plugin_figma_figma-desktop__get_screenshot
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. **If plan has Design Context section (UI task)**:
   - Note the Figma reference (URL, node ID)
   - Review design specifications (colors, typography, spacing)
   - Understand component hierarchy
   - Identify design tokens to use or create
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. **For UI implementation tasks**:
   - Use `mcp__plugin_figma_figma-desktop__get_design_context` to get detailed specs for the component being implemented
   - Reference design tokens from the plan's Design Context section
   - Match colors, typography, and spacing exactly as specified
   - Use `mcp__plugin_figma_figma-desktop__get_screenshot` if visual reference needed
4. Run verifications as specified
5. Mark as completed

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly
- **For UI tasks**: Design specs are ambiguous, Figma node not accessible, or design conflicts with existing patterns

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
- **For UI tasks**: Use Figma MCP to verify implementation matches design specs