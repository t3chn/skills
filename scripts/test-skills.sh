#!/bin/bash
# Integration test for convention skills
# Verifies that all skills exist and have correct structure

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Skills Integration Test ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

check() {
    local desc="$1"
    local condition="$2"

    if eval "$condition" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $desc"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗${NC} $desc"
        FAILED=$((FAILED + 1))
    fi
}

echo "## Convention Skills Exist"
check "go-conventions SKILL.md" "[ -f '$SKILLS_ROOT/go-dev/skills/go-conventions/SKILL.md' ]"
check "ts-conventions SKILL.md" "[ -f '$SKILLS_ROOT/ts-dev/skills/ts-conventions/SKILL.md' ]"
check "rust-conventions SKILL.md" "[ -f '$SKILLS_ROOT/rust-dev/skills/rust-conventions/SKILL.md' ]"
check "python-conventions SKILL.md" "[ -f '$SKILLS_ROOT/python-dev/skills/python-conventions/SKILL.md' ]"
check "node-conventions SKILL.md" "[ -f '$SKILLS_ROOT/node-dev/skills/node-conventions/SKILL.md' ]"

echo ""
echo "## Skills Have Required Frontmatter"
for lang in go ts rust python node; do
    dir="${lang}-dev"
    [ "$lang" = "ts" ] && dir="ts-dev"
    [ "$lang" = "node" ] && dir="node-dev"

    skill_file="$SKILLS_ROOT/${dir}/skills/${lang}-conventions/SKILL.md"
    if [ -f "$skill_file" ]; then
        check "${lang}-conventions has 'name:'" "grep -q '^name:' '$skill_file'"
        check "${lang}-conventions has 'globs:'" "grep -q '^globs:' '$skill_file'"
        check "${lang}-conventions has 'description:'" "grep -q '^description:' '$skill_file'"
    fi
done

echo ""
echo "## Marketplace References Skills"
marketplace="$SKILLS_ROOT/.claude-plugin/marketplace.json"
check "marketplace.json exists" "[ -f '$marketplace' ]"
check "marketplace has go-conventions" "grep -q 'go-conventions' '$marketplace'"
check "marketplace has ts-conventions" "grep -q 'ts-conventions' '$marketplace'"
check "marketplace has rust-conventions" "grep -q 'rust-conventions' '$marketplace'"
check "marketplace has python-conventions" "grep -q 'python-conventions' '$marketplace'"
check "marketplace has node-conventions" "grep -q 'node-conventions' '$marketplace'"

echo ""
echo "## Review Commands Exist"
check "go-review.md exists" "[ -f '$SKILLS_ROOT/go-dev/commands/go-review.md' ]"
check "ts-review.md exists" "[ -f '$SKILLS_ROOT/ts-dev/commands/ts-review.md' ]"

echo ""
echo "## No Overlapping Globs"
ts_globs=$(grep 'globs:' "$SKILLS_ROOT/ts-dev/skills/ts-conventions/SKILL.md" || echo "")
node_globs=$(grep 'globs:' "$SKILLS_ROOT/node-dev/skills/node-conventions/SKILL.md" || echo "")
check "ts-conventions no package.json" "! echo '$ts_globs' | grep -q 'package.json'"
check "node-conventions has package.json" "echo '$node_globs' | grep -q 'package.json'"

echo ""
echo "## 2025 Tooling Documented"
check "go-conventions has sqlc" "grep -q 'sqlc' '$SKILLS_ROOT/go-dev/skills/go-conventions/SKILL.md'"
check "ts-conventions has Bun" "grep -q 'Bun' '$SKILLS_ROOT/ts-dev/skills/ts-conventions/SKILL.md'"
check "python-conventions has uv" "grep -q 'uv' '$SKILLS_ROOT/python-dev/skills/python-conventions/SKILL.md'"
check "python-conventions has Ruff" "grep -q 'Ruff' '$SKILLS_ROOT/python-dev/skills/python-conventions/SKILL.md'"
check "rust-conventions has miette" "grep -q 'miette' '$SKILLS_ROOT/rust-dev/skills/rust-conventions/SKILL.md'"
check "rust-conventions has nextest" "grep -q 'nextest' '$SKILLS_ROOT/rust-dev/skills/rust-conventions/SKILL.md'"

echo ""
echo "=== Results ==="
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi

echo ""
echo "All tests passed!"
