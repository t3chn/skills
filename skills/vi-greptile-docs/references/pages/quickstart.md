# 5-Minute Quickstart

URL: https://www.greptile.com/docs/quickstart

This guide covers GitHub/GitLab setup, repository configuration, and your first automated code review.

## Installation & Setup

GitHub or GitLab users can follow the outlined steps to successfully enable Greptile within their repositories.
```
[Log in](https://app.greptile.com/login) to your Greptile account or [sign up](https://app.greptile.com/signup) via email, Google, Github, or GitLab.
```
Ensure you have the required permissions to allow the AI code reviewer access to all or specific repos. Each platform offers a different procedure for integration.

### GitHub App Installation

The following steps will help you connect Greptile with GitHub:

Connect to GitHub

Click the **Connect** button with the GitHub icon to link your GitHub account in the ** Settings** dashboard.

Grant Greptile access to repositories

Select the type of repository access you want to grant Greptile.

* **All repository** : This grants Greptile access to all current and future repositories both public and private.
* **Only select repositories** : At least one repository should be selected for access.

### GitLab Integration

The following steps will help you connect Greptile with GitLab:

Connect to GitLab

Select **GitLab** in the dropdown button at the top right corner, in the ** Settings** dashboard.

Generate Personal or Group Access Token on GitLab

* Log in to your **GitLab** account.
* Go to **User Settings** or ** Group Settings** to generate access token.
* An access token should have a name, role, expiration usually one year and selected scope as **api** .

Copy GitLab Access Token

Copy the generated GitLab access token and fill it in the access token field and click **Submit** in Greptile Settings dashboard.

Configure Webhook on GitLab

Greptile generates details needed to create a GitLab webhook; a **URL** , **secret token** and ** triggers**.

* Go to your **GitLab** account.
* Click on **Webhooks** in your GitLab Project/Group Settings.
* Fill in details for GitLab webhook including the Greptile generated URL, secret token, and check required triggers and click **Add webhook** .
* Click on the **DONE, I HAVE MADE THE CHANGES** button.

### Repository Selection & Configuration

The following configuration steps are common to GitHub and GitLab:

Enable repository indexing by Greptile

Ensure you have enabled Greptile to index all or selected repositories.

Configure PR Summary

Customize how Greptile summarizes pull requests:

* **Summary** : Choose if you want summaries of changes
* **Include diagrams** : Add sequence diagrams for complex changes
* **Confidence scores** : Show/hide confidence levels for each PR

[Learn more about PR summaries ](/docs/code-review/first-pr-review#pr-summary)

Control Review Behavior

Fine-tune what Greptile comments on:

* **Severity threshold** : Low (more comments) High (critical only)
* **Comment types** : Toggle logic, syntax, and style issues

[Learn more about controlling nitpickiness ](/docs/code-review/controlling-nitpickiness)

Add Filters

Set when Greptile automatically reviews:

* **Labels** : Only review PRs with specific labels (e.g., needs-review)
* **Authors** : Include/exclude specific developers or bots
* **Branches** : Target specific branches (e.g., main, develop)
* **Keywords** : Trigger on PR title/description keywords

[Learn more about triggers ](/docs/code-review/controlling-nitpickiness#trigger-configuration)

After a repository has been indexed (typically 1-2 hours for very large repos), any new pull/merge request will initiate automated code reviews by Greptile.

---

## Create Your First Test PR

Try Greptile on a test pull request to see it in action:

Create a pull request

Make a test PR to your indexed repo with some code changes.

Wait for review (~3 minutes)

Greptile analyzes your PR with full codebase context and posts a comprehensive review.

Review the feedback

a summary of changes, inline comments on issues, and suggested fixes.

When issues are spotted, Greptile suggests potential code fixes:

You can trigger a code review manually by tagging **@greptileai** with a comment. This is helpful for reviewing older PRs from before Greptile was integrated.

---

## Whats next?
