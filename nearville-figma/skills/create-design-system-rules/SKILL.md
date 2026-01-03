---
name: create-design-system-rules
description: Generates custom design system rules for the user's codebase. Use when user says "create design system rules", "generate rules for my project", "set up design rules", "customize design system guidelines", or wants to establish project-specific conventions for Figma-to-code workflows. Requires Figma MCP server connection.
---

# Create Design System Rules

Generate project-specific design system rules that guide Figma-to-code implementation. These rules ensure consistent code generation that matches your project's patterns, conventions, and design tokens.

## Core Principles
- **Project-Specific**: Rules tailored to your exact tech stack and patterns
- **Comprehensive**: Cover styling, components, tokens, and conventions
- **Actionable**: Provide clear guidance for code generation
- **Maintainable**: Easy to update as the project evolves

**Announce at start:** "I'm using the create-design-system-rules skill to generate design system rules."

---

## Phase 1: Analyze the Codebase

**Goal**: Understand the project's design patterns and conventions

**Actions**:
1. Identify the tech stack:
   - Framework (React, Vue, Svelte, etc.)
   - Styling approach (Tailwind, CSS Modules, styled-components, etc.)
   - TypeScript usage
2. Find design token sources:
   - Theme files
   - CSS variables
   - Tailwind config
   - Design token files (JSON, JS)
3. Analyze existing components:
   - Component structure patterns
   - Prop naming conventions
   - File organization

---

## Phase 2: Get Figma Context

**Goal**: Understand how the Figma design system is structured

**Actions**:
1. Call `mcp__nearville-figma_figma-desktop__create_design_system_rules` to get the rules prompt
2. If available, call `mcp__nearville-figma_figma-desktop__get_variable_defs` to understand Figma variables
3. Identify:
   - Color naming in Figma
   - Typography styles
   - Spacing conventions
   - Component naming

---

## Phase 3: Map Figma to Code Conventions

**Goal**: Create mappings between Figma design tokens and code equivalents

**Actions**:
1. Map colors:
   - Figma color names → CSS variables/Tailwind classes
   - Semantic color usage (primary, secondary, error, etc.)
2. Map typography:
   - Figma text styles → typography utilities/classes
   - Font family, size, weight, line-height mappings
3. Map spacing:
   - Figma spacing values → spacing scale
   - Common patterns (padding, margins, gaps)
4. Map effects:
   - Shadows → shadow utilities
   - Border radius → radius scale

---

## Phase 4: Document Component Patterns

**Goal**: Capture component conventions for code generation

**Actions**:
1. Document component structure patterns:
   - File naming conventions
   - Directory organization
   - Export patterns
2. Document styling patterns:
   - How to apply styles (className, style props, styled())
   - Responsive breakpoints
   - State styling (hover, focus, active)
3. Document accessibility patterns:
   - Required aria attributes
   - Keyboard navigation patterns
   - Screen reader considerations

---

## Phase 5: Generate Rules File

**Goal**: Create the design system rules file

**Actions**:
1. Create `.claude/figma.md` with:
   ```markdown
   # Design System Rules

   ## Tech Stack
   - Framework: [framework]
   - Styling: [approach]
   - Components: [library]

   ## Token Mappings

   ### Colors
   | Figma Token | Code Equivalent |
   |-------------|-----------------|
   | primary/500 | text-primary-500 |

   ### Typography
   ...

   ## Component Conventions
   ...

   ## Implementation Guidelines
   ...
   ```
2. Include specific examples from the codebase
3. Document any edge cases or exceptions

---

## Output Guidelines

When complete, provide:
1. Summary of rules created
2. Path to the rules file: `.claude/figma.md`
3. Key mappings documented
4. Suggestions for keeping rules updated
5. How these rules will be used during design implementation
