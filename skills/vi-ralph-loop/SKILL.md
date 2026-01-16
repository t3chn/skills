---
name: vi-ralph-loop
description: "Run an iterative 'Ralph loop' workflow: keep the same prompt and repeatedly refine code (run tests, fix, repeat) until completion criteria are met or max iterations reached. Use when a task benefits from persistent iteration and objective verification."
---

# Ralph Loop (Iterative Development Loop)

Use the Ralph Wiggum technique: iterate on the *same prompt* until the work is genuinely complete. The “self-reference” comes from seeing your previous attempts in the repo (files, diffs, tests), not from feeding your own output back in.

## Inputs

- **Prompt**: a single, stable task description (don’t rewrite it every iteration).
- **Completion promise** (optional): an exact phrase to output only when the claim is unquestionably true.
- **Max iterations** (recommended): a safety cap to avoid infinite loops.

## Prompt template

Include:

- Requirements and non-goals
- Objective checks (tests, linters, build)
- Clear completion criteria
- An escape hatch for “stuck” cases (what to do near the iteration limit)

Example:

- “Run `npm test`; all tests must pass.”
- “Output `<promise>COMPLETE</promise>` only when the criteria are met.”

## Loop procedure

For each iteration:

1. Re-read the prompt *verbatim* and restate the current completion criteria.
2. Inspect current repo state (diffs, failing tests, logs, TODOs).
3. Make the smallest change that moves the work forward.
4. Run the narrowest relevant verification (tests/lint/build) and use failures as data.
5. Decide:
   - If complete: output `<promise>…</promise>` (only if it is true) and stop.
   - If not complete: continue to the next iteration without changing the prompt.

## Critical rule (completion promises)

If a completion promise is set, output it **only** when the statement is completely and unequivocally true. Do not output false promises to “exit the loop”.

## When to use

Good for:
- Well-defined tasks with objective checks (tests, linters, builds)
- Work that benefits from repeated debug → test → fix cycles

Not good for:
- Tasks requiring frequent human decisions or ambiguous product choices
- One-shot operations with unclear success criteria

## Cancel / stop

If the user asks to stop/cancel, stop iterating and instead:

1. Summarize what’s done and what remains
2. List blockers and what was tried
3. Suggest the next 1–3 concrete steps to resume later
