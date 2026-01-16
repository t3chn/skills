# Reports & Analytics

URL: https://www.greptile.com/docs/mcp-v2/reports

Use MCP tools to generate reports on review activity and track team progress.

## PR Status

Get a quick status check for any PR:

What's the review status for PR #5 in owner/repo?

Response includes:

* `reviewCompleteness`: 2/5 Greptile comments addressed
* `hasNewCommitsSinceReview`: Whether re-review needed
* `addressedComments` / `unaddressedComments`: Full lists

---

## Weekly Summary

Generate a report of open PR status:

Give me a weekly summary of all open PRs with their review status and make a nice visual graph for important stats.

The assistant:

1. Calls `list_pull_requests` with `state: "open"`
2. For each PR, calls `get_merge_request` to get `reviewAnalysis`
3. Compiles: PR number, title, author, age, completeness, unaddressed count

Claude took the MCP data and whipped up a basic webpage to visualize it.

---

## Team Metrics

Comments by repository

How many unaddressed Greptile comments do we have per repository?

Review completion rate

What percentage of Greptile comments have been addressed across all open PRs?

Stale PRs

Which open PRs are older than 7 days and still have unaddressed comments?

Issues with fixes available

How many unaddressed comments have suggested code fixes?

Issues by file

Which files have the most unaddressed Greptile comments?

---

## Code Review History

Recent reviews

Show me the last 10 completed code reviews

Review details

Get details for code review 1382118

Failed reviews

Are there any failed or skipped code reviews?

---

## Next Steps
