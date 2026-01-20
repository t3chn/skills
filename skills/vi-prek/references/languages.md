# Language support (Hook runtimes)

Use this when a hook fails to install/run due to toolchain/runtime issues, or when defining `repo: local` hooks.

## What `language` controls

Each hook has a `language` that tells prek how to install and run it:

- Whether prek creates a managed environment
- How `additional_dependencies` are installed
- How toolchain versions are resolved (`language_version`)
- How `entry` is executed

For `repo: local` hooks, `language` is required.

## Toolchains and `language_version`

prek resolves toolchains by:

1. Discovering system toolchains (PATH and common version manager locations)
2. Downloading a toolchain when supported and needed

Key values:

- `language_version: system` → never download; require system toolchain
- `language_version: default` → use language defaults (may download)

prek parses `language_version` as a version request; some languages accept semver ranges.

Languages with managed toolchain downloads:

- Python
- Node
- Go
- Rust

## Python specifics (prek behavior)

- prek installs Python hook repos using `uv pip install` and runs installed console scripts.
- prek may auto-install `uv` and required Python versions.
- `UV_*` environment variables can affect hook dependency resolution; check them when installs behave oddly.

## Docker hook languages

- `language: docker` builds a Dockerfile from the hook repo and runs inside the container.
- `language: docker_image` runs an existing image.

prek auto-detects the container runtime (Docker/Podman/Apple Container) and can be overridden with `PREK_CONTAINER_RUNTIME`.
