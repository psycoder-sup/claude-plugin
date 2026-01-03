---
name: code-connect-components
description: Connects Figma design components to code components using Code Connect. Use when user says "code connect", "connect this component to code", "connect Figma to code", "map this component", "link component to code", "create code connect mapping", "add code connect", "connect design to code", or wants to establish mappings between Figma designs and code implementations. Requires Figma MCP server connection.
---

# Code Connect Components

Create mappings between Figma design components and code implementations using Figma's Code Connect feature. This enables developers to see relevant code snippets directly in Figma Dev Mode.

## Core Principles
- **Accurate Mapping**: Connect Figma components to their exact code counterparts
- **Props Alignment**: Map Figma variants to component props correctly
- **Documentation**: Provide helpful code snippets in Figma
- **Maintainability**: Create connections that are easy to update

**Announce at start:** "I'm using the code-connect-components skill to connect Figma designs to code."

---

## Phase 1: Identify Components to Connect

**Goal**: Understand which Figma components need code connections

**Actions**:
1. If user provides a Figma URL, extract the node ID
2. Call `mcp__nearville-figma_figma-desktop__get_design_context` to get component information
3. Identify:
   - Component name in Figma
   - Variants and their properties
   - Current connection status (if any)
4. Call `mcp__nearville-figma_figma-desktop__get_metadata` if needed for component hierarchy

---

## Phase 2: Find Corresponding Code Components

**Goal**: Locate the code implementation of the Figma component

**Actions**:
1. Search the codebase for components matching the Figma component name
2. Analyze the code component:
   - Props interface/type
   - Variants supported
   - Export path
3. Verify the code component matches the Figma design functionally
4. Note any discrepancies between Figma variants and code props

---

## Phase 3: Check Code Connect Setup

**Goal**: Ensure Code Connect is properly configured in the project

**Actions**:
1. Check if `figma.config.json` or similar config exists
2. Look for existing `.figma.tsx` or Code Connect files
3. If not set up, guide user through initial setup:
   - Install `@figma/code-connect` package
   - Create configuration file
   - Set up file structure for connections

---

## Phase 4: Create Code Connect Mapping

**Goal**: Write the Code Connect configuration file

**Actions**:
1. Create or update the Code Connect file (typically `ComponentName.figma.tsx`)
2. Include:
   ```tsx
   import figma from '@figma/code-connect'
   import { ComponentName } from './ComponentName'

   figma.connect(ComponentName, 'FIGMA_COMPONENT_URL', {
     props: {
       // Map Figma variants to code props
       variant: figma.enum('Variant', {
         Primary: 'primary',
         Secondary: 'secondary',
       }),
       disabled: figma.boolean('Disabled'),
       label: figma.string('Label'),
     },
     example: (props) => <ComponentName {...props} />,
   })
   ```
3. Map all Figma variants to corresponding code props
4. Handle nested instances if applicable

---

## Phase 5: Validate and Publish

**Goal**: Ensure the connection works correctly

**Actions**:
1. Run Code Connect validation: `npx figma connect`
2. Fix any mapping errors
3. If user wants to publish: `npx figma connect publish`
4. Verify in Figma Dev Mode that code snippets appear correctly

---

## Output Guidelines

When complete, provide:
1. Summary of components connected
2. File(s) created or modified with paths
3. Command to validate: `npx figma connect`
4. Command to publish: `npx figma connect publish`
5. Any variant mappings that may need review
