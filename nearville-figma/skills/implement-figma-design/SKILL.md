---
name: implement-figma-design
description: Translates Figma designs into production-ready React Native code with 1:1 visual fidelity. Use when implementing UI from Figma files, when user mentions "implement design", "generate code", "implement component", "build Figma design", provides Figma URLs, or asks to build components matching Figma specs. Requires Figma MCP server connection.
---

# Implement Figma Design (React Native)

Transform Figma designs into production-ready React Native code with high visual fidelity. This skill guides you through extracting design context, understanding the design system, and generating matching code.

## Core Principles
- **Visual Fidelity**: Match the Figma design as closely as possible
- **Native Components**: Use appropriate React Native components (View, Text, Pressable, etc.)
- **Design System Aware**: Use existing theme tokens and components when available
- **Platform Consideration**: Handle iOS/Android differences when necessary
- **Clean Code**: Generate maintainable, well-structured code with proper TypeScript types

**Announce at start:** "I'm using the implement-figma-design skill to implement this Figma design for React Native."

---

## Phase 1: Extract Design Context

**Goal**: Get complete design information from Figma

**Actions**:
1. If user provides a Figma URL, extract the node ID from it
   - URL format: `https://figma.com/design/:fileKey/:fileName?node-id=1-2` → nodeId is `1:2`
   - Branch format: `https://figma.com/design/:fileKey/branch/:branchKey/:fileName` → use branchKey as fileKey
2. Call `mcp__nearville-figma_figma-desktop__get_design_context` with:
   - `nodeId`: The extracted node ID (or empty for current selection)
   - `clientLanguages`: "typescript"
   - `clientFrameworks`: "react-native"
   - `artifactType`: Type of artifact being created
3. If needed, also call `mcp__nearville-figma_figma-desktop__get_screenshot` to get a visual reference
4. Review the design context output for:
   - Component structure and hierarchy
   - Styles (colors, typography, spacing)
   - Layout information (flexbox direction, alignment, gaps)
   - Any design tokens or variables used

---

## Phase 2: Understand the Codebase

**Goal**: Identify existing patterns, components, and design tokens

**Actions**:
1. Search for existing design system files:
   - Look for theme files (colors, typography, spacing scales)
   - Find existing component library (Button, Text, Card, etc.)
   - Identify styling patterns (StyleSheet, styled-components/emotion, NativeWind, Tamagui, etc.)
2. Check if similar components already exist that can be reused or extended
3. Identify the file structure convention for new components
4. Note any relevant design system rules in `.claude/figma.md` if it exists
5. Check for navigation library usage (React Navigation, Expo Router)

---

## Phase 3: Clarify Requirements

**Goal**: Resolve ambiguities before implementation

**Actions**:
1. Identify unclear aspects:
   - Screen size adaptations (phone vs tablet)
   - Interactive states (pressed, disabled)
   - Animation requirements (Reanimated, Moti, etc.)
   - Component props and variants
   - Navigation behavior
   - Platform-specific requirements (iOS vs Android)
2. Ask clarifying questions if needed
3. Make reasonable assumptions based on design context and document them

---

## Phase 4: Generate Code

**Goal**: Create production-ready React Native code matching the design

**Actions**:
1. Create component file(s) following project conventions
2. Implement the component with:
   - Correct component hierarchy matching Figma structure
   - Use appropriate RN components:
     - `View` for containers/frames
     - `Text` for all text (never raw strings)
     - `Pressable` or `TouchableOpacity` for interactive elements
     - `Image` or `FastImage` for images
     - `ScrollView` or `FlatList` for scrollable content
   - Accurate styling using project's styling approach:
     ```typescript
     // StyleSheet example
     const styles = StyleSheet.create({
       container: {
         flex: 1,
         flexDirection: 'column',
         padding: 16,
       },
     });
     ```
   - Proper use of theme tokens/variables
   - Accessibility props (`accessibilityLabel`, `accessibilityRole`, `accessibilityHint`)
3. Handle all visual states present in the design
4. Add proper TypeScript types for props
5. Export component appropriately

**React Native Styling Notes**:
- All dimensions are unitless (density-independent pixels)
- Flexbox is the primary layout system (default `flexDirection: 'column'`)
- No CSS grid - use nested flex containers
- Use `gap` for spacing between children (RN 0.71+)
- Shadows differ by platform:
  ```typescript
  // iOS
  shadowColor: '#000',
  shadowOffset: { width: 0, height: 2 },
  shadowOpacity: 0.25,
  shadowRadius: 3.84,
  // Android
  elevation: 5,
  ```

---

## Phase 5: Review and Refine

**Goal**: Ensure code quality and design accuracy

**Actions**:
1. Compare generated code against design context
2. Verify:
   - Colors match exactly (hex values, opacity via `rgba()` or separate `opacity` prop)
   - Typography matches (fontFamily, fontSize, fontWeight, lineHeight)
   - Spacing matches (padding, margin, gap)
   - Border radius and effects are correct
3. Check for any hardcoded values that should use theme tokens
4. Ensure code follows project patterns and conventions
5. Verify accessibility props are properly set
6. Check for platform-specific styling needs

---

## Output Guidelines

When complete, provide:
1. Summary of what was implemented
2. File(s) created or modified with paths
3. Any assumptions made
4. Platform considerations (if any iOS/Android differences)
5. Suggestions for testing the implementation
