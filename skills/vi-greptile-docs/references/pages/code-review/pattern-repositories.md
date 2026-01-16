# Pattern Repositories

URL: https://www.greptile.com/docs/code-review/pattern-repositories

Pattern repositories let Greptile reference related codebases when reviewing your code. Use this for shared libraries, API documentation, or microservices that interact with the repository under review.

## Configuration

Add the `patternRepositories` array to your `greptile.json`:

greptile.json

```
{
"patternRepositories": [
"your-org/shared-library",
"your-org/api-documentation"
]
}
```

**Requirements:**

* Use `org/repo` format for GitHub or `group/project` for GitLab
* Repositories must be accessible by your GitHub/GitLab integration
* Pattern repos are indexed automatically

## Examples

* Frontend Backend
* Shared Libraries

**Frontends `greptile.json`:**

```
{
"patternRepositories": ["acme/backend-api"],
"customContext": {
"rules": [{
"rule": "API calls must match backend endpoint contracts",
"scope": ["src/api/**/*.ts"]
}]
}
}
```

Greptile can now check API endpoint consistency, warn about deprecated endpoints, and validate request/response types.

**Services `greptile.json`:**

```
{
"patternRepositories": [
"acme/shared-utils",
"acme/testing-framework"
],
"customContext": {
"rules": [{
"rule": "Use shared logging utilities from acme/shared-utils",
"scope": ["src/**/*.ts"]
}]
}
}
```

Greptile can detect reimplementation of existing utilities and suggest using shared patterns instead.

## Troubleshooting

Pattern repository not found

**Symptoms:**

* Repository not found errors in dashboard
* Pattern context not appearing in reviews

**Solutions:**

1. Verify repository name format: `org/repo` or `group/project`
2. Check GitHub/GitLab access permissions
3. Confirm repository exists and isnt private without access
4. Allow time for initial indexing

No context from pattern repositories

**Symptoms:**

* Pattern repos indexed but not referenced in reviews
* Expected patterns not being suggested

**Common causes:**

* Context only applied when relevant to PR changes
* Pattern repo may not contain applicable patterns for the change
* Indexing may still be in progress

**Solutions:**

1. Check repository index status in dashboard
2. Add explicit references in PR description
Example: relates to auth patterns in acme/shared-utils
3. Verify pattern repo contains relevant code/docs

Access denied errors

**Symptoms:**

* Access denied or permission errors
* Pattern repos not indexing

**Check your configuration:**

```
{
"patternRepositories": [
"your-org/shared-library"
]
}
```

**Solutions:**

1. Verify your GitHub/GitLab integration has access to the pattern repository
2. For private repos, ensure Greptile app installation includes the repository
3. Check organization permissions if using GitHub Apps

Test repository access by visiting the repo URL while logged in to GitHub/GitLab with the same account used for Greptile integration.

## Whats Next
