---
name: vi-greptile
description: "Use the Greptile MCP integration to inspect PRs, reviews, and comments, trigger Greptile reviews, and manage custom context. Use when requests mention Greptile, Greptile MCP, Greptile review comments, or setting the GREPTILE_API_KEY."
---

# Greptile MCP

Use Greptile MCP tools to work with PR reviews and Greptile context. Keep credentials safe and avoid guessing configuration.

## Setup checklist

1. Confirm `GREPTILE_API_KEY` is set in the user's shell environment.
2. Prefer adding the export to `~/.zshrc` or `~/.bashrc` as shown in `references/greptile.md`.
3. For non-interactive runs, ensure the environment variable is passed to the Codex process.
4. If the Greptile MCP server is not configured, ask the user to add it and follow Greptile docs; do not guess config keys.

## Tool usage

1. Use `list_pull_requests` to find the PR, then `get_merge_request` for details.
2. Use `list_merge_request_comments` or `search_greptile_comments` to collect feedback.
3. Use `trigger_code_review` to start a new review when requested.
4. Use custom context tools to inspect or add organization rules.

See `references/greptile.md` for the exact tool list and example prompts.

## Safety

- Do not print, log, or commit the API key.
- If the key is missing, ask the user to set it and re-run the task.
