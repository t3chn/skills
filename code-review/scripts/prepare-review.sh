#!/bin/bash
# prepare-review.sh - Prepare git SHAs for code review
# Usage: ./prepare-review.sh [base_ref]
# Examples:
#   ./prepare-review.sh              # Compare against HEAD~1
#   ./prepare-review.sh main         # Compare against main branch
#   ./prepare-review.sh HEAD~5       # Compare against 5 commits ago
#   ./prepare-review.sh "Task 1"     # Compare against commit with "Task 1" message

set -e

BASE_REF="${1:-HEAD~1}"
HEAD_SHA=$(git rev-parse HEAD)

# Try to resolve base reference
if git rev-parse "$BASE_REF" >/dev/null 2>&1; then
    # Direct ref (branch, tag, SHA, HEAD~n)
    BASE_SHA=$(git rev-parse "$BASE_REF")
elif git log --oneline --all | grep -q "$BASE_REF"; then
    # Search in commit messages
    BASE_SHA=$(git log --oneline --all | grep "$BASE_REF" | head -1 | awk '{print $1}')
else
    echo "Error: Cannot resolve '$BASE_REF'" >&2
    echo "Usage: $0 [base_ref]" >&2
    echo "  base_ref: branch, tag, SHA, HEAD~n, or commit message search" >&2
    exit 1
fi

# Output for easy copy-paste
echo "BASE_SHA=$BASE_SHA"
echo "HEAD_SHA=$HEAD_SHA"
echo ""
echo "# Changes to review:"
git log --oneline "$BASE_SHA".."$HEAD_SHA"
echo ""
echo "# Files changed:"
git diff --stat "$BASE_SHA".."$HEAD_SHA" | tail -1
echo ""
echo "# Quick diff summary:"
git diff --shortstat "$BASE_SHA".."$HEAD_SHA"
