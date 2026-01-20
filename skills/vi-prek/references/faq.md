# FAQ / Common Confusions

## What does `prek install --install-hooks` do?

It combines two actions:

1. **Install git hooks**: write the git hook shim under `.git/hooks/` so `git commit` invokes prek.
2. **Prepare prek-managed hook environments**: proactively create the environments/caches needed by the hooks declared in `.pre-commit-config.yaml`.

Use `prek install` if you only want to wire the git hook.
Use `prek install --install-hooks` if you also want to warm caches/envs ahead of time (useful in CI images or first-time setup).

When running via `uvx`, the command is the same with a prefix:

- `uvx prek install`
- `uvx prek install --install-hooks`
