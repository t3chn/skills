#!/usr/bin/env python3
"""
Feature-dev enforcement hook for Claude Code.

Blocks creation of 2+ new code files without /feature-dev workflow active.
This ensures multi-file features go through proper exploration and architecture phases.

Hook events handled:
  - PreToolUse (Write): Track new code files, block at threshold
  - UserPromptSubmit: Detect /feature-dev invocation, reset counter
  - SessionStart: Reset state for new session

Exit codes:
  - 0: Allow (with optional context)
  - 2: Block with error message (stderr)
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# State file in project's .claude directory
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
STATE_FILE = Path(PROJECT_DIR) / ".claude" / "feature-dev-state.json"

# Threshold for blocking
NEW_FILES_THRESHOLD = 2

# Code file patterns (implementation files that need feature-dev)
CODE_PATTERNS = [
    re.compile(r"^(?!.*_test\.go$).*\.go$"),  # Go (not tests)
    re.compile(r"^(?!.*\.(test|spec)\.(ts|tsx)$).*\.(ts|tsx)$"),  # TS (not tests)
    re.compile(r"^(?!test_)(?!.*_test\.py$).*\.py$"),  # Python (not tests)
    re.compile(r"^(?!.*_test\.rs$).*\.rs$"),  # Rust (not tests)
]

# Paths that bypass checks
BYPASS_PATTERNS = [
    r"\.md$",
    r"\.json$",
    r"\.ya?ml$",
    r"\.toml$",
    r"\.mod$",
    r"\.sum$",
    r"\.lock$",
    r"\.serena/",
    r"\.claude/",
    r"\.beads/",
    r"docs/",
    r"scripts/",
    r"hooks/",
    r"_test\.",
    r"\.test\.",
    r"\.spec\.",
    r"test_",
]


def load_state() -> dict:
    """Load feature-dev tracking state."""
    default = {"feature_dev_active": False, "new_files": [], "session_start": None}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            for k, v in default.items():
                if k not in state:
                    state[k] = v
            return state
        except (json.JSONDecodeError, IOError):
            pass
    return default


def save_state(state: dict) -> None:
    """Save state to file."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def is_bypass_path(path: str) -> bool:
    """Check if path should bypass feature-dev checks."""
    for pattern in BYPASS_PATTERNS:
        if re.search(pattern, path):
            return True
    return False


def is_code_file(filename: str) -> bool:
    """Check if file is a code implementation file."""
    for pattern in CODE_PATTERNS:
        if pattern.match(filename):
            return True
    return False


def handle_session_start() -> None:
    """Reset state for new session."""
    state = {
        "feature_dev_active": False,
        "new_files": [],
        "session_start": datetime.now().isoformat(),
    }
    save_state(state)
    sys.exit(0)


def handle_user_prompt(data: dict) -> None:
    """Detect /feature-dev invocation."""
    prompt = data.get("prompt", "").lower()
    state = load_state()

    if "/feature-dev" in prompt or "feature-dev:feature-dev" in prompt:
        state["feature_dev_active"] = True
        state["new_files"] = []
        save_state(state)

    # Output status
    status = "active" if state.get("feature_dev_active") else "inactive"
    new_count = len(state.get("new_files", []))
    print(f"[feature-dev: {status}, new files: {new_count}]", file=sys.stderr)
    sys.exit(0)


def handle_pre_tool_use(data: dict) -> None:
    """Track new code files and block if threshold exceeded."""
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path or tool_name != "Write":
        sys.exit(0)

    # Get relative path
    rel_path = file_path
    if file_path.startswith(PROJECT_DIR):
        rel_path = file_path[len(PROJECT_DIR) :].lstrip("/")

    # Check bypass patterns
    if is_bypass_path(rel_path):
        sys.exit(0)

    # Check if it's a new code file
    if Path(file_path).exists():
        sys.exit(0)  # Editing existing file

    filename = Path(rel_path).name
    if not is_code_file(filename):
        sys.exit(0)

    # Track new file
    state = load_state()
    if file_path not in state["new_files"]:
        state["new_files"].append(file_path)
        save_state(state)

    # Check if should block
    if state.get("feature_dev_active"):
        sys.exit(0)

    if len(state["new_files"]) >= NEW_FILES_THRESHOLD:
        files_str = ", ".join(Path(f).name for f in state["new_files"])
        print(
            f"BLOCKED: Creating {len(state['new_files'])} new code files without /feature-dev.\n"
            f"Files: {files_str}\n\n"
            f"Multi-file features require /feature-dev workflow:\n"
            f"1. Run /feature-dev <description>\n"
            f"2. Follow the 7-phase guided process\n"
            f"3. Then write implementation files",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    event = data.get("hook_event_name", "")

    if event == "SessionStart":
        handle_session_start()
    elif event == "UserPromptSubmit":
        handle_user_prompt(data)
    elif event == "PreToolUse":
        handle_pre_tool_use(data)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
