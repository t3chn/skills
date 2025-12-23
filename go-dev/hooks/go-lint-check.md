---
name: go-lint-check
description: Check Go formatting after file edits
event: PostToolUse
matchTools: Edit, Write
matchFiles: "**/*.go"
type: bash
timeout: 5000
---

# Check Go file formatting
FILE="${CLAUDE_TOOL_ARG_file_path:-${CLAUDE_TOOL_ARG_filePath}}"

if [ -n "$FILE" ] && [ -f "$FILE" ]; then
    # Check if gofmt would modify the file
    DIFF=$(gofmt -l "$FILE" 2>/dev/null)
    if [ -n "$DIFF" ]; then
        echo "FORMATTING: $FILE needs gofmt"
    fi
fi
