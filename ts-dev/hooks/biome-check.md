---
name: biome-check
description: Check TypeScript/JavaScript formatting with Biome after file edits
event: PostToolUse
matchTools: Edit, Write
matchFiles: "**/*.{ts,tsx,js,jsx}"
type: bash
timeout: 5000
---

# Check TypeScript file formatting with Biome
FILE="${CLAUDE_TOOL_ARG_file_path:-${CLAUDE_TOOL_ARG_filePath}}"

if [ -n "$FILE" ] && [ -f "$FILE" ]; then
    # Check if biome is available and biome.json exists
    if command -v biome &> /dev/null || [ -f "node_modules/.bin/biome" ]; then
        BIOME_CMD="biome"
        if [ -f "node_modules/.bin/biome" ]; then
            BIOME_CMD="./node_modules/.bin/biome"
        fi

        # Check formatting and linting
        OUTPUT=$($BIOME_CMD check "$FILE" 2>&1) || true
        if echo "$OUTPUT" | grep -q "Found"; then
            echo "BIOME: Run 'pnpm biome check --write $FILE' to fix issues"
        fi
    fi
fi
