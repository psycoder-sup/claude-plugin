---
name: planning-tasks
description: This skill should be used when the user asks to "plan a feature", "create a task plan", "break down this work", "help me plan implementation", "design the architecture", or needs systematic planning for development work. Provides guided task planning with codebase understanding, architecture focus, and delivers a comprehensive plan file.
allowed-tools:
  - mcp__plugin_figma_figma-desktop__get_design_context
  - mcp__plugin_figma_figma-desktop__get_screenshot
  - mcp__plugin_figma_figma-desktop__get_variable_defs
---

# Task planner

Help a developer to make a concrete plan for implementation. Follow the systemic approach: understand user requests deeply. Analyze the user's request to understand its impact of existing code base. Consequently create a plan file.

## Core Principles
- **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions rather than making assumptions. Wait for user answer before proceeding with implementation. Ask questions early (after understanding the codebase, before creating task files).
- **Understand before plan**: Read and comprehend existing code patterns first
- **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read. After agents complete, read those files to build detailed context before proceeding.
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound plan
- **Create a task file**: Create a comprehensive task file in docs/tasks directory (create one if not exists). Save task plans to `docs/tasks/YYYY-MM-DD-<task-name>.md`. Always follow the task file template structure (see Phase 5).


**Announce at start:** "I'm using the planning-tasks skill to implement this plan."

---

## Phase 1: Discovery

**Goal**: Understand what needs to be built, including design context when applicable

Ask user for a brief explanation of the task.

**Actions**:
1. If user requests are unclear, ask user for detailed information.
2. **Check for UI/Design work**: Determine if this task involves UI implementation
   - User provides a Figma URL
   - Task description mentions UI, design, component, screen, or visual elements
3. **If Figma design is involved**, extract design context:
   - Extract node ID from Figma URL if provided (format: `?node-id=1-2` → `1:2`)
   - Call `mcp__plugin_figma_figma-desktop__get_design_context` with:
     - `nodeId`: The extracted node ID (or empty for current selection)
     - `clientLanguages`: Appropriate language for the project
     - `clientFrameworks`: Appropriate framework for the project
   - Call `mcp__plugin_figma_figma-desktop__get_screenshot` for visual reference
   - Call `mcp__plugin_figma_figma-desktop__get_variable_defs` to understand design tokens
   - Document key findings:
     - Component structure and hierarchy
     - Design tokens/variables used (colors, typography, spacing)
     - Layout patterns (flex direction, alignment, gaps)
     - Interactive states if present
4. Summarize understanding and confirm with user

---

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns at both high and low levels

**Actions**:
1. Launch 2-3 task:code-explorer agents in parallel. Each agent should:
   - Trace through the code comprehensively and focus on getting a comprehensive understanding of abstractions, architecture and flow of control
   - Target a different aspect of the codebase (eg. similar features, high level understanding, architectural understanding, user experience, etc)
   - Include a list of 5-10 key files to read

   **Example agent prompts**
   - "Find features similar to [feature] and trace through their implementation comprehensively"
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"
   - "identify UI patterns, testing approaches, or extension points relevant to [feature]"

2. Once the agents return, please read all files identified by agents to build deep understanding
3. Present comprehensive summary of findings and patterns discovered

---

## Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities before planning

**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

**Actions**:
1. Review the codebase findings and original user request
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs
3. **Present all questions to the user in a clear, organized list**
4. **wait for answers before proceeding to architecture design**

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation.


---

## Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches with different trade-offs

**Actions**:
1. Launch 2-3 task:code-architect agents in parallel with different focuses: minimal changes (smallest change, maximum reuse), clean architecture (maintainability, elegant abstractions), or pragmatic balance (speed + quality)
2. Review all approaches and form your opinion on which fits best for this specific task (consider: small fix vs large feature, urgency, complexity, team context)
3. Present to user: brief summary of each approach, trade-offs comparison, **your recommendation with reasoning**, concrete implementation differences
4. **Ask user which approach they prefer**

---

## Phase 5: Create task file

**Goal**: Create a task file following the [task file template](./references/task-template.md) exactly.

**Actions**:
1. Read all relevant files identified in previous phases
2. Create a task file in docs/tasks/ directory
3. **Always follow the template structure** - fill in all sections:
   - **Overview**: Task summary, dates, and SubTasks checklist
   - **Design Context** (for UI/design tasks): Fill in Figma Reference, Design Specifications table, Component Hierarchy, and Design Tokens from Phase 1 findings
   - **Technical Context**: Key files, patterns to follow, and architecture notes from Phase 2 findings
4. For non-design tasks, omit the Design Context section entirely (it's marked optional in template)
5. Ensure SubTasks in Overview are concrete, actionable items derived from the chosen architecture approach

---
