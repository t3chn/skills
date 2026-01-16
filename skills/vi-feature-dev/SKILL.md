---
name: vi-feature-dev
description: "Guided end-to-end feature development workflow (discovery → codebase exploration → clarifying questions → architecture → implementation → review → summary). Use when implementing a new feature or significant change and you want a structured, question-first approach."
---

# Feature Development (7-Phase Workflow)

Implement new features with a systematic, high-signal process: understand first, ask questions, design, implement, review, summarize.

## Core principles

- Ask clarifying questions early and explicitly; don’t guess requirements.
- Understand the codebase before designing or coding.
- Prefer simple, maintainable solutions that match existing patterns.
- Don’t start implementation without explicit user approval.
- Track progress with `update_plan` when available.

## Phase 1: Discovery

Goal: Ensure the request is understood.

Actions:

1. Restate the feature request and success criteria.
2. If unclear, ask targeted questions (problem, scope, constraints, non-goals).
3. Confirm understanding before moving on.

## Phase 2: Codebase exploration

Goal: Learn the relevant architecture and patterns.

Actions:

1. Do 2–3 focused exploration passes (sequentially) such as:
   - **Similar feature tracer**: find the closest existing feature and trace it end-to-end.
   - **Architecture mapper**: map layers/abstractions and extension points in the relevant area.
   - **UX/testing patterns**: find UI patterns, tests, and conventions that apply.
2. Produce a short list of key files to read (5–15), then read them.
3. Summarize findings: patterns to follow, pitfalls to avoid, and where the change should live.

## Phase 3: Clarifying questions

Goal: Resolve all ambiguities before design.

Actions:

1. Identify underspecified aspects: edge cases, error handling, integration points, backward compatibility, performance, rollout.
2. Present questions as a numbered list.
3. **Wait for answers before proceeding.**

If the user says “whatever you think is best”, propose defaults and get explicit confirmation.

## Phase 4: Architecture design

Goal: Design options and recommend an approach.

Actions:

1. Propose 2–3 approaches with trade-offs (e.g., minimal changes vs cleaner separation).
2. Recommend one approach and explain why it fits this repo and request.
3. Get explicit user choice/approval for the approach.
4. Produce an implementation blueprint: files to touch, component boundaries, data flow, tests.

## Phase 5: Implementation

Goal: Build the feature.

Actions:

1. **Wait for explicit approval to start coding.**
2. Implement following the chosen design and repo conventions.
3. Keep changes scoped; avoid unrelated refactors.
4. Run the narrowest relevant checks/tests when available.

## Phase 6: Quality review

Goal: Catch bugs and improve quality without over-nitpicking.

Actions:

1. Review from 3 angles (sequentially):
   - **Correctness** (bugs, edge cases, error handling)
   - **Simplicity** (unnecessary complexity, duplication, readability)
   - **Conventions** (project rules, layering, naming, tests)
2. Present the highest-severity issues first.
3. Ask what to do: fix now, defer, or proceed.

## Phase 7: Summary

Goal: Make the work easy to understand and ship.

Actions:

1. Summarize what was built and the key decisions.
2. List files modified and suggested next steps (tests, rollout, docs).
3. Ensure the plan is marked complete.
