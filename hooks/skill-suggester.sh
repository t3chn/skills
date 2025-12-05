#!/usr/bin/env bash
# skill-suggester.sh - SessionStart hook for vi-skills
# Detects project context and suggests relevant skills to invoke
#
# Install: Add to ~/.claude/settings.json under hooks.SessionStart
# Output goes to session context (exit 0 = context injection)

set -e

# Collect suggested skills (newline-separated for compatibility)
skills=""
reasons=""

add_skill() {
  local skill="$1"
  local reason="$2"
  # Check if already added
  if [[ "$skills" != *"$skill"* ]]; then
    skills="${skills}${skill}"$'\n'
    reasons="${reasons}${reason}"$'\n'
  fi
}

# =============================================================================
# BACKEND DETECTION
# =============================================================================

# Rust
if [ -f "Cargo.toml" ]; then
  add_skill "vi-skills:backend-rust" "Cargo.toml → Rust project"
fi

# Python
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
  add_skill "vi-skills:backend-python" "Python project detected"

  # Check for tests
  if [ -d "tests" ] || [ -d "test" ]; then
    add_skill "vi-skills:python-testing" "tests/ directory found"
  fi
fi

# Node.js / TypeScript
if [ -f "package.json" ]; then
  add_skill "vi-skills:backend-nodejs" "package.json → Node.js project"
fi

# Add core patterns for any backend
if [ -f "Cargo.toml" ] || [ -f "pyproject.toml" ] || [ -f "package.json" ]; then
  add_skill "vi-skills:backend-core" "Backend → core patterns"
fi

# =============================================================================
# FRONTEND DETECTION
# =============================================================================

# React/Vue/Svelte components
if [ -d "src/components" ] || [ -d "components" ] || [ -d "app/components" ]; then
  add_skill "vi-skills:frontend-design" "Components directory found"
fi

# Check package.json for frontend frameworks
if [ -f "package.json" ]; then
  if grep -qE '"(react|vue|svelte|next|nuxt|astro)"' package.json 2>/dev/null; then
    add_skill "vi-skills:frontend-design" "Frontend framework detected"
  fi
fi

# =============================================================================
# MCP DETECTION
# =============================================================================

if [ -f "pyproject.toml" ] && grep -qi "mcp\|fastmcp" pyproject.toml 2>/dev/null; then
  add_skill "vi-skills:mcp-builder" "MCP/FastMCP in pyproject.toml"
fi

if [ -f "package.json" ] && grep -qi '"@modelcontextprotocol' package.json 2>/dev/null; then
  add_skill "vi-skills:mcp-builder" "MCP SDK in package.json"
fi

# =============================================================================
# WORKFLOW DETECTION
# =============================================================================

# Beads issue tracker
if [ -d ".beads" ]; then
  add_skill "vi-skills:beads-workflow" ".beads/ directory"
fi

# Secrets protection
if [ -f ".pre-commit-config.yaml" ]; then
  if grep -q "gitleaks" .pre-commit-config.yaml 2>/dev/null; then
    add_skill "vi-skills:secrets-guardian" "gitleaks in pre-commit"
  fi
fi

# =============================================================================
# ALWAYS USEFUL (if doing development)
# =============================================================================

# Code review - useful for any code project with git
if [ -d ".git" ] && [ -n "$skills" ]; then
  add_skill "vi-skills:code-review" "Git repo → code review"
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -z "$skills" ]; then
  # No skills detected, exit silently
  exit 0
fi

# Output header
echo "# 🎯 Recommended Skills"
echo ""
echo "**INVOKE these skills using the Skill tool before relevant work:**"
echo ""

# Output skills with reasons (read line by line)
IFS=$'\n'
skill_arr=($skills)
reason_arr=($reasons)
unset IFS

for i in "${!skill_arr[@]}"; do
  if [ -n "${skill_arr[$i]}" ]; then
    echo "- \`${skill_arr[$i]}\` — ${reason_arr[$i]}"
  fi
done

echo ""
echo "**Usage:** \`Skill(skill=\"vi-skills:backend-rust\")\`"
echo ""

# Exit 0 = inject output as context
exit 0
