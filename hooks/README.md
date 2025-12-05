# vi-skills Hooks

Hooks for automatic skill suggestion in Claude Code sessions.

## skill-suggester.sh

SessionStart hook that detects project context and suggests relevant skills.

### What it detects

| Trigger | Skills suggested |
|---------|------------------|
| `Cargo.toml` | backend-rust, backend-core |
| `pyproject.toml` / `requirements.txt` | backend-python, backend-core |
| `package.json` | backend-nodejs, backend-core |
| `tests/` directory (Python) | python-testing |
| `src/components/` or frontend framework | frontend-design |
| MCP/FastMCP in dependencies | mcp-builder |
| `.beads/` directory | beads-workflow |
| gitleaks in `.pre-commit-config.yaml` | secrets-guardian |
| Any git repo with code | code-review |

### Installation

**Автоматически** — хук включён в плагин vi-skills.

При установке плагина хук загружается из `hooks/hooks.json`:
```json
{
  "SessionStart": [{
    "matcher": "",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/hooks/skill-suggester.sh"
    }]
  }]
}
```

Никакой ручной настройки не требуется.

### Output Example

```
# 🎯 Recommended Skills

**INVOKE these skills using the Skill tool before relevant work:**

- `vi-skills:backend-rust` — Cargo.toml → Rust project
- `vi-skills:backend-core` — Backend → core patterns
- `vi-skills:beads-workflow` — .beads/ directory
- `vi-skills:code-review` — Git repo → code review

**Usage:** `Skill(skill="vi-skills:backend-rust")`
```

### How it works

1. Hook runs at session start
2. Detects project type from files (Cargo.toml, package.json, etc.)
3. Outputs skill suggestions to session context
4. Claude sees these suggestions and should invoke relevant skills

### Extending

To add new skill detection, edit `skill-suggester.sh` and add:

```bash
if [ -f "some-marker-file" ]; then
  add_skill "vi-skills:skill-name" "Reason for suggestion"
fi
```
