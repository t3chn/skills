# FastMCP Cloud Deployment Guide

## Overview

FastMCP Cloud is a managed deployment platform for MCP servers. Currently **free during beta**. Supports FastMCP 2.0 and FastMCP 1.0 servers.

**URL format:** `https://your-project-name.fastmcp.app/mcp`

## Prerequisites

- GitHub account
- Repository with FastMCP server
- Python file with `FastMCP` server object
- Optional: `requirements.txt` or `pyproject.toml`

Verify compatibility:
```bash
fastmcp inspect server.py:mcp
```

## Deployment Steps

### 1. Create Project

1. Go to [fastmcp.cloud](https://fastmcp.cloud)
2. Authenticate with GitHub
3. Create new project:
   - **Name**: generates URL (`name.fastmcp.app`)
   - **Entrypoint**: `server.py` or `server.py:mcp`
   - **Authentication**: toggle for org-only access

### 2. Deploy

Platform automatically:
- Clones repository
- Installs dependencies from `requirements.txt` / `pyproject.toml`
- Builds and deploys

**Continuous deployment:** Auto-deploys on push to `main`. PRs get unique preview URLs.

### 3. Connect

Server available at:
```
https://your-project-name.fastmcp.app/mcp
```

## Project Structure

```
my-mcp-server/
├── server.py           # FastMCP server (entrypoint)
├── requirements.txt    # or pyproject.toml
└── .env.example        # Document required env vars
```

## Server File Requirements

```python
from fastmcp import FastMCP

# Server object (referenced in entrypoint)
mcp = FastMCP("my_service")

@mcp.tool
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"

# This block is IGNORED by FastMCP Cloud
if __name__ == "__main__":
    mcp.run()
```

**Important:** The `if __name__ == "__main__"` block is ignored. FastMCP Cloud manages server lifecycle.

## Environment Variables

Set secrets in FastMCP Cloud dashboard, not in code:

```python
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

## Authentication Options

### No Auth (Public)
Anyone can connect to your server.

### Organization Auth
Toggle in dashboard — restricts to GitHub org members.

### Custom Auth (FastMCP 2.0)

```python
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider

auth = BearerAuthProvider(
    token_verifier=lambda token: verify_token(token)
)

mcp = FastMCP("my_service", auth=auth)
```

## Dependencies

**requirements.txt:**
```
fastmcp>=2.0.0
httpx>=0.27.0
pydantic>=2.0.0
```

**pyproject.toml:**
```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
dependencies = [
    "fastmcp>=2.0.0",
    "httpx>=0.27.0",
]
```

## Testing Locally

```bash
# Install FastMCP CLI
pip install fastmcp

# Run server locally
fastmcp dev server.py:mcp

# Inspect server
fastmcp inspect server.py:mcp
```

## Connecting from Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-service": {
      "url": "https://my-project.fastmcp.app/mcp"
    }
  }
}
```

## Connecting from Claude Code

```bash
claude mcp add my-service https://my-project.fastmcp.app/mcp
```

## Best Practices

1. **Keep server lightweight** — avoid heavy dependencies
2. **Use environment variables** for secrets
3. **Handle errors gracefully** — cloud logs errors
4. **Test locally first** with `fastmcp dev`
5. **Document env vars** in `.env.example`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check `requirements.txt` syntax |
| Import errors | Ensure all dependencies listed |
| Auth fails | Verify GitHub org membership |
| Timeout | Optimize slow operations |

## Limitations

- Serverless — no persistent state between requests
- Cold starts possible for idle servers
- Memory/CPU limits apply (generous during beta)
