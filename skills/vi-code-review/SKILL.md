---
name: vi-code-review
description: "Automate GitHub pull request code reviews using `gh`: check eligibility (not closed/draft/trivial/already-reviewed), collect relevant `AGENTS.md` guidance, review changes from multiple perspectives, confidence-score issues, and post a concise PR comment with full-SHA code links."
---

# GitHub PR Code Review (gh)

Provide a structured code review for a GitHub pull request using the GitHub CLI (`gh`).

## Prerequisites

- `gh` installed and authenticated (`gh auth status`)
- Run inside a git repo with the PR remote configured

## Workflow

1. Create an `update_plan` checklist for the steps below.

2. Identify the PR:
   - If the user provides a PR URL/number, use that.
   - Otherwise, infer the current PR (`gh pr view`) or ask which PR to review.

3. Eligibility check (skip if not eligible):
   - PR is **closed/merged**
   - PR is a **draft**
   - PR is **trivial/automated** (e.g. dependency-bump bot PRs, mechanical version bumps) and obviously OK
   - PR already has a code review from you (check existing comments)

4. Gather review context:
   - Fetch PR summary + files changed (`gh pr view`)
   - Fetch diff (`gh pr diff`)
   - Collect relevant guidance files:
     - Root `AGENTS.md` (if present)
     - Any `AGENTS.md` in directories containing modified files
     - If none exist, proceed without them

5. Review from multiple perspectives (do separate passes; avoid nitpicks):
   - **Guidance compliance**: Does the change violate relevant `AGENTS.md` instructions?
   - **Shallow bug scan**: Obvious correctness issues visible in the diff (focus on big bugs).
   - **Historical context**: Use `git blame` / history on modified files for relevant pitfalls/regressions.
   - **Related PR context**: Look for prior PRs touching the same files and reuse relevant lessons (optional; only if easy via `gh`).
   - **Comment intent**: Ensure changes comply with important code comments in modified files.

6. For each potential issue, assign a confidence score (0–100):
   - **0**: False positive or clearly pre-existing
   - **25**: Might be real but can’t verify; stylistic and not explicitly required by guidance
   - **50**: Real but minor/nitpick or unlikely to matter
   - **75**: Very likely real and important; or explicitly mentioned by guidance
   - **100**: Definitely real; strong evidence it will occur frequently or break functionality

   Filter out issues with score **< 80**.

7. Re-check eligibility (PR can change while you review): still open, not draft, still needs review.

8. Comment on the PR with the result using `gh pr comment`.
   - Keep it brief; avoid emojis.
   - Cite each issue with a link to the exact code location using **full SHA** and a line range:
     `https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<start>-L<end>`

## Comment Format

If issues exist (score ≥ 80):

```markdown
### Code review

Found N issues:

1. <brief description> (<guidance or evidence>)

<full-sha link>
```

If no issues meet the threshold:

```markdown
### Code review

No issues found. Checked for bugs and guidance compliance.
```

## Review Boundaries

- Do not run builds/typechecks/linters just for review; assume CI will handle it.
- Ignore pre-existing problems not introduced by the PR.
- Avoid pedantic formatting/style nits unless explicitly required by a relevant guidance file.
