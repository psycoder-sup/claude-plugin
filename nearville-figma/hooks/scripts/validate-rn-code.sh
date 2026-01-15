#!/bin/bash
# validate-rn-code.sh
# PostToolUse hook to validate React Native code quality
# Checks for common issues in RN component files

# Read JSON input from stdin
INPUT=$(cat)

# Extract the file path from the tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only validate .tsx files (React Native components)
if [[ ! "$FILE_PATH" =~ \.(tsx|jsx)$ ]]; then
    exit 0
fi

# Check if file exists
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Read file content
CONTENT=$(cat "$FILE_PATH")
WARNINGS=""

# Check for inline styles (should use StyleSheet)
if echo "$CONTENT" | grep -qE 'style=\{\{'; then
    WARNINGS="${WARNINGS}Consider using StyleSheet instead of inline styles for better performance. "
fi

# Check for hardcoded colors (should use theme)
if echo "$CONTENT" | grep -qE "color:\s*['\"]#[0-9a-fA-F]{3,6}['\"]"; then
    WARNINGS="${WARNINGS}Consider using theme colors instead of hardcoded hex values. "
fi

# Check for hardcoded dimensions
if echo "$CONTENT" | grep -qE "(width|height|padding|margin):\s*[0-9]+[^%]"; then
    # This is just informational, not necessarily wrong
    : # skip
fi

# Check for missing accessibility props in touchables
if echo "$CONTENT" | grep -qE '(Pressable|TouchableOpacity|TouchableHighlight)' && ! echo "$CONTENT" | grep -q 'accessible'; then
    WARNINGS="${WARNINGS}Consider adding accessibility props (accessible, accessibilityLabel) to touchable components. "
fi

# Report warnings (non-blocking)
if [[ -n "$WARNINGS" ]]; then
    echo "{\"warning\": \"${WARNINGS}\"}"
fi

exit 0
