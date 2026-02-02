# Task template snippet (Terraform)

Coder Tasks run inside Coder Workspaces. A template is **Tasks-capable** if it includes:

- `data "coder_task" "me" {}` (task context, including `prompt`)
- `resource "coder_ai_task" ...` (links a workspace app to the Task UI)
- An agent module (Codex CLI, Claude Code, etc.) that runs in the workspace and consumes `data.coder_task.me.prompt`

## Minimal pattern (agent module placeholder)

```hcl
terraform {
  required_providers {
    coder = {
      source  = "coder/coder"
      version = ">= 2.13"
    }
  }
}

data "coder_task" "me" {}

# You still need your normal workspace resources:
# - compute/container/VM/etc.
# - a `coder_agent` that your module connects to
# - a `coder_app` that will host the agent chat UI (provided by agent modules)

resource "coder_agent" "agent" {
  # ...
}

module "agent" {
  # Pick a Tasks-capable agent module from the Coder Registry:
  # - Claude Code: registry.coder.com/coder/claude-code
  # - Codex CLI:   registry.coder.com/coder-labs/codex
  #
  # Module should expose a `task_app_id` output.
  source   = "registry.coder.com/<org>/<module>/coder"
  version  = "<pin>"
  agent_id = coder_agent.agent.id
  workdir  = "/home/coder/project"

  ai_prompt = data.coder_task.me.prompt
}

resource "coder_ai_task" "task" {
  app_id = module.agent.task_app_id
}
```

## Hybrid vs Tasks-only templates

- **Tasks-only template**: keep it simple. Expect every workspace to be created as a Task.
- **Hybrid template** (usable as a normal workspace + as a Task): gate agent/task resources with `data.coder_task.me.enabled` so humans don’t accidentally run the agent.

## Presets (important)

Tasks don’t expose template parameters at runtime. If users need choices (compute size, region, toolchain),
encode them as **workspace presets** in the template.
