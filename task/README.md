# task

Task planning and execution system for Claude Code with intelligent code analysis agents.

## Commands

### `/plan-task`

Plan features with systematic approach:
1. **Discovery** - Understand requirements, extract Figma design context if UI task
2. **Codebase Exploration** - Launch code-explorer agents to analyze patterns
3. **Clarifying Questions** - Resolve ambiguities before planning
4. **Architecture Design** - Compare approaches using code-architect agents
5. **Create Task File** - Generate comprehensive task file in `docs/tasks/`

**Usage:**
```
/plan-task
```

### `/execute-task`

Execute planned tasks with review checkpoints:
1. Load and review plan file
2. Execute tasks in batches (default: 3 tasks)
3. Report progress and wait for feedback
4. Continue until complete

**Usage:**
```
/execute-task <path-to-task-file>
```

## Agents

### code-architect
Designs feature architectures by analyzing existing patterns. Outputs implementation blueprints with specific files, component designs, and build sequences.

### code-explorer
Analyzes codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies.

## Skills

### planning-tasks
Guided task planning with:
- Codebase understanding via explorer agents
- Architecture focus via architect agents
- Figma MCP integration for UI tasks
- Comprehensive task file output

### executing-tasks
Batch execution with:
- Review checkpoints for architect feedback
- Figma MCP verification for UI implementation
- Stop-and-ask protocol for blockers

## Task File Format

Task files are stored in `docs/tasks/YYYY-MM-DD-<task-name>.md`:

```markdown
# Task Name - [TODO/In-Progress/Done]

## Overview
- Created at: MM/DD/YYYY HH:mm

**SubTasks**:
- [ ] Task 1
- [ ] Task 2

## Design Context (Optional - for UI tasks)
**Figma Reference**: URL, Node ID
**Design Specifications**: Colors, typography, spacing
**Component Hierarchy**: Structure overview
**Design Tokens**: Variables to use/create

## Technical Context
**Key Files**: Relevant source files
**Patterns to Follow**: Conventions to match
```

## Hooks

### PostToolUse: Write
Validates task files written to `docs/tasks/`:
- Checks for required title heading
- Validates Overview section presence
- Warns if SubTasks checklist is missing

## Version

1.1.10
