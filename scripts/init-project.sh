#!/usr/bin/env bash
# init-project.sh - Initialize project for production workflow
#
# Usage:
#   ./init-project.sh                    # Interactive mode
#   ./init-project.sh --name "My App"    # With project name
#   ./init-project.sh --minimal          # Only beads + CLAUDE.md
#
# Creates:
#   - .beads/ (task tracking)
#   - .serena/ (code memory)
#   - CLAUDE.md (AI quick reference)
#   - .pre-commit-config.yaml (optional)

set -e

# =============================================================================
# COLORS
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# PARSE ARGUMENTS
# =============================================================================

PROJECT_NAME=""
MINIMAL=false
SKIP_PRECOMMIT=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --name)
      PROJECT_NAME="$2"
      shift 2
      ;;
    --minimal)
      MINIMAL=true
      shift
      ;;
    --skip-precommit)
      SKIP_PRECOMMIT=true
      shift
      ;;
    -h|--help)
      echo "Usage: init-project.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --name NAME       Project name (default: directory name)"
      echo "  --minimal         Only beads + CLAUDE.md (no serena, no pre-commit)"
      echo "  --skip-precommit  Skip pre-commit setup"
      echo "  -h, --help        Show this help"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Default project name from directory
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(basename "$(pwd)")
fi

# =============================================================================
# CHECK PREREQUISITES
# =============================================================================

echo -e "${BLUE}🚀 Initializing project: ${PROJECT_NAME}${NC}"
echo ""

# Check if git repo
if [ ! -d ".git" ]; then
  echo -e "${YELLOW}⚠️  Not a git repository. Initialize git first:${NC}"
  echo "   git init"
  exit 1
fi

# =============================================================================
# STEP 1: BEADS (Task Tracking)
# =============================================================================

echo -e "${BLUE}[1/4] Setting up beads (task tracking)...${NC}"

if [ -d ".beads" ]; then
  echo -e "${GREEN}  ✓ .beads/ already exists${NC}"
else
  if command -v bd &> /dev/null; then
    bd init
    echo -e "${GREEN}  ✓ beads initialized${NC}"
  else
    echo -e "${YELLOW}  ⚠ beads CLI not found. Install: cargo install beads${NC}"
    echo -e "${YELLOW}    Skipping beads setup${NC}"
  fi
fi

# =============================================================================
# STEP 2: SERENA (Code Memory)
# =============================================================================

if [ "$MINIMAL" = false ]; then
  echo -e "${BLUE}[2/4] Setting up serena (code memory)...${NC}"

  mkdir -p .serena/memories

  if [ ! -f ".serena/project.yml" ]; then
    cat > .serena/project.yml << EOF
version: "1.0"
name: "${PROJECT_NAME}"
description: "Project initialized with vi-skills production flow"
EOF
    echo -e "${GREEN}  ✓ .serena/project.yml created${NC}"
  else
    echo -e "${GREEN}  ✓ .serena/project.yml already exists${NC}"
  fi

  # Create overview memory
  if [ ! -f ".serena/memories/overview.md" ]; then
    cat > .serena/memories/overview.md << EOF
# ${PROJECT_NAME} Overview

## Structure
\`\`\`
$(ls -1 | head -20)
\`\`\`

## Key Files
- README.md — project documentation
- CLAUDE.md — AI quick reference

## Patterns
[Add patterns used in this project]

## Notes
[Add important notes for future sessions]
EOF
    echo -e "${GREEN}  ✓ .serena/memories/overview.md created${NC}"
  else
    echo -e "${GREEN}  ✓ overview.md already exists${NC}"
  fi
else
  echo -e "${YELLOW}[2/4] Skipping serena (--minimal mode)${NC}"
fi

# =============================================================================
# STEP 3: CLAUDE.md (AI Quick Reference)
# =============================================================================

echo -e "${BLUE}[3/4] Creating CLAUDE.md...${NC}"

if [ ! -f "CLAUDE.md" ]; then
  # Detect language/framework
  LANG_SECTION=""
  if [ -f "package.json" ]; then
    LANG_SECTION="## Stack
- Node.js / TypeScript
- Run: \`npm install && npm run dev\`
- Test: \`npm test\`
"
  elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    LANG_SECTION="## Stack
- Python
- Run: \`uv sync && uv run python main.py\`
- Test: \`pytest\`
"
  elif [ -f "go.mod" ]; then
    LANG_SECTION="## Stack
- Go
- Run: \`go run .\`
- Test: \`go test ./...\`
"
  elif [ -f "Cargo.toml" ]; then
    LANG_SECTION="## Stack
- Rust
- Run: \`cargo run\`
- Test: \`cargo test\`
"
  fi

  cat > CLAUDE.md << EOF
# ${PROJECT_NAME}

## Quick Start (New Session)
1. \`bd prime\` — текущая задача
2. \`bd ready\` — доступные задачи
3. \`read_memory('overview.md')\` — обзор проекта

## Key Commands
| Command | Purpose |
|---------|---------|
| \`bd ready\` | Доступные задачи |
| \`bd update <id> --status in_progress\` | Начать задачу |
| \`bd close <id>\` | Завершить задачу |
| \`/checkpoint\` | Сохранить прогресс |
| \`/commit\` | Создать коммит |

${LANG_SECTION}
## Architecture
[Describe key components]

## Documentation Rule
При добавлении фичей обновляй:
1. README.md — если user-facing
2. CLAUDE.md — если меняется workflow
3. Serena memory — если часто используется
EOF
  echo -e "${GREEN}  ✓ CLAUDE.md created${NC}"
else
  echo -e "${GREEN}  ✓ CLAUDE.md already exists${NC}"
fi

# =============================================================================
# STEP 4: PRE-COMMIT (Code Quality)
# =============================================================================

if [ "$MINIMAL" = false ] && [ "$SKIP_PRECOMMIT" = false ]; then
  echo -e "${BLUE}[4/4] Setting up pre-commit hooks...${NC}"

  if [ ! -f ".pre-commit-config.yaml" ]; then
    cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
EOF
    echo -e "${GREEN}  ✓ .pre-commit-config.yaml created${NC}"

    # Install pre-commit if available
    if command -v pre-commit &> /dev/null; then
      pre-commit install --install-hooks -t pre-commit -t commit-msg 2>/dev/null || true
      echo -e "${GREEN}  ✓ pre-commit hooks installed${NC}"
    else
      echo -e "${YELLOW}  ⚠ pre-commit not found. Install: pip install pre-commit${NC}"
      echo -e "${YELLOW}    Then run: pre-commit install${NC}"
    fi
  else
    echo -e "${GREEN}  ✓ .pre-commit-config.yaml already exists${NC}"
  fi
else
  echo -e "${YELLOW}[4/4] Skipping pre-commit${NC}"
fi

# =============================================================================
# SUMMARY
# =============================================================================

echo ""
echo -e "${GREEN}✅ Project initialized!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review and customize CLAUDE.md"
echo "  2. Update .serena/memories/overview.md with project details"
echo "  3. Create first task: bd create --title \"...\" --type task"
echo "  4. Commit setup: git add -A && git commit -m \"chore: init production workflow\""
echo "  5. Sync beads: bd sync"
echo ""
