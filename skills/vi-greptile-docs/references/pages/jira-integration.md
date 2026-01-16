# Jira Integration

URL: https://www.greptile.com/docs/jira-integration

Connect Jira to give Greptile access to ticket context during code reviews. When PRs reference Jira tickets, Greptile verifies code against requirements and flags gaps.

## What You Get

* **Automatic ticket detection** - Greptile identifies Jira references in PR titles, descriptions, and commit messages
* **Requirement verification** - Reviews flag when code doesnt match ticket acceptance criteria
* **Context-aware comments** - Greptile considers business context from linked tickets
* **Status awareness** - Understands ticket priority and type (bug, feature, story)

**Example:** A PR titled JIRA-123: Add user authentication links to a ticket requiring password complexity. Greptile flags if the implementation is missing that validation.

## Setup

Go to Integrations

Click **Integrations** in the left sidebar of your Greptile dashboard.

Connect Jira

Click **Connect** on the Atlassian card.

Accept Connection

Click **Accept** to allow Greptile to connect to Jira.

Accepting also connects Atlassian Confluence.

Done

Atlassian appears as a connected data source in your dashboard.
