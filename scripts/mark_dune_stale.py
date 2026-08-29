"""Preserve verified Dune values while exposing an unavailable refresh."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_adoption import mark_dune_metrics_stale
from solana_observatory.pipeline import write_reports


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        changed = mark_dune_metrics_stale(
            snapshot,
            reason="Automatic query execution unavailable",
        )
        written = write_reports(snapshot, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Dune stale fallback failed: {error}", file=sys.stderr)
        return 1

    print(f"Preserved {changed} verified Dune metrics as stale.")
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
