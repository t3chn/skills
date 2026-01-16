# Anatomy of a Review

URL: https://www.greptile.com/docs/code-review/first-pr-review

This page breaks down every component of a Greptile review so you know exactly what to expect and how to interpret the feedback.

## The Review Process

When you open a PR, Greptile:

1. **Detects the PR** and starts analyzing
2. **Builds context** from your entire codebase, not just the diff
3. **Posts feedback** as a PR summary + inline comments

| Status | Emoji | Typical Duration |
| --- | --- | --- |
| Analyzing | ~3 minutes |
| Complete | - |
| Failed | Tag `@greptileai` to retry |

---

## PR Summary

The PR summary is a top-level comment that gives you the big picture.

### Components

#### Summary

Plain-language explanation of what the PR does, who it affects, and why. Includes major improvements and any issues found.

#### Confidence Score

A 0-5 rating that tells you at a glance whether the PR is ready to merge. Greptile calculates this based on the severity and quantity of issues found, the complexity of changes, and how well the code aligns with your codebase patterns.

| Score | Meaning | Action |
| --- | --- | --- |
| **5/5** | Production ready | Merge |
| **4/5** | Minor polish needed | Merge after small fixes |
| **3/5** | Implementation issues | Address feedback first |
| **2/5** | Significant bugs | Needs rework |
| **0-1/5** | Critical problems | Major rethink needed |

Scores are contextual. A 3/5 on a payments feature is more serious than a 3/5 on an internal script.

#### Files Changed & Issues

File-by-file breakdown showing what changed and issues found per file.

#### Sequence Diagram

Visual flow showing how changes interact. Useful for complex PRs with multiple services.

```
Configure which components appear in your [dashboard](https://app.greptile.com):
```

---

## Inline Comments

Greptile posts comments directly on specific lines where it finds issues.

### Comment Types

| Type | What it catches | Examples |
| --- | --- | --- |
| **Logic** | Bugs, incorrect behavior, edge cases | Null pointer, race condition, wrong return value |
| **Syntax** | Code that wont compile/run | Missing import, typo, invalid syntax |
| **Style** | Code quality, best practices | Naming conventions, dead code, complexity |

### Suggested Fixes

Most comments include a code suggestion you can apply:

```
const data = fetchData()
+ const data = await fetchData()
```

---

## Troubleshooting

Review didn't appear

**Check:**

* Repository enabled in dashboard
* Not a draft PR (skipped by default)
* Branch not excluded by filters
* Indexing complete (first time: ~1-2 hours)

**Fix:** Comment `@greptileai` to trigger manually

---

## Whats Next

Now that you understand what a review looks like, learn how to interact with Greptile:
