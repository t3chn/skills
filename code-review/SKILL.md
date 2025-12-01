---
name: code-review
description: Use when receiving code review feedback (especially if unclear or technically questionable), when completing tasks or major features requiring review before proceeding, or before making any completion/success claims. Covers three practices - (1) receiving feedback with technical rigor over performative agreement (no "You're absolutely right!", no "Great point!"), (2) requesting reviews via code-reviewer subagent after each task, (3) verification gates requiring evidence before any status claims. Essential for subagent-driven development, pull requests, and preventing false completion claims. Honors YAGNI, KISS, DRY.
---

# Code Review

**Core principle:** Technical correctness over social comfort. Verify before implementing. Evidence before claims.

## References

| Practice | When | Reference |
|----------|------|-----------|
| **Receiving feedback** | Got review comments, unclear feedback, external reviewer | `references/code-review-reception.md` |
| **Requesting review** | Completed task/feature, before merge | `references/requesting-code-review.md` |
| **Verification gates** | About to claim completion/success | `references/verification-before-completion.md` |

## Tools

| Tool | Purpose |
|------|---------|
| `templates/code-reviewer-prompt.md` | Ready-to-use prompt for code-reviewer subagent |
| `scripts/prepare-review.sh` | Get git SHAs for review (`./prepare-review.sh [base]`) |

## Decision Tree

```
SITUATION?
│
├─ Received feedback
│  ├─ Unclear? → STOP, clarify ALL items first
│  ├─ From user? → Understand, implement (no performative agreement)
│  └─ External? → Verify technically, push back if wrong
│
├─ Completed work
│  └─ Request code-reviewer subagent review
│
└─ About to claim status
   ├─ Have fresh evidence? → Claim WITH evidence
   └─ No evidence? → RUN verification first
```

## Key Rules

**Receiving feedback:**
- ❌ "You're absolutely right!", "Great point!", "Thanks for..."
- ✅ Restate requirement, ask questions, push back, or just work

**Verification (Iron Law):**
- NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
- IDENTIFY → RUN → READ → VERIFY → THEN claim
- "Should pass" / "seems to work" = NOT verified

**Red flags - STOP:**
- Using "should"/"probably"/"seems to"
- Expressing satisfaction before verification
- Trusting agent reports without checking
