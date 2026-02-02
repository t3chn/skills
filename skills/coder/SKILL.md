---
name: coder
description: "Work with Coder using the `coder` CLI and API, especially Coder Tasks (AI agents in Coder workspaces): create/list/monitor tasks (`coder task create|list|status|logs|send|delete`), pick task templates/presets, and troubleshoot task-template requirements (`coder_ai_task` and `coder_task`). Triggers: Coder, Coder Tasks, coder task, coder_ai_task, AgentAPI, AI Bridge, templates push."
---

# Coder (Tasks-first)

## Goal

Use Coder Tasks as the primary unit of work (a task runs an agent inside an isolated Coder workspace), and manage tasks from the terminal reliably.

## Quick start (CLI)

1) Ensure `coder` CLI is installed and authenticated

- Login: `coder login <url>`
- Print current session token (useful for API calls): `coder login token`

2) Create a task

- Direct input: `coder task create "<prompt>"`
- From stdin: `echo "<prompt>" | coder task create`
- Non-interactive: pass `--template`, optional `--preset`, optional `--name`
- Automation: add `--quiet` to print only the task ID

3) Monitor + iterate

- Watch status: `coder task status <task> --watch`
- Send follow-ups: `coder task send <task> "<more instructions>"`
- Inspect logs: `coder task logs <task> -o json`

4) Cleanup

- Delete (no prompt): `coder task delete <task> --yes`

## Task templates (required)

If `coder task create` fails with something like “no task templates configured”, the deployment has no templates that are Tasks-capable.

A template becomes Tasks-capable when it defines:

- `resource "coder_ai_task" ...` (links a workspace app to the Task UI)
- `data "coder_task" "me" {}` (gives access to the task prompt and metadata)
- An agent module (Codex CLI, Claude Code, etc.) that runs in the workspace and consumes `data.coder_task.me.prompt`

Minimal Terraform snippet + notes: `references/task-template-snippet.md`.

## API (automation)

If you need to create tasks from CI/GitHub automation (or without the `coder` CLI), use the Tasks API (`/api/v2/tasks/...`) with a Coder session token.

Quick reference: `references/api.md`.

## Safety defaults

- Prefer a dedicated, locked-down Task template (least privilege, no prod secrets).
- Treat agents as untrusted: restrict permissions in the agent module when supported.
- Keep prompts explicit: inputs, repo, constraints, and “done when” criteria.

## Troubleshooting

- Need the backing workspace: `coder task status <task> -o json` (look for `workspace_name`/IDs), then use normal workspace commands.
- Task is `error`/unhealthy: start with `coder task logs <task>`.

## References (load as needed)

- Task template snippet + design notes: `references/task-template-snippet.md`
- Tasks API quick reference: `references/api.md`
