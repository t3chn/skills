# vi-skills

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet?style=flat-square&logo=anthropic)](https://claude.ai)
[![Skills](https://img.shields.io/badge/Skills-14-blue?style=flat-square)](#skills)
[![Agents](https://img.shields.io/badge/Agents-2-green?style=flat-square)](#agents)
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
| **[backend-core](./backend-core)** | Language-agnostic patterns: API design, auth, security (OWASP), architecture, DevOps. | ~150 |
| **[backend-python](./backend-python)** | Python backend with FastAPI, SQLAlchemy, modern tooling (uv, ruff). | ~330 |
| **[backend-nodejs](./backend-nodejs)** | Node.js/TypeScript with NestJS, Drizzle/Prisma, Vitest, ESLint 9. | ~450 |
| **[backend-rust](./backend-rust)** | Rust backend with Axum, SQLx, teloxide (Telegram). Shuttle/Fly.io deployment. $0 hosting. | ~400 |
| **[frontend-design](./frontend-design)** | Distinctive UI with ready design systems, font pairings, CSS animations. Anti-AI-slop. | ~140 |
| **[mcp-builder](./mcp-builder)** | MCP server development with FastMCP (Python) and MCP SDK (TypeScript). | ~250 |
| **[code-review](./code-review)** | Verification gates, anti-performative agreement, code-reviewer workflow. | ~460 |
| **[skill-creator](./skill-creator)** | Guide for creating effective Claude Code skills. | ~360 |
| **[subagent-creator](./subagent-creator)** | Guide for creating custom subagents. | ~570 |
| **[beads-workflow](./beads-workflow)** | Session management with beads issue tracker. Auto-init, task lifecycle, sync. | ~170 |
| **[secrets-guardian](./secrets-guardian)** | Protect repos from secret leaks. Pre-commit hooks, gitleaks, detect-secrets. | ~400 |
| **[python-testing](./python-testing)** | Pytest best practices, fixtures, async testing, mocking. Includes test-writer agent. | ~800 |
| **[tasks-auditor](./tasks-auditor)** | End-of-day audit of beads tasks. Health checks, stale tasks, duplicates. | ~100 |
| **[support-docs](./support-docs)** | Generate SUPPORT.md for AI support bot from project sources. Auto-generates FAQ. | ~150 |

## Agents

| Agent | Model | Description |
|-------|-------|-------------|
| **[python-test-writer](./python-dev/agents/python-test-writer)** | opus | Generate comprehensive pytest tests with fixtures and mocking. |

> **Code Review:** Use official `feature-dev:code-reviewer` agent with language-specific convention skills (`go-conventions`, `ts-conventions`, etc.) for context.

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| **[skill-suggester](./hooks)** | SessionStart | Auto-detect project type and suggest relevant skills |

The hook runs at session start and outputs skill recommendations based on project files (Cargo.toml → backend-rust, package.json → backend-nodejs, etc.).

## Highlights

### Backend Development
- **Modern tooling enforced**: uv/ruff (Python), Vitest (Node.js), Cargo (Rust)
- Ready templates: Dockerfile, CI/CD, docker-compose
- Security: OWASP Top 10, Argon2id, parameterized queries
- Stack-specific skills: Python, Node.js, **Rust** (new!)
- **$0 Hosting**: Rust + Shuttle.dev/Fly.io for cost-effective MVPs

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
├── hooks/
│   ├── hooks.json           # Plugin hook config
│   └── skill-suggester.sh   # Auto-suggest skills
├── agents/
│   └── code-reviewer.md
├── backend-core/           # Language-agnostic patterns
├── backend-python/         # FastAPI, SQLAlchemy, uv/ruff
├── backend-nodejs/         # NestJS, Drizzle, Vitest
├── backend-rust/           # Axum, teloxide, Shuttle/Fly.io
├── frontend-design/        # Design systems, typography
├── mcp-builder/            # MCP server development
├── code-review/            # Verification gates
├── skill-creator/          # Create skills
├── subagent-creator/       # Create subagents
├── beads-workflow/         # Issue tracker workflow
├── secrets-guardian/       # Secrets protection
├── python-testing/         # Pytest patterns + agent
├── tasks-auditor/          # Beads health checks
└── support-docs/           # AI support bot docs
```

## Philosophy

1. **Practical over theoretical** — Copy-paste code, not explanations
2. **Modern tooling** — uv, ruff, Vitest, not pip/flake8/Jest
3. **Lean content** — No bloat, no basic CS theory
4. **Ready resources** — Design systems, templates, scripts

## License

MIT
