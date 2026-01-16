# Tools Reference

URL: https://www.greptile.com/docs/mcp-v2/tools

Complete reference for all tools provided by the Greptile MCP server.

Repository parameters (`name`, `remote`, `defaultBranch`) must be provided together or omitted entirely.

## Pull Request Tools

### list\_pull\_requests / list\_merge\_requests

List PRs with optional filtering. Both tool names work identically.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | No\* | Repository name (`owner/repo`) |
| `remote` | string | No\* | `github`, `gitlab`, `azure`, `bitbucket` |
| `defaultBranch` | string | No\* | Default branch name |
| `sourceBranch` | string | No | Filter by source branch (partial match) |
| `authorLogin` | string | No | Filter by author (fuzzy match) |
| `state` | string | No | `open`, `closed` |
| `limit` | number | No | Max results (default: 20, max: 100) |
| `offset` | number | No | Pagination offset |

Merged PRs also appear under `state: "closed"`.

```
{
"mergeRequests": [
{
"id": "15384680",
"number": 5,
"title": "Fix config test logic",
"state": "open",
"isDraft": false,
"authorLogin": "developer",
"branches": {
"source": "fix-config-test",
"target": "develop"
},
"repository": {
"name": "owner/repo",
"remote": "github"
},
"stats": {
"changedFiles": 2,
"additions": 10,
"deletions": 1
},
"commentsCount": 2,
"reviewsCount": 1,
"createdAt": "2025-11-15T21:22:04.000Z"
}
],
"total": 4
}
```

---

### get\_merge\_request

Get detailed PR information including review analysis.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | **Yes** | Repository name (`owner/repo`) |
| `remote` | string | **Yes** | `github`, `gitlab`, `azure`, `bitbucket` |
| `defaultBranch` | string | **Yes** | Default branch |
| `prNumber` | number | **Yes** | PR number |

```
{
"mergeRequest": {
"number": 5,
"title": "Fix config test logic",
"description": "Fixes the configuration issue.",
"state": "open",
"isDraft": false,
"authorLogin": "developer",
"branches": {
"source": "fix-config-test",
"target": "develop"
},
"stats": {
"changedFiles": 2,
"additions": 10,
"deletions": 1
},
"labels": [],
"comments": {
"greptile": [...],
"human": [...]
},
"codeReviews": [
{
"id": "1382118",
"status": "COMPLETED",
"createdAt": "2025-11-15T21:22:08.333Z",
"completedAt": "2025-11-15T21:24:33.848Z"
}
],
"reviewAnalysis": {
"totalGreptileComments": 2,
"totalHumanComments": 0,
"addressedComments": [],
"unaddressedComments": [...],
"commitsSinceLastReview": [],
"lastReviewDate": "2025-11-15T21:24:33.643Z",
"reviewCompleteness": "0/2 Greptile comments addressed",
"hasNewCommitsSinceReview": false
}
}
}
```

**Key fields:**

* `comments.greptile[]` - Greptile-generated comments
* `comments.human[]` - Human comments
* `reviewAnalysis.reviewCompleteness` - Human-readable progress
* `reviewAnalysis.hasNewCommitsSinceReview` - Needs re-review?

---

### list\_merge\_request\_comments

Get all comments for a PR with filtering options.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | **Yes** | Repository name |
| `remote` | string | **Yes** | Provider |
| `defaultBranch` | string | **Yes** | Default branch |
| `prNumber` | number | **Yes** | PR number |
| `greptileGenerated` | boolean | No | Filter Greptile comments only |
| `addressed` | boolean | No | Filter by addressed status |
| `createdAfter` | string | No | ISO 8601 date filter |
| `createdBefore` | string | No | ISO 8601 date filter |

```
{
"comments": [
{
"id": "152718338",
"commentId": "IC_kwDOQI_wgM7S0QWt",
"body": "<h2>Greptile Overview</h2>...",
"authorLogin": "greptile-apps[bot]",
"filePath": null,
"lineStart": null,
"lineEnd": null,
"isGreptileComment": true,
"addressed": false,
"createdAt": "2025-11-15T21:24:33.643Z",
"hasSuggestion": false,
"suggestedCode": null,
"linkedMemory": null
},
{
"id": "152718337",
"commentId": "PRRC_kwDOQI_wgM6Wzw2_",
"body": "**logic:** API token exposed...\n\n```suggestion\n\"Authorization\": \"Bearer ${process.env.TOKEN}\"\n```",
"authorLogin": "greptile-apps",
"filePath": ".mcp.json",
"lineStart": null,
"lineEnd": null,
"isGreptileComment": true,
"addressed": false,
"createdAt": "2025-11-15T21:24:33.623Z",
"hasSuggestion": true,
"suggestedCode": "\"Authorization\": \"Bearer ${process.env.TOKEN}\"",
"linkedMemory": null
}
],
"repository": "owner/repo",
"prNumber": 5,
"total": 2
}
```

**Key fields:**

* `isGreptileComment` - Boolean: is this from Greptile?
* `hasSuggestion` - Boolean: has a code fix?
* `suggestedCode` - The actual fix code
* `linkedMemory` - Links to custom context (usually null)

**Two Greptile identities:** PR summaries come from `greptile-apps[bot]`, inline comments from `greptile-apps`. Use `isGreptileComment: true` to catch both.

---

## Code Review Tools

### list\_code\_reviews

List code reviews with optional filtering.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | No | Repository name |
| `remote` | string | No | Provider |
| `defaultBranch` | string | No | Default branch |
| `prNumber` | number | No | Filter by PR |
| `status` | string | No | Filter by status |
| `limit` | number | No | Max results (default: 20) |
| `offset` | number | No | Pagination offset |

**Status values:** `PENDING`, `REVIEWING_FILES`, `GENERATING_SUMMARY`, `COMPLETED`, `FAILED`, `SKIPPED`

```
{
"codeReviews": [
{
"id": "1382118",
"status": "COMPLETED",
"createdAt": "2025-11-15T21:22:08.333Z",
"completedAt": "2025-11-15T21:24:33.848Z",
"metadata": {
"strictness": 2,
"totalFiles": 2,
"correlationId": "6ab3bbc7-141a-4403-978d-1152501bf9be",
"completedFiles": 2
},
"mergeRequest": {
"id": "15384680",
"prNumber": 5,
"title": "Fix config test logic",
"sourceRepoUrl": "https://github.com/owner/repo",
"repository": {
"name": "owner/repo"
}
}
}
],
"total": 10
}
```

**Key fields:**

* `metadata.strictness` - Review strictness level (1-5)
* `metadata.totalFiles` / `completedFiles` - Review progress

---

### get\_code\_review

Get detailed information for a specific code review.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `codeReviewId` | string | **Yes** | Code review ID |

```
{
"codeReview": {
"id": "1382118",
"body": "<sub>2 files reviewed, 1 comment</sub>...",
"status": "COMPLETED",
"createdAt": "2025-11-15T21:22:08.333Z",
"completedAt": "2025-11-15T21:24:33.848Z",
"metadata": {
"strictness": 2,
"totalFiles": 2,
"correlationId": "6ab3bbc7-141a-4403-978d-1152501bf9be",
"completedFiles": 2
},
"mergeRequest": {
"id": "15384680",
"prNumber": 5,
"title": "Fix config test logic",
"sourceRepoUrl": "https://github.com/owner/repo",
"description": "Fixes the configuration issue.",
"authorLogin": "developer",
"repository": {
"id": "557313",
"name": "owner/repo",
"remote": "github"
}
}
}
}
```

---

### trigger\_code\_review

Start a new code review on a PR.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | **Yes** | Repository name |
| `remote` | string | **Yes** | Provider |
| `defaultBranch` | string | **Yes** | Default branch |
| `prNumber` | number | **Yes** | PR number |
| `branch` | string | No | Working branch |

`defaultBranch` is **required** despite appearing optional. Omitting it returns: `MCP error -32000: invalid_type - defaultBranch Required`

```
{
"codeReviewId": "cr_abc123xyz",
"status": "PENDING",
"message": "Code review triggered successfully"
}
```

---

## Comment Search Tool

### search\_greptile\_comments

Search across all Greptile comments.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | string | **Yes** | Search term |
| `limit` | number | No | Max results (default: 10, max: 50) |
| `includeAddressed` | boolean | No | Include resolved comments (default: false) |
| `createdAfter` | string | No | ISO 8601 date filter |

```
{
"comments": [
{
"id": "152718338",
"commentId": "IC_kwDOQI_wgM7S0QWt",
"body": "**Critical Security Issue:** ...",
"authorLogin": "greptile-apps[bot]",
"sourceType": "greptile",
"isGreptileComment": true,
"filePath": null,
"lineStart": null,
"lineEnd": null,
"addressed": false,
"hasSuggestion": false,
"suggestedCode": null,
"createdAt": "2025-11-15T21:24:33.643Z",
"mergeRequest": {
"id": "15384680",
"prNumber": 5,
"title": "Fix config test logic",
"sourceRepoUrl": "https://github.com/owner/repo",
"repository": {
"name": "owner/repo"
}
},
"linkedMemory": null
}
],
"query": "security",
"total": 4,
"note": "All results are Greptile review comments",
"summary": {
"addressed": 0,
"unaddressed": 4,
"withSuggestions": 1
}
}
```

**Key fields:**

* `summary.withSuggestions` - Count of comments with fixes
* `mergeRequest` - PR context for each comment

---

## Custom Context Tools

### list\_custom\_context

List your organizations coding patterns.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | No | `CUSTOM_INSTRUCTION` or `PATTERN` |
| `greptileGenerated` | boolean | No | Filter by source |
| `limit` | number | No | Max results (default: 20, max: 100) |
| `offset` | number | No | Pagination offset |

```
{
"customContexts": [
{
"id": "9c29e7ed-2d3f-45bd-846d-a61a59f10dd9",
"type": "CUSTOM_INSTRUCTION",
"body": "Use async/await over promises",
"status": "ACTIVE",
"scopes": {
"OR": [
{
"field": "repository",
"value": "owner/repo",
"operator": "MATCHES"
}
]
},
"metadata": {
"subtype": "style_guide",
"includeUris": [...]
},
"evidenceCount": 0,
"commentsCount": 0,
"createdAt": "2025-11-04T07:26:36.339Z"
}
],
"total": 2
}
```

**Scope formats:**

* `{}` - Universal (applies everywhere)
* `{"AND": [...]}` - All conditions must match
* `{"OR": [...]}` - Any condition matches

---

### get\_custom\_context

Get details for a specific pattern.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `customContextId` | string | **Yes** | UUID of the context |

```
{
"customContext": {
"id": "9c29e7ed-2d3f-45bd-846d-a61a59f10dd9",
"type": "CUSTOM_INSTRUCTION",
"body": "Use async/await over promises",
"status": "ACTIVE",
"metadata": {
"subtype": "style_guide",
"includeUris": [...]
},
"scopes": {},
"createdAt": "2025-11-04T07:26:36.339Z",
"linkedComments": []
}
}
```

---

### search\_custom\_context

Search patterns by content.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | string | **Yes** | Search term |
| `limit` | number | No | Max results (default: 10, max: 50) |

```
{
"customContexts": [...],
"query": "async await",
"total": 0
}
```

---

### create\_custom\_context

Create a new coding pattern.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `body` | string | No | Pattern content |
| `type` | string | No | `CUSTOM_INSTRUCTION` or `PATTERN` |
| `status` | string | No | `ACTIVE`, `INACTIVE`, `SUGGESTED` |
| `scopes` | object | No | Where pattern applies |
| `metadata` | object | No | Additional data |

**Scope structure:**

```
{
"AND": [
{
"operator": "MATCHES",
"field": "filepath",
"value": "**/api/** "
}
]
}
```

```
{
"customContext": {
"id": "8849b548-82ad-498a-b239-e854b5dd9e2b",
"type": "CUSTOM_INSTRUCTION",
"body": "Test custom context",
"scopes": {"AND": []},
"status": "INACTIVE",
"metadata": {},
"createdAt": "2025-11-29T09:01:03.755Z"
}
}
```

Theres no `delete_custom_context` tool. To disable a pattern, set `status: "INACTIVE"`.

---

## Error Handling

Standard JSON-RPC error format:

```
{
"jsonrpc": "2.0",
"id": 1,
"error": {
"code": -32601,
"message": "Method not found"
}
}
```

**Common Error Codes:**

| Code | Meaning |
| --- | --- |
| `-32700` | Parse error |
| `-32600` | Invalid request |
| `-32601` | Method not found |
| `-32602` | Invalid parameters |
| `-32603` | Internal error |
| `-32000` | Server error (includes auth failures) |

---
