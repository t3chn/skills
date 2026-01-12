---
name: vi-security-guidance
description: "Security reminders while editing code: workflow injection, command injection, XSS sinks, eval/code execution, and unsafe deserialization. Use when changing CI/workflows, shell/exec code, HTML rendering, auth, or other security-sensitive areas."
---

# Security Guidance (Reminders + Checks)

Use this as a lightweight, manual guardrail when making changes in security-sensitive areas. Prefer concrete threat modeling over generic advice.

## Quick checklist

1. Identify **untrusted inputs** (user content, HTTP params, headers, env vars, CI event payloads).
2. Avoid **shell interpretation**; pass arguments as arrays to non-shell APIs.
3. Validate/normalize inputs; encode outputs for the destination (SQL/HTML/URL/shell).
4. Avoid XSS sinks unless content is trusted and/or properly sanitized.
5. Avoid dynamic code evaluation (`eval`, `new Function`) unless strictly required.
6. Avoid unsafe deserialization (`pickle`) with untrusted data.
7. Be extra careful in CI config (`.github/workflows/*`) where injection is common.

## Common footguns to watch for

- **GitHub Actions workflow injection**: don’t interpolate untrusted event fields into `run:`. Prefer `env:` + quoting, and treat issue/PR titles, bodies, comments, and commit messages as attacker-controlled.
- **Node.js command execution**: avoid `child_process.exec`/`execSync` with dynamic strings; prefer `execFile`/`spawn` with argument arrays; never pass user-controlled input to a shell.
- **Browser/React XSS sinks**: `dangerouslySetInnerHTML`, `.innerHTML =`, `document.write` are high-risk when content isn’t trusted/sanitized (use `textContent` or sanitize with a well-maintained library when HTML is required).
- **Dynamic evaluation**: `eval(` and `new Function` can turn input into code execution.
- **Python**: `pickle` on untrusted data can lead to RCE; `os.system` with dynamic input is command injection.

## Optional: scan your diff

If you have a git repo, run the bundled checker to flag these patterns in `git diff`:

- Working tree diff: `python3 ~/.codex/skills/vi-security-guidance/scripts/check_diff.py`
- Staged diff: `python3 ~/.codex/skills/vi-security-guidance/scripts/check_diff.py --staged`
- Both: `python3 ~/.codex/skills/vi-security-guidance/scripts/check_diff.py --all`

Treat this as a reminder tool (not a security scanner).
