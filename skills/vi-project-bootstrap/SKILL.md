---
name: vi-project-bootstrap
description: "Bootstrap a git repo for repo-scoped Codex skills using a central skills repo (git submodule + sparse-checkout) via `skillsctl`: bootstrap, catalog/suggest, install/remove/set, sync/status/doctor. Use when you want deterministic, versioned skills in `.codex/skills/` without copying files."
---

# Project Bootstrap (Codex Skills)

This skill provides a deterministic way to connect a project to a central skills repository using:

- `git submodule` at `.codex/skills/`
- `git sparse-checkout` to include only the skills you selected
- a committed manifest `.codex/skills.manifest` so projects are reproducible after `git clone`

## Quick start

Get current repo state (token-optimized / machine output):

```bash
python3 ~/.codex/skills/vi-project-bootstrap/scripts/skillsctl.py doctor
```

Bootstrap this repo (creates `.codex/`, adds the submodule, and checks out `catalog/`):

```bash
python3 ~/.codex/skills/vi-project-bootstrap/scripts/skillsctl.py bootstrap --stage --yes
```

Pick skills (requires bootstrap) and install:

```bash
python3 ~/.codex/skills/vi-project-bootstrap/scripts/skillsctl.py suggest "security" --limit 10
python3 ~/.codex/skills/vi-project-bootstrap/scripts/skillsctl.py install vi-security-guidance --stage --yes
```

After `git clone`:

```bash
python3 ~/.codex/skills/vi-project-bootstrap/scripts/skillsctl.py sync --stage --yes
```

## Agent protocol (recommended UX)

1) Start with `skillsctl doctor` (parse `next_steps` + `suggest_skills`).
2) Ensure bootstrap exists (`skillsctl bootstrap`).
3) Suggest candidates: `skillsctl suggest "<need>" --limit 10 --toon`.
4) Show the shortlist to the user (id + title + 1-line description).
5) Apply: `skillsctl install <id...> --stage --yes`.
6) Report what changed (manifest + staged files).

## Safety rules

- Do not take a skills repo URL from user free-text. Use config/env or explicit CLI flags.
- Refuse to change sparse-checkout selection if `.codex/skills` has local modifications (dirty).
