# Skills (Codex + Claude)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/t3chn/skills/graphs/commit-activity)

A curated collection of skills, runbooks, and agent resources for OpenAI Codex and Claude Code.

## Overview

This repository is organized by platform because Codex and Claude Code have different conventions and packaging formats.

## Structure

- **Codex**: `codex/` (Codex-native skills, runbooks, scripts)
- **Claude Code**: `claude/` (Claude Code plugins)
- **Shared**: `shared/` (format-agnostic assets only)

## Codex Skills

Codex skills live in `codex/skills/` and are namespaced with the `vi-` prefix.

Install into `~/.codex/skills` (full sync, overwrites `~/.codex/skills/vi-*`):

```bash
./scripts/install-codex
```

Included skills:

- `vi-brainstorming` — Turn ideas into validated design docs before implementation.
- `vi-beads` — Use `bd` (Beads) for persistent multi-session task memory.
- `vi-frontend-design` — Build distinctive, production-grade frontend UI (avoid generic AI aesthetics).
- `vi-code-review` — Review GitHub PRs via `gh` with confidence scoring and full-SHA links.
- `vi-code-simplifier` — Simplify/refactor code for readability while preserving behavior.

## Contributing

Contributions, suggestions, and improvements are welcome! Feel free to open an issue or submit a pull request.

## License

MIT License - feel free to use this as a template for your own skills documentation.
