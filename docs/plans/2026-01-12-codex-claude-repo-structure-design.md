# Codex + Claude Repo Structure (Design)

## Goal

Maintain a single repo that can store skills, role prompts, runbooks, scripts, and other agent resources for both:

- OpenAI Codex (Codex CLI skills + repo instructions)
- Claude Code (plugins/agents/commands/skills)

Codex and Claude have different formats and conventions, so the repo must keep them separated to avoid drift and accidental cross-contamination.

## Decisions

### 1) Separate by platform, not by “concept”

- `codex/` contains Codex-native assets.
- `claude/` contains Claude Code assets (plugin structure).
- `shared/` exists only for truly shared, format-agnostic artifacts (templates, reference docs, etc.). No automatic syncing.

Rationale: platform divergence is real (tooling, formats, conventions). Keeping “source-of-truth” separate reduces friction and accidental incompatibilities.

### 2) Codex “agents/roles” are implemented as skills

Codex doesn’t have Claude-style `agents/*.md` as a first-class runtime feature. For Codex, roles like “code reviewer” are represented as `SKILL.md` skill packages.

### 3) Codex skills are namespaced with `vi-`

All Codex skills use a `vi-` prefix (e.g. `vi-brainstorming`, `vi-beads`) to avoid collisions with:

- Codex built-in/system skills
- third-party skill sets

### 4) Codex installation uses copy + full sync

We provide `scripts/install-codex` with this behavior:

1. Delete all existing `~/.codex/skills/vi-*`
2. Copy `codex/skills/vi-*` into `~/.codex/skills/`

Rationale: predictable, reproducible local state; upgrades are “exact mirror of repo”.

### 5) `dist/` is build output, not source

`dist/` contains packaging artifacts (e.g. `*.skill`) and must not be committed. If we later want distributable artifacts, publish them via GitHub Releases instead.

## Repository Layout

```
.
├── codex/
│   ├── skills/
│   │   └── vi-*/SKILL.md
│   ├── runbooks/
│   └── scripts/
├── claude/
│   └── plugins/
├── shared/
├── scripts/
│   └── install-codex
└── docs/
    └── plans/
```

## Migration Plan (initial)

- Move existing `brainstorming/` → `codex/skills/vi-brainstorming/`
- Move existing `beads/` → `codex/skills/vi-beads/`
- Update `name:` in frontmatter to `vi-*`
- Add `scripts/install-codex`
- Add `.gitignore` entry for `dist/` and remove tracked artifacts
