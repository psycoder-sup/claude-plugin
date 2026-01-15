# nearville-figma

Figma design-to-code implementation for React Native with Claude Code.

## Requirements

- Figma Desktop app with MCP server running on `http://127.0.0.1:3845/mcp`

## Commands

### `/implement-design`

Translate Figma designs to production-ready React Native code:

1. **Extract Design Context** - Get component structure, styles, layout from Figma
2. **Understand Codebase** - Find existing patterns, components, design tokens
3. **Clarify Requirements** - Resolve platform-specific and interaction questions
4. **Generate Code** - Create React Native components matching the design
5. **Review and Refine** - Verify visual fidelity and code quality

**Usage:**
```
/implement-design <figma-url>
/implement-design  # Uses currently selected node in Figma
```

### `/code-connect`

Connect Figma design components to code implementations using Code Connect.

**Usage:**
```
/code-connect <figma-url>
```

### `/design-system-rules`

Generate custom design system rules for your project based on existing patterns.

**Usage:**
```
/design-system-rules
```

## Skills

### implement-design
Translates Figma designs with:
- 1:1 visual fidelity
- React Native best practices (View, Text, Pressable, etc.)
- Design token integration
- Platform considerations (iOS/Android)
- Accessibility props

### code-connect-components
Maps Figma components to code using Code Connect for design-to-code consistency.

### create-design-system-rules
Analyzes your codebase to generate `.claude/figma.md` rules for consistent Figma-to-code workflows.

## MCP Tools

This plugin uses Figma MCP server tools:
- `get_design_context` - Extract design specs and code hints
- `get_screenshot` - Visual reference of designs
- `get_variable_defs` - Design tokens and variables
- `get_metadata` - Node structure overview

## React Native Notes

- All dimensions are density-independent pixels (unitless)
- Flexbox layout (default `flexDirection: 'column'`)
- Use `gap` for spacing (RN 0.71+)
- Platform-specific shadows:
  ```typescript
  // iOS
  shadowColor, shadowOffset, shadowOpacity, shadowRadius
  // Android
  elevation
  ```

## Agents

### design-analyzer
Analyzes Figma designs to identify:
- Component structure and patterns
- Design tokens (colors, typography, spacing)
- Implementation priorities
- Reusable component opportunities

### component-matcher
Matches Figma design components to existing code:
- Searches codebase for similar components
- Evaluates visual and prop compatibility
- Suggests adaptations needed

## Hooks

### PostToolUse: Write|Edit
Validates React Native code quality:
- Suggests StyleSheet over inline styles
- Warns about hardcoded colors (use theme)
- Recommends accessibility props on touchables

## Version

1.0.2
