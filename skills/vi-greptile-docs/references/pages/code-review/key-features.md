# Key Features

URL: https://www.greptile.com/docs/code-review/key-features

## Full codebase context

Greptile builds a graph of your repository (functions, classes, imports, dependencies) and uses it during reviews to reason about ripple effects beyond the diff.

* Surfaces impacted callers and contracts
* Detects cross-file inconsistencies and missing validations
* References similar patterns already in your codebase

## High-signal findings (not nitpicks)

Focus on issues that matter by default; control verbosity with strictness and comment-type filters.

* Logic, security, performance, architectural issues by default
* Style and syntax can be reduced or disabled
* Per-repository rules with `greptile.json`

## Learns your teams standards

Greptile adapts over time using thumbs up/down and short replies.

* Suppresses suggestions your team routinely ignores
* Reinforces patterns your team prefers
* Auto-discovers custom rules from team discussions

## Auto-resolution from your IDE (MCP)

Resolve Greptile comments without leaving your editor.

* Open files, apply suggested fixes, mark threads resolved
* Works with Cursor, Windsurf, Claude Desktop

## Enterprise-grade deployment

* Cloud (SOC2 Type II), self-hosted Docker/Kubernetes, air-gapped
* SSO/SAML, audit logging, role-based access
* Customer-managed PostgreSQL + pgvector, Redis (self-hosted)

## Configuration you control

Use `greptile.json` for repo-level behavior.

greptile.json

```
{
"strictness": 2,
"commentTypes": ["logic", "syntax", "style", "info"],
"triggerOnUpdates": true,
"ignorePatterns": "**/*.test.js\n**/vendor/** "
}
```
