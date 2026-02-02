# Beads Task Contract v0 (orx)

This contract is designed to prevent agent drift and feature creep.
Only tasks that opt in via the `orx` label are required to follow it.

## Description template

Use these fixed section headings in the Beads **Description** field:

```md
## Objective
One short sentence describing the result.

## Must-Haves (≤3)
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Non-Goals
- None

## Constraints
- None

## Verification
- Command(s) you will actually run (tests/lint/build).
```

## Acceptance Criteria field

Fill the Beads **Acceptance Criteria** field with bullet items, for example:

```md
- [ ] Condition 1 is true
- [ ] Condition 2 is true
```

## Multi-repo (optional)

For multi-repo work, put these key/value lines in the **Constraints** section:

```md
- Role: leaf
- EpicRef: github.com/owner/repo#<epic_bead_id>
```

Or for an epic:

```md
- Role: epic
- Child: github.com/owner/repo#<leaf_bead_id>
- Child: gitlab.com/group/subgroup/repo#<leaf_bead_id>
```

