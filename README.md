# vi-skills

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet?style=flat-square&logo=anthropic)](https://claude.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE.txt)

Production-ready skills, agents, and hooks for Claude Code. Focused on reliable execution and persistent workflows.

## Installation

```bash
# Via Claude Code CLI
/plugin add https://github.com/anthropics/claude-code-plugins/tree/main/vi-skills
```

## Skills

### Core Workflow

| Skill | Description |
|-------|-------------|
| **[production-flow](./production-flow)** | Unified development flow: pre-commit → beads → TDD → code-review → commit |
| **[beads-workflow](./beads-workflow)** | Task management with beads CLI (v0.35.0+). Molecules, wisps, dependencies |
| **[reliable-execution](./reliable-execution)** | Patterns for persistent agent work. Checkpoints, handoffs, recovery |
| **[context-engineering](./context-engineering)** | Optimize AI context usage. Budget management, structured prompts |

### Code Intelligence

| Skill | Description |
|-------|-------------|
| **[serena-navigation](./serena-navigation)** | Semantic code exploration with serena MCP. Symbols, references, memories |
| **[unified-context](./unified-context)** | Unified Memory API for Redis + Serena hybrid storage |
| **[redis-memory](./redis-memory)** | Redis vector storage for semantic search |
| **[redis-learning](./redis-learning)** | AI-assisted learning from code patterns and errors |

### Development Patterns

| Skill | Description |
|-------|-------------|
| **[backend-core](./backend-core)** | Language-agnostic patterns: API design, auth, security (OWASP) |
| **[mcp-builder](./mcp-builder)** | MCP server development with FastMCP (Python) and MCP SDK (TypeScript) |
| **[secrets-guardian](./secrets-guardian)** | Protect repos from secret leaks. Pre-commit hooks, gitleaks |
| **[tasks-auditor](./tasks-auditor)** | End-of-day audit of beads tasks. Health checks, stale detection |

## Language-Specific Development

| Directory | Description |
|-----------|-------------|
| **[python-dev](./python-dev)** | Python patterns, pytest, FastAPI |
| **[go-dev](./go-dev)** | Go patterns, testing, project structure |
| **[ts-dev](./ts-dev)** | TypeScript patterns, Vitest |
| **[node-dev](./node-dev)** | Node.js patterns, testing |
| **[rust-dev](./rust-dev)** | Rust patterns, testing |
| **[tdd-enforcer](./tdd-enforcer)** | Red-Green-Refactor enforcement |

## Agents

| Agent | Description |
|-------|-------------|
| **[task-tracker](./agents/task-tracker.md)** | Manages beads task lifecycle |
| **[session-checkpoint](./agents/session-checkpoint.md)** | Creates recovery checkpoints |
| **[code-navigator](./agents/code-navigator.md)** | Explores code with serena |

## Commands

| Command | Description |
|---------|-------------|
| `/task` | Quick beads task management |
| `/checkpoint` | Save session progress |
| `/flow` | Production flow quick reference |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| session-context | SessionStart | Inject date, beads context, memory suggestions |
| flow-check | SessionStart | Check production flow compliance |
| skill-suggester | SessionStart | Auto-suggest relevant skills |
| redis-context | SessionStart | Load Redis semantic context |
| suggest-semantic-tools | PreToolUse | Suggest serena tools for Grep/Read |
| session-persist | Stop | Sync beads on exit |
| redis-learn | Stop | Learn from session patterns |

## Session Features

### Date Injection
Every session starts with `**Today:** YYYY-MM-DD` to prevent AI year confusion.

### Memory Suggestions
Hook auto-suggests relevant memories at session start:
- Recent checkpoints (`checkpoint-*.md`)
- Session handoffs (`handoff-*.md`)
- Project overview (`overview-skills.md`)

### Flow Compliance
Checks for: CLAUDE.md, pre-commit hooks, beads setup, tests directory.

## Structure

```
vi-skills/
├── .claude-plugin/        # Plugin marketplace config
├── agents/                # Subagent definitions
├── commands/              # Slash commands
├── hooks/                 # Event hooks
├── scripts/               # Utility scripts (Redis, etc.)
├── tests/                 # Test suite
│
├── production-flow/       # Core workflow skill
├── beads-workflow/        # Task management
├── reliable-execution/    # Persistence patterns
├── context-engineering/   # Context optimization
│
├── serena-navigation/     # Code intelligence
├── unified-context/       # Hybrid memory
├── redis-memory/          # Vector storage
├── redis-learning/        # Pattern learning
│
├── backend-core/          # API patterns
├── mcp-builder/           # MCP development
├── secrets-guardian/      # Security
├── tasks-auditor/         # Task health
│
├── python-dev/            # Python tooling
├── go-dev/                # Go tooling
├── ts-dev/                # TypeScript tooling
├── node-dev/              # Node.js tooling
├── rust-dev/              # Rust tooling
└── tdd-enforcer/          # TDD enforcement
```

## Key Features

### Reliable Execution
- **Checkpoints**: Save progress to serena memories
- **Handoffs**: Seamless session transitions
- **Recovery**: Resume from any checkpoint

### Beads Integration (v0.35.0+)
- **Molecules**: Reusable workflow templates
- **Wisps**: Ephemeral local workflows
- **Dependencies**: Block/wait relationships

### Redis Context Engine
- **Semantic search**: Find relevant context by meaning
- **Execution cache**: Remember command results
- **Guidance cache**: Learn from error resolutions

## Philosophy

1. **Reliable over fast** — Work survives context resets
2. **Persistent state** — Beads + serena + git layers
3. **Practical patterns** — Copy-paste ready, not theory
4. **Modern tooling** — uv, ruff, Vitest, beads v0.35.0

## License

MIT
