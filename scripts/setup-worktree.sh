#!/bin/bash
# Create a git worktree for parallel development
# Usage: ./scripts/setup-worktree.sh <branch-name> [base-branch]
# Example: ./scripts/setup-worktree.sh feature/auth main

set -e

BRANCH_NAME=$1
BASE_BRANCH=${2:-main}
TREES_DIR=".trees"

if [ -z "$BRANCH_NAME" ]; then
    echo "Usage: $0 <branch-name> [base-branch]"
    echo ""
    echo "Examples:"
    echo "  $0 feature/auth          # Create from main"
    echo "  $0 fix/parser develop    # Create from develop"
    echo ""
    echo "Available worktrees:"
    git worktree list
    exit 1
fi

# Sanitize branch name for directory (replace / with -)
DIR_NAME=$(echo "$BRANCH_NAME" | sed 's|/|-|g')
WORKTREE_PATH="$TREES_DIR/$DIR_NAME"

# Create trees directory if not exists
mkdir -p "$TREES_DIR"

# Check if worktree already exists
if [ -d "$WORKTREE_PATH" ]; then
    echo "Worktree already exists at $WORKTREE_PATH"
    echo "To remove: git worktree remove $WORKTREE_PATH"
    exit 1
fi

# Create worktree with new branch or checkout existing
echo "Creating worktree for '$BRANCH_NAME'..."
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    # Branch exists, just checkout
    git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
else
    # Create new branch from base
    git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" "$BASE_BRANCH"
fi

echo ""
echo "Worktree created!"
echo ""
echo "  cd $WORKTREE_PATH"
echo ""
echo "When done:"
echo "  git push -u origin $BRANCH_NAME"
echo "  # Create PR, merge, then:"
echo "  git worktree remove $WORKTREE_PATH"
echo "  git branch -d $BRANCH_NAME"
