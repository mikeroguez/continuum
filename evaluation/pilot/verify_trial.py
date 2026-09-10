#!/usr/bin/env python3
"""Run the fixed acceptance test and append a minimal local trial record."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ACCEPTANCE_COMMAND = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."]


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if ".continuum-pilot" in path.parts:
            continue
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def run_acceptance(trial_directory: Path, *, capture_output: bool = False) -> tuple[int, float]:
    started = time.monotonic()
    completed = subprocess.run(
        ACCEPTANCE_COMMAND,
        cwd=trial_directory,
        check=False,
        capture_output=capture_output,
    )
    return completed.returncode, time.monotonic() - started


def record_result(record_path: Path, result: dict[str, object]) -> None:
    record_path.parent.mkdir(parents=True, exist_ok=True)
    with record_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(result, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial-directory", type=Path, required=True)
    parser.add_argument("--trial-id", required=True)
    parser.add_argument("--condition", choices=("A", "B", "C"), required=True)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()

    metadata_path = args.trial_directory / ".continuum-pilot" / "trial.json"
    if not metadata_path.is_file():
        parser.error("trial directory was not prepared by prepare_trial.py")
    metadata = json.loads(metadata_path.read_text())
    if metadata["trial_id"] != args.trial_id or metadata["condition"] != args.condition:
        parser.error("trial identifier or condition does not match prepared metadata")

    return_code, duration_seconds = run_acceptance(args.trial_directory)
    result: dict[str, object] = {
        "trial_id": args.trial_id,
        "condition": args.condition,
        "acceptance_passed": return_code == 0,
        "acceptance_returncode": return_code,
        "duration_seconds": round(duration_seconds, 3),
        "partial_tree_sha256": metadata["partial_tree_sha256"],
        "result_tree_sha256": tree_hash(args.trial_directory),
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if args.record:
        record_result(args.record, result)
    print(json.dumps(result, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
