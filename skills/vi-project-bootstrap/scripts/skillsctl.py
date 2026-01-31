#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def _inject_src() -> None:
    skill_root = Path(__file__).resolve().parents[1]
    src_dir = skill_root / "src"
    if src_dir.is_dir():
        sys.path.insert(0, str(src_dir))


_inject_src()

from vi_project_bootstrap.skillsctl import cli  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(cli())

