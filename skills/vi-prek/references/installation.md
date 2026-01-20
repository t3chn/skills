# Installation, Updates, Completions

Use this when a user asks how to install/upgrade prek locally or in CI images.

## Run via `uvx` (preferred)

Run all prek commands as `uvx prek ...` (no separate prek installation required).

Verify:

```bash
uvx prek --version
```

## Update

When using `uvx`, updates are handled by uv/tool caching; re-running `uvx prek ...` will use the cached tool (or a newer one, depending on your uv settings).

## Shell completions

Install completions by printing them from prek.

- Bash:

```bash
COMPLETE=bash uvx prek > /etc/bash_completion.d/prek
```

- Zsh:

```bash
COMPLETE=zsh uvx prek > "${fpath[1]}/_prek"
```

- Fish:

```bash
COMPLETE=fish uvx prek > ~/.config/fish/completions/prek.fish
```

- PowerShell:

```powershell
COMPLETE=powershell uvx prek >> $PROFILE
```
