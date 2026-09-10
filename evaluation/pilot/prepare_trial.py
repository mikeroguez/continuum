#!/usr/bin/env python3
"""Create one isolated, local continuity-pilot trial directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


PILOT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PILOT_ROOT.parents[1]
BASELINE = PILOT_ROOT / "baseline"
OVERLAYS = PILOT_ROOT / "overlays"
TEMPLATE = REPOSITORY_ROOT / "template"
TRIAL_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")


def tree_hash(root: Path) -> str:
    """Return a stable content hash without recording absolute paths."""
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def copy_continuum(destination: Path) -> None:
    for name in ("AI_COLLABORATION.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy2(TEMPLATE / name, destination / name)
    shutil.copytree(TEMPLATE / "tools", destination / "tools")
    shutil.copytree(TEMPLATE / ".ai", destination / ".ai")
    shutil.copytree(OVERLAYS / "C" / ".ai", destination / ".ai", dirs_exist_ok=True)
    shutil.copy2(
        OVERLAYS / "C" / "project-index.md",
        destination / ".ai" / "state" / "estado-dev.md",
    )


def prepare(condition: str, trial_id: str, destination: Path) -> dict[str, str]:
    """Create a trial once. Existing directories are never overwritten."""
    if not TRIAL_ID.fullmatch(trial_id):
        raise ValueError("trial_id must be a short pseudonymous identifier")
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")

    shutil.copytree(BASELINE, destination)
    partial_hash = tree_hash(BASELINE)
    if condition in {"B", "C"}:
        shutil.copy2(OVERLAYS / "B" / "AGENT_GUIDE.md", destination / "AGENT_GUIDE.md")
    if condition == "C":
        copy_continuum(destination)

    metadata = {
        "trial_id": trial_id,
        "condition": condition,
        "partial_tree_sha256": partial_hash,
        "acceptance_command": "python -m unittest discover -s tests -t .",
    }
    metadata_dir = destination / ".continuum-pilot"
    metadata_dir.mkdir()
    (metadata_dir / "trial.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=("A", "B", "C"), required=True)
    parser.add_argument("--trial-id", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    try:
        metadata = prepare(args.condition, args.trial_id, args.destination)
    except (FileExistsError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
