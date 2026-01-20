# Codex Skills

A curated collection of skills, runbooks, and helper scripts for OpenAI Codex CLI.

## Structure

- `skills/` — Codex skills (`SKILL.md`) namespaced with `vi-`
- `runbooks/` — human-readable playbooks (not auto-triggered)
- `scripts/` — repo utilities (installation, helpers)

## Install

Install into `~/.codex/skills` (full sync, overwrites `~/.codex/skills/vi-*`):

```bash
./scripts/install-codex
```

Included skills:

- `vi-brainstorming` — Turn ideas into validated design docs before implementation.
- `vi-beads` — Use `bd` (Beads) for persistent multi-session task memory.
- `vi-frontend-design` — Build distinctive, production-grade frontend UI (avoid generic AI aesthetics).
- `vi-prek` — Set up prek configs/hooks/CI (pre-commit replacement).
- `vi-code-review` — Review GitHub PRs via `gh` with confidence scoring and full-SHA links.
- `vi-code-simplifier` — Simplify/refactor code for readability while preserving behavior.
- `vi-code-explorer` — Deeply trace a feature end-to-end to understand codebase flows.
- `vi-code-architect` — Produce a decisive implementation blueprint that fits existing patterns.
- `vi-code-reviewer` — Review local diffs (`git diff`) with confidence scoring and low false positives.
- `vi-feature-dev` — Guided 7-phase workflow for implementing new features.
- `vi-ralph-loop` — Iterate on the same prompt until objective completion criteria are met.
- `vi-security-guidance` — Security reminders for CI, exec/shell usage, XSS sinks, eval, and unsafe deserialization.

## Contributing

Contributions, suggestions, and improvements are welcome! Feel free to open an issue or submit a pull request.

## License

MIT
