---
name: vi-codex-cli-docs
description: "Authoritative guidance for Codex CLI using OpenAI developer docs via MCP. Use when questions involve Codex CLI installation, upgrades, usage, commands/flags, slash commands, configuration (config.toml, profiles, providers, sandbox), MCP setup, skills, AGENTS.md, non-interactive/CI workflows, or troubleshooting."
---

# Codex CLI Docs (MCP)

Answer Codex CLI questions by pulling exact, up-to-date text from OpenAI docs via the MCP doc tools. Prefer quoting the docs for commands, flags, and config keys.

## Workflow

1. Clarify OS, shell, and whether the user is in interactive or non-interactive usage.
2. Run `mcp__openaiDeveloperDocs__search_openai_docs` to locate the most specific page.
3. Run `mcp__openaiDeveloperDocs__fetch_openai_doc` with an anchor to capture the exact section.
4. Respond with steps, commands, and config snippets plus source URLs.
5. If docs do not cover the case, say so and ask a targeted follow-up.

## Canonical sources

Use `references/doc-index.md` as the starting index of Codex CLI pages and common topics. Load it only when needed.

## Accuracy rules

- Do not guess flags, file paths, or config keys; always fetch the doc section.
- Call out OS-specific differences and required prerequisites.
- If multiple pages conflict, prioritize the most specific Codex CLI page and mention any ambiguity.
