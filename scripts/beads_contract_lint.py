#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass


SECTION_PATTERNS: dict[str, re.Pattern[str]] = {
    "Objective": re.compile(r"^#{0,6}\s*Objective\s*:?\s*$", re.IGNORECASE),
    "Must-Haves": re.compile(
        r"^#{0,6}\s*Must[- ]Haves(?:\s*\([^)]*\))?\s*:?\s*$", re.IGNORECASE
    ),
    "Non-Goals": re.compile(r"^#{0,6}\s*Non[- ]Goals\s*:?\s*$", re.IGNORECASE),
    "Constraints": re.compile(r"^#{0,6}\s*Constraints\s*:?\s*$", re.IGNORECASE),
    "Verification": re.compile(r"^#{0,6}\s*Verification\s*:?\s*$", re.IGNORECASE),
}

ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(?P<text>.+?)\s*$")
META_KV_RE = re.compile(r"^(?P<key>[A-Za-z][A-Za-z0-9_-]*)\s*:\s*(?P<value>\S.*)$")

REPO_ID_RE = re.compile(r"^[^\s#/]+/[^\s#]+/[^\s#]+(?:/[^\s#]+)*$")
REPO_REF_RE = re.compile(r"^(?P<repo_id>[^\s#]+)#(?P<issue_id>[^\s#]+)$")


@dataclass(frozen=True)
class IssueRef:
    repo_id: str
    issue_id: str


def _parse_issue_ref(value: str) -> IssueRef | None:
    match = REPO_REF_RE.match(value.strip())
    if not match:
        return None
    repo_id = match.group("repo_id")
    issue_id = match.group("issue_id")
    if not REPO_ID_RE.match(repo_id):
        return None
    return IssueRef(repo_id=repo_id, issue_id=issue_id)


def _extract_section_blocks(text: str) -> tuple[dict[str, list[str]], list[str]]:
    lines = text.splitlines()
    section_starts: list[tuple[int, str]] = []
    errors: list[str] = []

    for idx, line in enumerate(lines):
        stripped = line.strip()
        for section, pattern in SECTION_PATTERNS.items():
            if pattern.match(stripped):
                section_starts.append((idx, section))
                break

    # Detect duplicates.
    seen: set[str] = set()
    for _, section in section_starts:
        if section in seen:
            errors.append(f"duplicate section heading: {section}")
        seen.add(section)

    blocks: dict[str, list[str]] = {}
    if errors:
        return blocks, errors

    section_starts_sorted = sorted(section_starts, key=lambda t: t[0])
    for i, (start_idx, section) in enumerate(section_starts_sorted):
        end_idx = (
            section_starts_sorted[i + 1][0] if i + 1 < len(section_starts_sorted) else len(lines)
        )
        content = lines[start_idx + 1 : end_idx]
        # Trim leading/trailing empty lines.
        while content and content[0].strip() == "":
            content = content[1:]
        while content and content[-1].strip() == "":
            content = content[:-1]
        blocks[section] = content

    return blocks, []


def _count_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in lines:
        match = ITEM_RE.match(line)
        if not match:
            continue
        text = match.group("text").strip()
        if text:
            items.append(text)
    return items


def _extract_meta(items: list[str]) -> dict[str, list[str]]:
    meta: dict[str, list[str]] = {}
    for item in items:
        match = META_KV_RE.match(item)
        if not match:
            continue
        key = match.group("key").strip().lower()
        value = match.group("value").strip()
        meta.setdefault(key, []).append(value)
    return meta


def validate_issue(issue: dict) -> list[str]:
    errors: list[str] = []
    issue_id = str(issue.get("id", "")).strip() or "<missing-id>"

    description = str(issue.get("description", "") or "")
    blocks, block_errors = _extract_section_blocks(description)
    if block_errors:
        errors.extend(block_errors)
        return errors

    required_sections = ["Objective", "Must-Haves", "Non-Goals", "Constraints", "Verification"]
    for section in required_sections:
        if section not in blocks:
            errors.append(f"missing section: {section}")

    # Stop early if key sections are missing.
    if any(e.startswith("missing section:") for e in errors):
        return errors

    # Objective: must have at least one non-empty line.
    objective_lines = [ln.strip() for ln in blocks.get("Objective", []) if ln.strip()]
    if not objective_lines:
        errors.append("Objective section is empty")

    must_haves_items = _count_items(blocks.get("Must-Haves", []))
    if not must_haves_items:
        errors.append("Must-Haves must contain 1–3 bullet items")
    elif len(must_haves_items) > 3:
        errors.append(f"Must-Haves has {len(must_haves_items)} items (max 3)")

    non_goals_items = _count_items(blocks.get("Non-Goals", []))
    if not non_goals_items:
        errors.append("Non-Goals must contain at least 1 bullet item (use '- None' if needed)")

    constraints_items = _count_items(blocks.get("Constraints", []))
    if not constraints_items:
        errors.append("Constraints must contain at least 1 bullet item (use '- None' if needed)")

    verification_items = _count_items(blocks.get("Verification", []))
    if not verification_items:
        errors.append("Verification must contain at least 1 bullet item/command")

    acceptance = str(issue.get("acceptance_criteria", "") or "")
    ac_items = _count_items(acceptance.splitlines())
    if not ac_items:
        errors.append("Acceptance Criteria is missing or has no bullet items")

    # Optional multi-repo meta inside Constraints.
    meta = _extract_meta(constraints_items)
    role_values = meta.get("role", [])
    if role_values:
        role = role_values[-1].strip().lower()
        if role not in {"leaf", "epic"}:
            errors.append("Constraints Role must be 'leaf' or 'epic'")
        if role == "leaf":
            epic_refs = meta.get("epicref", [])
            if not epic_refs:
                errors.append("Constraints Role=leaf requires 'EpicRef: <host>/<path>#<bead_id>'")
            elif _parse_issue_ref(epic_refs[-1]) is None:
                errors.append("Invalid EpicRef format (expected '<host>/<path>#<bead_id>')")
        if role == "epic":
            children = meta.get("child", [])
            if not children:
                errors.append("Constraints Role=epic requires at least one 'Child: <host>/<path>#<bead_id>'")
            else:
                for child in children:
                    if _parse_issue_ref(child) is None:
                        errors.append("Invalid Child format (expected '<host>/<path>#<bead_id>')")
                        break

    if errors:
        title = str(issue.get("title", "") or "").strip()
        header = f"{issue_id}: {title}" if title else issue_id
        return [header] + errors
    return []


def _iter_issues(path: pathlib.Path) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    issues: list[dict] = []
    if not path.exists():
        # Not all repositories track Beads issues in git. If the issues file is
        # absent, treat the lint as not-applicable and succeed.
        return issues, []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return issues, [f"failed to read issues file: {exc}"]

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("<<<<<<<", "=======", ">>>>>>>")):
            errors.append(f"merge conflict marker found in issues file at line {lineno}")
            continue
        try:
            issues.append(json.loads(stripped))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON at line {lineno}: {exc.msg}")
    return issues, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint Beads issues for the orx task contract v0 (anti-drift)."
    )
    parser.add_argument(
        "issue_ids",
        nargs="*",
        help="Optional issue IDs to lint. If omitted, lints issues matching --label/--status.",
    )
    parser.add_argument(
        "--issues-file",
        default=".beads/issues.jsonl",
        help="Path to .beads/issues.jsonl (default: .beads/issues.jsonl).",
    )
    parser.add_argument(
        "--label",
        default="orx",
        help="Only lint issues that include this label (default: orx).",
    )
    parser.add_argument(
        "--status",
        choices=["open", "closed", "all"],
        default="open",
        help="Which issues to consider when using --label filtering (default: open).",
    )
    args = parser.parse_args()

    issues_path = pathlib.Path(args.issues_file).expanduser().resolve()
    issues, load_errors = _iter_issues(issues_path)
    if load_errors:
        for err in load_errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        return 2

    wanted_ids = {i.strip() for i in args.issue_ids if i.strip()}
    label = args.label.strip()
    status_filter = args.status

    def matches(issue: dict) -> bool:
        issue_id = str(issue.get("id", "") or "").strip()
        if wanted_ids:
            return issue_id in wanted_ids
        if status_filter != "all":
            status = str(issue.get("status", "") or "").strip().lower()
            if status != status_filter:
                return False
        labels = issue.get("labels", []) or []
        return label in {str(x).strip() for x in labels}

    selected = [i for i in issues if matches(i)]
    if not selected:
        return 0

    failed = False
    for issue in selected:
        errors = validate_issue(issue)
        if not errors:
            continue
        failed = True
        header, *rest = errors
        print(f"[FAIL] {header}", file=sys.stderr)
        for msg in rest:
            print(f"  - {msg}", file=sys.stderr)

    if failed:
        print(
            "\nFix: ensure the issue description has Objective/Must-Haves/Non-Goals/Constraints/Verification "
            "sections and Acceptance Criteria contains bullet items.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
