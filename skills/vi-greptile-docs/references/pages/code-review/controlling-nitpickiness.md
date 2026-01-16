# Controlling Nitpickiness

URL: https://www.greptile.com/docs/code-review/controlling-nitpickiness

With noise control, Greptile limits reviews to high-signal insights, skipping low impact or repetitive feedback.

## Configuration Options Overview

You can **fine-tune** review behavior with these configuration options in the greptile.json file:

| Parameter | Type | Description |
| --- | --- | --- |
| `strictness` | number | Filters comments by importance (1-3 scale) |
| `commentTypes` | array | Categories of feedback to generate |
| `ignorePatterns` | string | Files/folders to skip (newline-separated patterns) |
| `triggerOnUpdates` | boolean | Review on every commit, not just PR open |
| `skipReview` | string | Set to `"AUTOMATIC"` for manual-only reviews |

## Severity Threshold Settings

Control how strict Greptile is about leaving comments with the strictness setting (13).

1. Low (Verbose)

**Comments on everything (low threshold).** Perfect for initial setup or deep reviews where you want every potential issue flagged.

2. Default (Recommended)

**Provides moderate filtering (default).** Balanced approach highlighting real issues while filtering common noise. We recommend starting here.

3. High (Critical)

**Shows only the most critical issues (high threshold).** Ideal for final reviews or teams that want minimal interruption.

### How to Configure

* Dashboard (Quick Testing)
* greptile.json (Production)

Create `greptile.json` at your repository root:

```
{
"strictness": 2
}
```

* `1` = verbose (all issues)
* `2` = balanced (default)
* `3` = critical only

This overrides dashboard settings for this repository.

## Comment Type Filtering

Filter which categories of feedback Greptile provides. All types are **enabled by default** .
**Available comment types:**

* `logic` - Business logic issues, algorithmic problems, potential bugs
* `syntax` - Language-specific best practices, proper usage patterns
* `style` - Code formatting, naming conventions, structural consistency
* `info` - Informational comments about code context and patterns

### How to Configure

* Dashboard
* greptile.json

**Only critical issues:**

```
{
"commentTypes": ["logic"]
}
```

**Code quality without style nitpicks:**

```
{
"commentTypes": ["logic", "syntax"]
}
```

**Everything (default):**

```
{
"commentTypes": ["logic", "syntax", "style", "info"]
}
```

## Ignore Patterns

Exclude files that dont need review to speed up analysis and reduce noise.

```
{
"ignorePatterns": "*.generated.*\n**/*.test.js\n**/node_modules/** \n*.config.js\npackage-lock.json\n*.md"
}
```

**Common patterns to ignore:**

* `*.generated.*` - Generated code
* `**/*.test.js` - Test files
* `**/node_modules/** ` - Dependencies
* `*.config.js` - Config files
* `package-lock.json` - Lock files
* `*.md` - Documentation

**Impact:** Ignoring generated/vendor files can speed up reviews by 30-50% and eliminate irrelevant comments.

`ignorePatterns` will only ignore those files during PR review. Greptile will still index them while indexing your repository, which can lead to other errors. For instance, in the case of large binary files. Reach out to Greptile support.

## Trigger Configuration

Control when Greptile performs reviews. This affects developer workflow and review frequency.

* Dashboard
* greptile.json

**Review on every commit:**

```
{
"triggerOnUpdates": true
}
```

**Manual trigger only (skip automatic reviews):**

```
{
"skipReview": "AUTOMATIC"
}
```

* `triggerOnUpdates` - When `true`, reviews on each push (not just PR open)
* `skipReview: "AUTOMATIC"` - Skips automatic reviews, only triggers via `@greptileai`

By default, Greptile reviews when PRs open. Use `triggerOnUpdates` for continuous review on each commit.

Start with dashboard defaults, then add `greptile.json` to repos that need custom settings.

## Troubleshooting

Settings not taking effect

**Check these in order:**

1. If using `greptile.json`, did you commit and push it?
2. Are you looking at a new PR? Settings dont affect existing reviews
3. Wait 2-3 minutes - config changes arent always instant

**Dashboard settings not working?**

* Check if the repo has a `greptile.json` (it overrides dashboard)
* Verify you saved the settings (look for confirmation message)

Still too many comments with strictness: 3

**Progressive solutions:**

1. Reduce comment types to `["logic"]` only
2. Add more ignore patterns for generated/test files
3. Consider `skipReview: "AUTOMATIC"` for non-critical repos
4. Give the learning system 2-3 weeks to adapt to your reactions

Missing important issues

**Check these settings:**

1. Is strictness too high? Try reducing by 1
2. Are all comment types enabled that you need?
3. Check ignore patterns - are they too broad?
4. Has the team been giving to important catches?

Different teams want different settings

**Best practice:**

1. Set conservative org defaults in dashboard (strictness: 2, all types)
2. Let teams create repository-specific `greptile.json` files
3. Share successful configurations as templates
4. Review settings quarterly as teams evolve

**Note:** You cannot prevent teams from creating `greptile.json` - embrace it as customization.

Excluded authors still getting reviewed

**In Dashboard:**
Go to `Settings Review Triggers Excluded Authors` and add:

* `dependabot[bot]`
* `renovate[bot]`
* Any other bot accounts

**Note:** This is dashboard-only, not available in greptile.json

Reviews triggering on disabled/release branches

**Solutions:**

1. Add release branches to excluded branches in dashboard
2. Use `greptile.json` with branch-specific rules
3. Set `skipReview: "AUTOMATIC"` for release repos

## Whats next?
