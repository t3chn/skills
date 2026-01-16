# Auto-Fix Workflow

URL: https://www.greptile.com/docs/mcp-v2/auto-fix

Use Greptile MCP tools to fetch unaddressed comments and apply fixes directly from your IDE.

## Your First Auto-Fix

Fetch unaddressed comments

Ask your AI assistant:

List unaddressed Greptile comments for PR #5 in owner/repo

The assistant calls `list_merge_request_comments` with `addressed: false`.

Review the response

comments with their details including file path, issue type, and whether a fix is available.

Apply fixes

For comments with `hasSuggestion: true`:

Apply the suggested fix for the API token issue

The assistant applies the `suggestedCode` to your file.

Accept changes

Review the changes, then click **Keep All** to apply them to your codebase.

Commit changes

After applying fixes, commit your changes. Greptile automatically marks comments as addressed when the file is modified.

---

## Understanding Comment Fields

When you fetch comments, each one includes these key fields:

| Field | Type | Description |
| --- | --- | --- |
| `isGreptileComment` | boolean | `true` if from Greptile |
| `addressed` | boolean | `true` if resolved by subsequent commit |
| `hasSuggestion` | boolean | `true` if includes a code fix |
| `suggestedCode` | string | The actual fix (when `hasSuggestion` is true) |
| `filePath` | string | File location (null for PR-level comments) |
| `lineStart` / `lineEnd` | number | Line range (null for general comments) |
| `linkedMemory` | object | Custom context that triggered this comment |

### How Comments Get Addressed

A comment becomes addressed when theres a **commit after the comment** that modifies the relevant file:

1. Greptile comments on src/auth.ts
2. Developer pushes commit touching src/auth.ts
3. Comment marked as addressed: true

Check progress via `reviewAnalysis.reviewCompleteness` (e.g., 2/5 Greptile comments addressed).

---

## Common Prompts

Get all comments with fixes

List all Greptile comments on PR #5 that have suggested code fixes

The assistant filters for `hasSuggestion: true`.

Fix style issues only

Find Greptile comments about style or formatting and apply the fixes

Searches comment bodies for style-related keywords.

Check if PR is ready to merge

What's the review status for PR #5? Are there any unaddressed critical issues?

Uses `get_merge_request` and checks `reviewAnalysis.reviewCompleteness`.

Get comments for specific file

Show Greptile comments for src/auth/login.ts

Filters results by `filePath`.

See what custom context triggered a comment

Why did Greptile flag this issue? Show the linked coding pattern.

Checks the `linkedMemory` field for the associated custom context.

---

## Next Steps
