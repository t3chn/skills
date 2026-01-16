# Custom Standards & Rules

URL: https://www.greptile.com/docs/code-review/custom-standards

Configure Greptile to enforce your teams unique standards, from simple naming conventions to complex architectural patterns. This guide covers all three configuration methods and when to use each.
**After this guide, you can:**

* Create custom rules that catch team-specific issues
* Upload existing style guides for automatic enforcement
* Configure repository-specific standards via `greptile.json`
* Verify rules are actually being applied
* Debug when rules dont work as expected

## Required Permissions

Understand who can configure custom standards:

| Action | Owner | Admin | Member |
| --- | --- | --- | --- |
| View custom context |
| Create/edit dashboard rules |
| Delete dashboard rules |
| Edit greptile.json | Anyone with repository write access |
| View suggested rules |
| Approve suggested rules |
| Delete organization |

Permission issues are common. If you lose edit access, check with your organization Owner.

## Configuration Methods

| Method | Best For | Version Control | Scope |
| --- | --- | --- | --- |
| **Dashboard** | Quick experiments, org-wide defaults | No | All repos or specific ones |
| **greptile.json** | Production standards | Yes | Repository-specific |

Dashboard and greptile.json are **separate systems** . Rules in greptile.json dont appear in dashboard. When both exist, greptile.json takes priority.

## Method 1: Dashboard

The quickest way to add custom rules. Changes apply within 2-3 minutes to new PRs.

Navigate to Custom Context

**Path:** AI Code Review Agent Custom Context

Create Rules

Rules must be specific and measurable:

* Write clean code
* Functions must not exceed 50 lines
* All API responses must include `status` and `timestamp` fields

Define Scope

Use glob patterns to target specific files:

```
src/**/*.ts # All TypeScript in src
**/*.test.{js,ts} # All test files
```

Upload Style Guides (Optional)

Point to existing documentation in your repository:

```
docs/style-guide.md
./CONTRIBUTING.md
```

Supported formats: Markdown, plain text, YAML, JSON

Test

1. Create a test PR with intentional violations
2. Verify Greptile catches them within 2-3 minutes
3. Check Last Applied timestamp updates

## Method 2: greptile.json

The most powerful method - version-controlled, repository-specific configuration.

### Understanding customContext Types

The `customContext` field in greptile.json accepts three arrays:
**1. `rules` - Specific coding standards to enforce**

```
"rules": [
{
"rule": "Use async/await instead of callbacks",
"scope": ["**/*.js", "**/*.ts"] // Optional: limit to specific files
},
{
"rule": "All API endpoints must have rate limiting",
"scope": ["src/api/**"]
}
]
```

**2. `files` - Reference existing documentation**

```
"files": [
{
"path": "docs/style-guide.md", // Path to file in your repo
"description": "Company coding standards", // Optional description
"scope": ["src/**"] // Optional: where to apply this file's rules
}
]
```

**3. `other` - General context and background information**

```
"other": [
{
"content": "This is legacy code from 2018 - be careful with changes",
"scope": ["src/legacy/**"]
},
{
"content": "We're migrating to TypeScript - prefer TS over JS"
}
]
```

Each type supports optional `scope` patterns using glob syntax to target specific files or directories. If no scope is specified, the context applies to all files.

### Complete Configuration Examples

* Custom Rules
* Full Example

```
{
"customContext": {
"rules": [
{
"rule": "Use dependency injection for all services",
"scope": ["src/services/**/*.ts"]
},
{
"rule": "API endpoints must have rate limiting",
"scope": ["**/api/** /*.ts"]
},
{
"rule": "Test files must use .test.ts extension",
"scope": ["src/**/*"]
}
]
}
}
```

```
{
// Review behavior
"strictness": 2,
"commentTypes": ["logic", "syntax", "style", "info"],

// Custom standards
"customContext": {
"rules": [
{
"rule": "No direct database queries in controllers",
"scope": ["src/controllers/**/*.ts"]
}
],
"files": [
{
"path": "docs/architecture.md",
"description": "System architecture guidelines"
}
]
},

// Pattern repositories (cross-repo context)
"patternRepositories": ["company/shared-standards"],

// Ignore patterns (newline-separated string)
"ignorePatterns": "*.generated.*\n**/vendor/** \n**/__snapshots__/** "
}
```

## Verifying Rules Are Active

Many teams report rules not working - heres how to verify:

Check 'Last Applied' Status

**Dashboard Custom Context Rules tab**

Look for Last Applied timestamp:

* Should update within 2-3 minutes of adding rule
* If stuck on Never, repository may not be indexed
* Force refresh: Create PR with `@greptileai review`

Verify Repository Status

**Dashboard Repositories Your Repo**

Test with Simple Rule

Add test rule with obvious violation:

```
{
"rule": "No TODO comments",
"scope": ["**/*.js"]
}
```

Create PR with `// TODO: test` and verify detection.

## Suggested Rules (Auto-Learning)

Greptile automatically suggests rules based on your teams patterns:
**How it works:**

1. After ~10 PRs, Greptile detects consistent patterns
2. You can approve, modify, or ignore suggestions
3. Duplicates may appear (safe to ignore)

Suggested rules may duplicate existing ones. This is a known issue - just mark as ignored.

## Troubleshooting Custom Rules

Rules not being applied

1. **Check Last Applied timestamp** (Dashboard Custom Context)
* If Never: Repository not indexed or rule not triggered
* If old: Rule may be inactive
2. **Verify repository is indexed** (Settings Repositories)
* Status must be Indexed not Indexing or Failed
3. **For greptile.json rules:**
* Validate JSON syntax
* Rules wont show in dashboard (this is expected)
* Takes effect on next PR only
4. **Force trigger:** Comment `@greptileai review this`

Dashboard rules not syncing with greptile.json

This is expected behavior:

* Dashboard and greptile.json are separate systems
* greptile.json rules apply during review but dont show in dashboard
* Dashboard rules dont generate a greptile.json file
* Use one or the other per repository, not both

Pattern syntax errors

**Wrong - comma-separated string:**

```
{
"scope": "**/*.cpp, **/*.hpp"
}
```

**Correct - array of patterns:**

```
{
"scope": ["**/*.cpp", "**/*.hpp"]
}
```

`ignorePatterns` only affects reviews, NOT indexing. Files will still be indexed.

Rules not specific enough

**Bad:** Follow best practices** Good:** Variable names must be camelCase, min 3 characters, no Hungarian notationInclude examples in your rule for best results:

```
{
"rule": "API error responses must include: status (number), message (string), timestamp (ISO 8601), requestId (UUID)",
"scope": ["**/api/** "]
}
```

## Whats Next?
