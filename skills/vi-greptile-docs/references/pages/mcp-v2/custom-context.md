# Custom Context

URL: https://www.greptile.com/docs/mcp-v2/custom-context

Custom context refers to your teams coding standards that Greptile checks during reviews. Rules like use async/await instead of promises or API endpoints must validate input. When code doesnt follow a pattern, Greptile comments on the PR.
With MCP, you can view, search, and create patterns from your IDE.

## View Your Patterns

What coding patterns does my organization have?

---

## Search Patterns

Search our coding patterns for error handling

---

## Get Pattern Details

Show details for pattern 9c29e7ed-2d3f-45bd-846d-a61a59f10dd9

Returns the full pattern including `linkedComments`PRs where this pattern triggered feedback.

---

## Create a Pattern

Create a coding pattern: "All React components must have TypeScript interfaces for props"
Apply it to .tsx files only.

### Scope Examples

| You Say | Pattern Applies To |
| --- | --- |
| Apply everywhere | All files in all repos |
| Apply to TypeScript files | `**/*.ts` |
| Apply to the api folder | `**/api/** ` |
| Apply to owner/repo only | That specific repository |

---

## Disable a Pattern

Theres no delete. Set status to inactive:

Disable the pattern about console.log statements

---

## Workflow: Turn Recurring Feedback Into a Pattern

When you notice Greptile making the same comment repeatedly:

Identify the pattern

Search Greptile comments for "error handling"

Find comments that keep appearing across PRs.

Create the custom context

Create a pattern: "All catch blocks must log the error before re-throwing"
Apply to all TypeScript files.

Verify it's active

List my custom contexts and confirm the new pattern is ACTIVE

---

## Field Reference

| Field | Description |
| --- | --- |
| `body` | The rule text |
| `type` | `CUSTOM_INSTRUCTION` (explicit rule) or `PATTERN` (code pattern) |
| `status` | `ACTIVE`, `INACTIVE`, or `SUGGESTED` |
| `commentsCount` | Times this pattern triggered a comment |
| `linkedComments` | PRs where this pattern was applied |

---

## Next Steps
