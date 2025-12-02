# vi-skills

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet?style=flat-square&logo=anthropic)](https://claude.ai)
[![Skills](https://img.shields.io/badge/Skills-10-blue?style=flat-square)](#skills)
[![Agents](https://img.shields.io/badge/Agents-3-green?style=flat-square)](#agents)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE.txt)

Production-ready skills and agents for Claude Code. Optimized for practical use, not theory.

## Installation

```bash
# Via Claude Code CLI
/plugin add https://github.com/t3chn/skills
```

## Skills

| Skill | Description | Lines |
|-------|-------------|-------|
| **[backend-development](./backend-development)** | Node.js/Python/Go/Rust, APIs, security (OWASP), DevOps. Modern tooling: uv, ruff, Vitest. | ~5.5k |
| **[frontend-design](./frontend-design)** | Distinctive UI with ready design systems, font pairings, CSS animations. Anti-AI-slop. | ~1k |
| **[code-review](./code-review)** | Verification gates, anti-performative agreement, code-reviewer workflow. | ~460 |
| **[mcp-builder](./mcp-builder)** | MCP server development with FastMCP (Python) and MCP SDK (TypeScript). | ~2k |
| **[skill-creator](./skill-creator)** | Guide for creating effective Claude Code skills. | ~360 |
| **[subagent-creator](./subagent-creator)** | Guide for creating custom subagents. | ~570 |
| **[beads-workflow](./beads-workflow)** | Session management with beads issue tracker. Auto-init, task lifecycle, sync. | ~300 |
| **[daily-planner](./daily-planner)** | Daily planning workflow. Fetch ready tasks, prioritize, track progress. | ~150 |
| **[secrets-guardian](./secrets-guardian)** | Protect repos from secret leaks. Pre-commit hooks, gitleaks, detect-secrets. | ~400 |
| **[python-testing](./python-testing)** | Pytest best practices, fixtures, async testing, mocking. Includes test-writer agent. | ~800 |

## Agents

| Agent | Model | Description |
|-------|-------|-------------|
| **[code-reviewer](./agents/code-reviewer.md)** | opus | Review code changes between commits. Returns issues with file:line references. |
| **[python-test-writer](./python-testing/agents/python-test-writer.md)** | opus | Generate comprehensive pytest tests with fixtures and mocking. |
| **[tasks-auditor](./agents/tasks-auditor.md)** | sonnet | End-of-day audit of beads tasks. Finds duplicates, stale issues, orphaned deps. |

## Highlights

### Backend Development
- **Modern tooling enforced**: uv/ruff (Python), Vitest (Node.js)
- Ready templates: Dockerfile, CI/CD, docker-compose
- Security: OWASP Top 10, Argon2id, parameterized queries
- Stack-specific: Node.js, Python, Go, Rust

### Frontend Design
- **6 ready design systems** with fonts + colors + spacing
- Curated Google Fonts pairings
- CSS animations (copy-paste ready)
- Modern CSS: container queries, :has(), oklch()

### Code Review
- **Verification gates**: No claims without evidence
- Anti-performative agreement (no "You're absolutely right!")
- Stack-specific verification commands
- Git SHA automation script

## Structure

```
vi-skills/
├── .claude-plugin/
│   └── marketplace.json
├── agents/
│   ├── code-reviewer.md
│   └── tasks-auditor.md
├── backend-development/
│   ├── SKILL.md
│   ├── references/
│   ├── templates/
│   └── scripts/
├── frontend-design/
│   ├── SKILL.md
│   └── references/
├── code-review/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── mcp-builder/
│   ├── SKILL.md
│   ├── reference/
│   └── scripts/
├── skill-creator/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── subagent-creator/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── beads-workflow/
│   ├── SKILL.md
│   └── references/
├── daily-planner/
│   └── SKILL.md
├── secrets-guardian/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
└── python-testing/
    ├── SKILL.md
    ├── agents/
    └── references/
```

## Philosophy

1. **Practical over theoretical** — Copy-paste code, not explanations
2. **Modern tooling** — uv, ruff, Vitest, not pip/flake8/Jest
3. **Lean content** — No bloat, no basic CS theory
4. **Ready resources** — Design systems, templates, scripts

## License

MIT
