# vi-skills Plugin Collection

## 🚨 Date Rule

**Before writing any date:** `date +%Y-%m-%d`

---

## Quick Start (New Session)

1. `bd prime` — текущая задача
2. `bd ready` — доступные задачи
3. `read_memory('overview-skills.md')` — обзор проекта

## Key Commands

| Command | Purpose |
|---------|---------|
| `bd ready` | Доступные задачи |
| `bd update <id> --status in_progress` | Начать задачу |
| `bd close <id> --reason "done"` | Завершить задачу |
| `bd sync` | Синхронизация с git |
| `/checkpoint` | Сохранить прогресс |
| `/task` | Быстрое управление задачами |
| `/flow` | Production flow reference |

## Architecture

- **12 Skills** — production-flow, beads-workflow, reliable-execution, context-engineering, serena-navigation, unified-context, redis-memory, redis-learning, backend-core, mcp-builder, secrets-guardian, tasks-auditor
- **5 Lang Plugins** — python-dev, go-dev, ts-dev, node-dev, rust-dev
- **3 Agents** — task-tracker, code-navigator, session-checkpoint
- **4 SessionStart Hooks** — flow-check, skill-suggester, session-context, redis-context

## Redis Context Engine

```bash
python3 scripts/context_engine.py status   # Check status
python3 scripts/context_engine.py context "query"  # Get context
```

## Key Files

| File | Purpose |
|------|---------|
| `hooks/hooks.json` | Hook configuration |
| `scripts/context_engine.py` | Redis context engine |
| `.serena/memories/` | Persistent memories |
| `agents/*.md` | Agent definitions |

## Memories Available

| Memory | Content |
|--------|---------|
| `overview-skills.md` | Skills catalog, key files |
| `quickref-beads.md` | Beads v0.35.0 commands |
| `quickref-redis.md` | Redis context engine ops |
| `patterns-recovery.md` | Session recovery protocol |
| `checkpoint-*.md` | Session checkpoints |

## Session Protocol

**Start:** Hooks auto-inject `bd prime` + memory suggestions

**End:**
```bash
bd sync
git add -A && git commit -m "..."
git push
```
