#!/bin/bash
# validate-task-file.sh
# PostToolUse hook to validate task file format after writing
# Ensures task files in docs/tasks/ have required sections

# Read JSON input from stdin
INPUT=$(cat)

# Extract the file path from the tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only validate files in docs/tasks/ directory
if [[ ! "$FILE_PATH" =~ docs/tasks/.*\.md$ ]]; then
    exit 0
fi

# Check if file exists
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Read file content
CONTENT=$(cat "$FILE_PATH")

# Check for required sections
MISSING_SECTIONS=""

# Check for title (# heading)
if ! echo "$CONTENT" | grep -q '^# '; then
    MISSING_SECTIONS="${MISSING_SECTIONS}Title (# heading), "
fi

# Check for Overview section
if ! echo "$CONTENT" | grep -q '^## Overview'; then
    MISSING_SECTIONS="${MISSING_SECTIONS}Overview section, "
fi

# Check for SubTasks
if ! echo "$CONTENT" | grep -q '\- \[ \]'; then
    MISSING_SECTIONS="${MISSING_SECTIONS}SubTasks checklist, "
fi

# Report missing sections as a warning (non-blocking)
if [[ -n "$MISSING_SECTIONS" ]]; then
    # Remove trailing comma and space
    MISSING_SECTIONS=${MISSING_SECTIONS%, }
    echo "{\"warning\": \"Task file may be missing: ${MISSING_SECTIONS}\"}"
    # Exit 0 to not block - just warn
    exit 0
fi

exit 0
