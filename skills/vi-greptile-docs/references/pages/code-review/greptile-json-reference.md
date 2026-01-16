# greptile.json Reference

URL: https://www.greptile.com/docs/code-review/greptile-json-reference

Complete configuration reference for `greptile.json`. All parameters are optional.

Place `greptile.json` in your repository root. Settings are read from the source branch of the PR and override dashboard settings.

## Review Behavior

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `strictness` | number | `2` | Severity threshold. Must be `1`, `2`, or `3` |
| `commentTypes` | array | `["logic", "syntax", "style", "info"]` | Comment types to provide. Options: `logic`, `syntax`, `style`, `info` |
| `triggerOnUpdates` | boolean | `false` | Review every commit to the PR, not just when opened |
| `skipReview` | string | - | Set to `"AUTOMATIC"` to skip auto-reviews but allow manual triggers |
| `model` | string | - | Specify which AI model to use for reviews |

## PR Filters

Control which PRs get reviewed:

| Parameter | Type | Description |
| --- | --- | --- |
| `labels` | array | Review only PRs with these labels |
| `disabledLabels` | array | Skip PRs with these labels |
```
| `includeAuthors` | array | Review only PRs from these authors. Empty = all authors (except excluded) |
```
| `excludeAuthors` | array | Never review PRs from these authors |
```
| `includeBranches` | array | Review only PRs to these branches. Empty = all branches (except excluded) |
```
| `excludeBranches` | array | Never review PRs to these branches |
| `includeKeywords` | string | Newline-separated keywords. Review only PRs with these in title/description |
| `ignoreKeywords` | string | Newline-separated keywords. Skip PRs with these in title/description |
| `fileChangeLimit` | number | Skip PRs with more than this many changed files (minimum: 1) |

## File Patterns

| Parameter | Type | Description |
| --- | --- | --- |
| `ignorePatterns` | string | Newline-separated file patterns to skip (follows `.gitignore` syntax) |

**Example:**

```
{
"ignorePatterns": "**/*.generated.*\ndist/**\nnode_modules/** "
}
```

## Custom Context

| Parameter | Type | Description |
| --- | --- | --- |
| `instructions` | string | Natural language instructions for code reviews |
| `customContext` | object | Advanced context with `rules`, `files`, and `other` arrays |
| `patternRepositories` | array | Related repos to reference (format: `org/repo`) |

**customContext structure:**

```
{
"customContext": {
"rules": [
{
"rule": "Use async/await instead of callbacks",
"scope": ["src/**/*.ts"]
}
],
"files": [
{
"path": "docs/style-guide.md",
"description": "Company style guide",
"scope": ["src/**"]
}
],
"other": [
{
"content": "This is a legacy codebase - be cautious with changes",
"scope": ["legacy/**"]
}
]
}
}
```

## Review Output

Control how reviews appear:

| Parameter | Type | Description |
| --- | --- | --- |
| `comment` | string | Disclaimer/prefix added to every PR summary |
| `shouldUpdateDescription` | boolean | If `true`, updates PR description. If `false`, posts as review comment |
| `updateExistingSummaryComment` | boolean | Update existing review comment instead of creating new one |
| `updateSummaryOnly` | boolean | Only update summary, dont post individual inline comments |
| `fixWithAI` | boolean | Add AI fix prompts to help AI tools understand fixes |
| `hideFooter` | boolean | Hide Greptile footer from review comments |

### Review Components

Control visibility of individual review components:

| Parameter | Type | Description |
| --- | --- | --- |
| `includeIssuesTable` | boolean | Include issues table in review |
| `includeConfidenceScore` | boolean | Include confidence scores in review |
| `includeSequenceDiagram` | boolean | Include sequence diagrams in review |

### Review Sections

Fine-grained control over section visibility and behavior:

| Parameter | Type | Properties |
| --- | --- | --- |
| `summarySection` | object | `included` (boolean), `collapsible` (boolean), `defaultOpen` (boolean) |
| `issuesTableSection` | object | `included` (boolean), `collapsible` (boolean), `defaultOpen` (boolean) |
| `confidenceScoreSection` | object | `included` (boolean), `collapsible` (boolean), `defaultOpen` (boolean) |
| `sequenceDiagramSection` | object | `included` (boolean), `collapsible` (boolean), `defaultOpen` (boolean) |

**Example:**

```
{
"summarySection": {
"included": true,
"collapsible": true,
"defaultOpen": false
}
}
```

## GitHub-Specific

| Parameter | Type | Description |
| --- | --- | --- |
| `statusCheck` | boolean | Create GitHub status check for each review |
| `statusCommentsEnabled` | boolean | Enable status comments on PRs |

## Complete Example

greptile.json

```
{
"strictness": 2,
"commentTypes": ["logic", "syntax"],
"model": "gpt-4",
"instructions": "Focus on security and maintainability",
"ignorePatterns": "**/*.generated.*\ndist/**\n*.md",
"patternRepositories": ["acme/shared-utils"],
"triggerOnUpdates": false,
"fileChangeLimit": 100,
"includeAuthors": [],
"excludeAuthors": ["dependabot[bot]"],
"includeBranches": ["main", "develop"],
"excludeBranches": ["draft/**"],
"customContext": {
"rules": [
{
"rule": "All API endpoints must have rate limiting",
"scope": ["src/api/**/*.ts"]
}
],
"files": [
{
"path": "docs/architecture.md",
"description": "System architecture"
}
]
},
"shouldUpdateDescription": false,
"updateExistingSummaryComment": true,
"statusCheck": true,
"includeConfidenceScore": true,
"summarySection": {
"included": true,
"collapsible": false,
"defaultOpen": true
}
}
```

## Parameter Reference by Category

All parameters alphabetically

* `comment` - string
* `commentTypes` - array
* `customContext` - object
* `disabledLabels` - array
* `excludeAuthors` - array
* `excludeBranches` - array
* `fileChangeLimit` - number
* `fixWithAI` - boolean
* `hideFooter` - boolean
* `ignoreKeywords` - string
* `ignorePatterns` - string
* `includeAuthors` - array
* `includeBranches` - array
* `includeConfidenceScore` - boolean
* `includeIssuesTable` - boolean
* `includeKeywords` - string
* `includeSequenceDiagram` - boolean
* `instructions` - string
* `labels` - array
* `model` - string
* `patternRepositories` - array
* `shouldUpdateDescription` - boolean
* `skipReview` - string (literal `"AUTOMATIC"`)
* `statusCheck` - boolean
* `statusCommentsEnabled` - boolean
* `strictness` - number (1, 2, or 3)
* `triggerOnUpdates` - boolean
* `updateExistingSummaryComment` - boolean
* `updateSummaryOnly` - boolean
* **Section objects:** `summarySection`, `issuesTableSection`, `confidenceScoreSection`, `sequenceDiagramSection`

## Validation

JSON syntax errors

**Common mistakes:** ** Trailing commas:**

```
{
"strictness": 2,
"commentTypes": ["logic"],
}
```

**No trailing comma:**

```
{
"strictness": 2,
"commentTypes": ["logic"]
}
```

**Validate your JSON:**

`npx jsonlint greptile.json`

Invalid parameter values

**strictness must be 1, 2, or 3:**

```
{
"strictness": 4
}
```

Invalid - only 1, 2, or 3 allowed**commentTypes must be valid:**

```
{
"commentTypes": ["logic", "syntax", "style", "info"]
}
```

Valid options: `logic`, `syntax`, `style`, `info`**skipReview must be exactly AUTOMATIC:**

```
{
"skipReview": "AUTO"
}
```

Invalid - must be `"AUTOMATIC"` exactly

File location

** Correct:** Repository root

your-repo/
greptile.json
src/
package.json

** Wrong:** Subdirectory

your-repo/
src/
greptile.json
package.json

Configuration not taking effect

**Check:**

1. File is in repository root
2. File exists in the source branch of the PR
3. JSON is valid (use jsonlint)
4. Parameter names are spelled correctly
5. Waiting for new PR (changes dont affect existing reviews)

```
Export dashboard settings: Go to [app.greptile.com/review/github](https://app.greptile.com/review/github?tab=config) Click copy/download icon
```

## Configuration Hierarchy

Settings priority (highest to lowest):

1. **greptile.json** in repository root
2. **Dashboard settings** (organization defaults)

Repository-level `greptile.json` always overrides dashboard settings.

## Whats Next
