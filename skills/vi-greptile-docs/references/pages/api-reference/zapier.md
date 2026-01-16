# Integrate with Zapier

URL: https://www.greptile.com/docs/api-reference/zapier

```
Greptile natively integrates with Zapier. See [here](https://zapier.com/apps/greptile/integrations) to get started.
```

## Overview and Examples

Greptile + Zapier allows you to quickly integrate Greptile into your developer tools to make them smarter.
The input is a prompt and one or more repositories, the output is a response with context from those repositories as well as links to specific locations in the code.
Some examples of how you could use it:

1. When a new issue is created in ClickUp, send the issue description to Greptile. Greptile will generate a codebase context-aware comment to help the developer get started with the ticket.
2. When a test fails in GitHub Actions, Greptile can generate a diagnosis with context from the codebase.
3. When there is a Sentry Alert, Greptile can generate a root cause analysis with context from the codebase.

## Authentication

To authenticate Greptile, you need a Greptile API key and a GitHub token.

```
Greptile API key can be provisioned [here](https://app.greptile.com/settings/api).
```

```
GitHub token can be provisioned [here](https://github.com/settings/tokens). Ensure it has access to the target repositories.
```

Greptile API Key must be formatted in the field as `Bearer api_key`.

## Input and Output Formats

The input is a `messages` array that contains the prompt and history of prompts/responses for conversational usecases as well as a `repositories` array that contains the repositories to reference.
The output is a `json` with `message` and `sources`.
**Sample Input:**
`messages`:

```
[
{
"content": "Diagnose this bug: `${stack_trace}`",
"role": "user",
"id": "0000"
}
]
```

`repositories`:

```
[
{
"repository":"helicone/helicone",
"remote":"github",
"branch":"main"
}
]
```

**Sample Output:**
The output looks something like this:

```
{
"message": "Based on the code, there are several potential reasons why ClickHouse writes might be failing: ...",
"sources": [
{
"repository": "helicone/helicone",
"remote": "github",
"branch": "main",
"filepath": "/valhalla/jawn/src/lib/db/ClickhouseWrapper.ts",
"linestart": 82,
"lineend": 92,
"summary": "The `ClickhouseWrapper.ts` file contains the implementation of the...",
"distance": 0.2171129350993909
},
{
"remote": "github",
"remoteUrl": null,
"branch": "main",
"repository": "helicone/helicone",
"filepath": "/valhalla/jawn/src/lib/db/ClickhouseWrapper.ts",
"linestart": 1,
"lineend": 80,
"summary": "The `ClickhouseWrapper.ts` file contains the implementation of the...",
"distance": 0
}
]
}
```
