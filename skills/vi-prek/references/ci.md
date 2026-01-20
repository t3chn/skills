# CI / Containers

Use this when wiring prek into CI (especially GitHub Actions) or container images.

## GitHub Actions (minimal)

Install `uv`, then run prek via `uvx`:

```yaml
name: Prek checks
on: [push, pull_request]

jobs:
  prek:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: astral-sh/setup-uv@v7
      - run: uvx prek run --all-files
```

## Docker

prek ships a distroless image:

- `ghcr.io/j178/prek`

The binary is located at `/prek`. A common pattern is copying it into your own image:

```dockerfile
FROM debian:bookworm-slim
COPY --from=ghcr.io/j178/prek:<tag> /prek /usr/local/bin/prek
```

Or run the image directly:

```bash
docker run --rm ghcr.io/j178/prek:<tag> --version
```

Pin `<tag>` in CI for reproducible builds.
