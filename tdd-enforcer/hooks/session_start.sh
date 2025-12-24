#!/bin/bash
# TDD Enforcer - Session Start Hook
# Detects project language and test framework

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(pwd)"

# Detect language and test framework
detect_language() {
    if [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "package.json" ]; then
        echo "typescript"
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        echo "python"
    else
        echo "unknown"
    fi
}

detect_test_command() {
    local lang="$1"
    case "$lang" in
        go)
            echo "go test ./..."
            ;;
        rust)
            echo "cargo test"
            ;;
        typescript)
            if [ -f "package.json" ]; then
                if grep -q '"vitest"' package.json 2>/dev/null; then
                    echo "pnpm vitest run"
                elif grep -q '"jest"' package.json 2>/dev/null; then
                    echo "npm test"
                else
                    echo "npm test"
                fi
            else
                echo "npm test"
            fi
            ;;
        python)
            if [ -f "pytest.ini" ] || grep -q "pytest" pyproject.toml 2>/dev/null; then
                echo "pytest"
            else
                echo "python -m pytest"
            fi
            ;;
        *)
            echo ""
            ;;
    esac
}

detect_test_pattern() {
    local lang="$1"
    case "$lang" in
        go)
            echo "*_test.go"
            ;;
        rust)
            echo "*_test.rs|tests/*.rs"
            ;;
        typescript)
            echo "*.test.ts|*.spec.ts|*.test.tsx|*.spec.tsx"
            ;;
        python)
            echo "test_*.py|*_test.py"
            ;;
        *)
            echo ""
            ;;
    esac
}

# Main detection
LANG=$(detect_language)
TEST_CMD=$(detect_test_command "$LANG")
TEST_PATTERN=$(detect_test_pattern "$LANG")

# Check for local config override
CONFIG_FILE=".claude/tdd-enforcer.local.md"
STRICT_MODE="false"

if [ -f "$CONFIG_FILE" ]; then
    # Parse YAML frontmatter for strictMode
    if grep -q "strictMode: true" "$CONFIG_FILE" 2>/dev/null; then
        STRICT_MODE="true"
    fi
    # Override test command if specified
    CUSTOM_CMD=$(grep "testCommand:" "$CONFIG_FILE" 2>/dev/null | sed 's/testCommand: *//')
    if [ -n "$CUSTOM_CMD" ]; then
        TEST_CMD="$CUSTOM_CMD"
    fi
fi

# Output context for Claude
if [ "$LANG" != "unknown" ]; then
    echo "TDD Enforcer: Detected $LANG project"
    echo "Test command: $TEST_CMD"
    echo "Test patterns: $TEST_PATTERN"
    if [ "$STRICT_MODE" = "true" ]; then
        echo "Mode: STRICT (blocking)"
    else
        echo "Mode: WARNING (advisory)"
    fi
fi
