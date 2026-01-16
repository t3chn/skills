# Greptile (Reference)

Source: `/Users/vi/projects/skills/greptile/README.md`

## Setup

1. Create a Greptile account and connect GitHub or GitLab repos.
2. Generate an API key at `https://app.greptile.com/settings/api`.
3. Set the environment variable in your shell profile:

```bash
export GREPTILE_API_KEY="your-api-key-here"
```

Reload your shell (for example, `source ~/.zshrc`).

## Available tools

### Pull request tools

- `list_pull_requests` - List PRs with optional filtering by repo, branch, author, or state
- `get_merge_request` - Get detailed PR info including review analysis
- `list_merge_request_comments` - Get all comments on a PR with filtering options

### Code review tools

- `list_code_reviews` - List code reviews with optional filtering
- `get_code_review` - Get detailed code review information
- `trigger_code_review` - Start a new Greptile review on a PR

### Comment search

- `search_greptile_comments` - Search across all Greptile review comments

### Custom context tools

- `list_custom_context` - List your organization's coding patterns and rules
- `get_custom_context` - Get details for a specific pattern
- `search_custom_context` - Search patterns by content
- `create_custom_context` - Create a new coding pattern

## Example prompts

- "Show me Greptile's comments on my current PR and help me resolve them"
- "What issues did Greptile find on PR #123?"
- "Trigger a Greptile review on this branch"
