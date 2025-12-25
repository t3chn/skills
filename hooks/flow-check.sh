#!/usr/bin/env bash
# flow-check.sh - Production flow compliance check
# Runs at SessionStart to verify project follows production flow

set -e

warnings=""
missing_count=0

add_warning() {
  warnings="${warnings}⚠️ $1"$'\n'
  missing_count=$((missing_count + 1))
}

# =============================================================================
# CHECK PRODUCTION FLOW COMPONENTS
# =============================================================================

# Only check if this looks like a code project
if [ ! -f "Cargo.toml" ] && [ ! -f "pyproject.toml" ] && [ ! -f "package.json" ] && [ ! -f "go.mod" ]; then
  exit 0  # Not a code project, skip checks
fi

# 1. CLAUDE.md - Project context for AI
if [ ! -f "CLAUDE.md" ] && [ ! -f ".claude/CLAUDE.md" ]; then
  add_warning "No CLAUDE.md found. Create one: \`/flow new\` or see production-flow skill"
fi

# 2. Pre-commit hooks
if [ ! -f ".pre-commit-config.yaml" ]; then
  add_warning "No .pre-commit-config.yaml. Quality gates missing!"
elif [ ! -f ".git/hooks/pre-commit" ]; then
  add_warning "Pre-commit not installed. Run: \`pre-commit install\`"
fi

# 3. Beads task tracking
if [ ! -d ".beads" ]; then
  add_warning "No .beads/ directory. Run: \`bd init\` for task tracking"
fi

# 4. Tests directory
if [ ! -d "tests" ] && [ ! -d "test" ] && [ ! -d "*_test.go" ] 2>/dev/null; then
  # Check for Go test files or Rust tests
  if ! find . -maxdepth 3 -name "*_test.go" -o -name "*_test.rs" 2>/dev/null | head -1 | grep -q .; then
    if [ ! -d "src" ] || ! grep -r "#\[test\]" src/ 2>/dev/null | head -1 | grep -q .; then
      add_warning "No tests directory found. TDD requires tests!"
    fi
  fi
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -z "$warnings" ]; then
  exit 0  # All good, no output
fi

echo "# Production Flow Check"
echo ""
echo "**Missing components detected:**"
echo ""
echo "$warnings"

# Suggest init-project if multiple components missing
if [ "$missing_count" -ge 2 ]; then
  echo "---"
  echo "**Quick fix:** Run \`/init-project\` to set up everything at once."
  echo ""
else
  echo "Run \`/flow\` for setup guide."
  echo ""
fi

exit 0
