---
name: vi-code-reviewer
description: "Review local changes (git diff or specified files) for real bugs, security issues, and guideline violations using confidence scoring; report only high-confidence, high-impact findings. Use when you want a strict, low-false-positive code review."
---

# Code Reviewer (High-Confidence Review)

Review changes with high precision and low false positives. Prefer quality over quantity.

## Default scope

- By default, review the current working tree diff (`git diff`).
- If the user asks, review staged changes (`git diff --staged`) or specific files/commits.

## Confidence scoring (0–100)

Rate each potential issue:

- **0**: Almost certainly false positive / irrelevant.
- **25**: Possible issue, but unclear or mostly stylistic.
- **50**: Real but low impact or edge-case.
- **75**: Likely real and important; would affect correctness/security/maintainability.
- **100**: Certain and high impact; evidence directly confirms it.

**Only report issues with confidence ≥ 80.**

## What to check

- **Project guidelines**: follow explicit repo rules (`AGENTS.md`, `CONTRIBUTING.md`, lint rules, conventions).
- **Correctness**: logic errors, missing edge cases, race conditions, resource leaks.
- **Security**: injection, authz/authn mistakes, secrets handling, unsafe deserialization, SSRF/XSS, etc.
- **Reliability/perf**: timeouts, retries, backpressure, N+1 queries, unbounded memory growth.
- **Maintainability**: major duplication, unclear abstractions, missing critical tests (only if important).

## Output format

1. State what you reviewed (diff/scope).
2. Group findings by severity (**Critical**, **Important**).
3. For each finding, include:
   - **Confidence** (0–100)
   - **Location** (file path + line number when available)
   - **Why it matters** (bug/security/guideline violation)
   - **Fix suggestion** (concrete)
4. If there are no high-confidence issues, say so and include a brief “looks good” summary.
