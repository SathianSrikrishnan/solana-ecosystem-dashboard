"""Expose whether the verified Dune adoption slice is due for execution."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_adoption import is_dune_execution_due


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    due = is_dune_execution_due(snapshot, now=datetime.now(timezone.utc))
    value = str(due).lower()
    print(f"Dune adoption execution due: {value}")
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with Path(output_path).open("a", encoding="utf-8") as output:
            output.write(f"due={value}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
