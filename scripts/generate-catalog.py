#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
DOUBLE_QUOTED_RE = re.compile(r'^"([^"\\\\]|\\\\.)*"$')
SINGLE_QUOTED_RE = re.compile(r"^'([^']|'')*'$")


def _unquote_scalar(value: str) -> str:
    value = value.strip()
    if DOUBLE_QUOTED_RE.match(value):
        inner = value[1:-1]
        inner = inner.replace(r"\\", "\\").replace(r"\"", '"')
        return inner
    if SINGLE_QUOTED_RE.match(value):
        inner = value[1:-1]
        return inner.replace("''", "'")
    return value


def _split_frontmatter(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines()
    if not lines:
        raise ValueError("empty file")
    if lines[0].lstrip("\ufeff").strip() != "---":
        raise ValueError("missing opening '---' YAML front matter delimiter")

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], lines[idx + 1 :]
    raise ValueError("missing closing '---' YAML front matter delimiter")


def _parse_frontmatter_subset(frontmatter_lines: list[str]) -> dict[str, str]:
    """
    Parse a tiny YAML subset suitable for this repo's SKILL.md frontmatter.

    Supported:
    - Top-level `key: value`
    - Block scalars `key: |` and `key: >` with indented content
    """
    out: dict[str, str] = {}
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        m = KEY_VALUE_RE.match(line)
        if not m:
            raise ValueError(f"invalid YAML line: {line!r}")
        key = m.group(1)
        value = m.group(2).strip()

        if value.startswith(("|", ">")):
            fold = value.startswith(">")
            block: list[str] = []
            i += 1
            while i < len(frontmatter_lines):
                raw = frontmatter_lines[i]
                if raw.strip() == "":
                    block.append("")
                    i += 1
                    continue
                if KEY_VALUE_RE.match(raw) and not raw.startswith((" ", "\t")):
                    break
                if not raw.startswith((" ", "\t")):
                    raise ValueError(f"block scalar content for {key!r} must be indented")
                block.append(raw.lstrip(" \t"))
                i += 1
            if fold:
                # Minimal folding: join non-empty lines with spaces, keep blank lines as paragraph breaks.
                paragraphs: list[str] = []
                current: list[str] = []
                for b in block:
                    if b == "":
                        if current:
                            paragraphs.append(" ".join(current).strip())
                            current = []
                        else:
                            paragraphs.append("")
                        continue
                    current.append(b)
                if current:
                    paragraphs.append(" ".join(current).strip())
                out[key] = "\n".join(paragraphs).strip()
            else:
                out[key] = "\n".join(block).strip()
            continue

        out[key] = _unquote_scalar(value)
        i += 1

    return out


def _extract_title(body_lines: list[str], fallback_id: str) -> str:
    for raw in body_lines:
        line = raw.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            title = title.replace("`", "")
            title = re.sub(r"\s+", " ", title).strip()
            if title:
                return title
    # Fallback: Title Case from id.
    return " ".join(w.capitalize() for w in fallback_id.split("-") if w)


def _default_tags(skill_id: str) -> list[str]:
    tags: list[str] = []
    for tok in skill_id.split("-"):
        tok = tok.strip()
        if tok and tok not in tags:
            tags.append(tok)
    for tok in ("codex", "skills"):
        if tok not in tags:
            tags.append(tok)
    return tags


def _load_existing_catalog(catalog_path: Path) -> dict[str, dict[str, Any]]:
    if not catalog_path.exists():
        return {}
    try:
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    skills = data.get("skills")
    if not isinstance(skills, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in skills:
        if not isinstance(item, dict):
            continue
        skill_id = item.get("id")
        if isinstance(skill_id, str) and skill_id:
            out[skill_id] = item
    return out


def build_catalog(repo_root: Path) -> dict[str, Any]:
    skills_dir = repo_root / "skills"
    catalog_path = repo_root / "catalog" / "skills.json"

    existing = _load_existing_catalog(catalog_path)

    skills: list[dict[str, Any]] = []
    for skill_dir in sorted([p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm_lines, body_lines = _split_frontmatter(text)
        fm = _parse_frontmatter_subset(fm_lines)

        skill_id = skill_dir.name
        name = fm.get("name", "").strip()
        desc = fm.get("description", "").strip()
        if not name:
            raise ValueError(f"missing frontmatter name in {skill_md}")
        if name != skill_id:
            raise ValueError(f"frontmatter name {name!r} does not match directory {skill_id!r} in {skill_md}")
        if not desc:
            raise ValueError(f"missing frontmatter description in {skill_md}")

        title = _extract_title(body_lines, fallback_id=skill_id)

        old = existing.get(skill_id, {})
        if isinstance(old.get("title"), str) and old.get("title"):
            title = str(old["title"])
        tags = old.get("tags") if isinstance(old.get("tags"), list) else _default_tags(skill_id)
        aliases = old.get("aliases") if isinstance(old.get("aliases"), list) else []

        skills.append(
            {
                "id": skill_id,
                "title": title,
                "description": desc,
                "tags": tags,
                "aliases": aliases,
                "targets": {"codex": {"path": f"skills/{skill_id}"}},
            }
        )

    skills.sort(key=lambda s: str(s.get("id", "")))
    return {"schema_version": 1, "skills": skills}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate catalog/skills.json from skills/*/SKILL.md")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if catalog/skills.json would change.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    catalog_path = repo_root / "catalog" / "skills.json"

    data = build_catalog(repo_root)
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        current = catalog_path.read_text(encoding="utf-8") if catalog_path.exists() else ""
        if current != rendered:
            print("[FAIL] catalog/skills.json is out of date. Run: python3 scripts/generate-catalog.py")
            return 1
        print("[OK] catalog/skills.json is up to date.")
        return 0

    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(rendered, encoding="utf-8")
    print("[OK] Wrote catalog/skills.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

