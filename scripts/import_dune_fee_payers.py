"""Import a verified Dune fee-payer export into dashboard reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_adoption import parse_daily_fee_payers_csv
from solana_observatory.pipeline import write_reports


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a seven-day Dune fee-payer CSV export."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--collected-at", required=True)
    return parser.parse_args()


def main() -> int:
    args = _arguments()
    try:
        csv_text = args.input.read_text(encoding="utf-8")
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        metric = parse_daily_fee_payers_csv(
            csv_text,
            collected_at=args.collected_at,
            source_url=args.source_url,
        )
        snapshot["metrics"][metric["id"]] = metric
        snapshot["generated_at"] = args.collected_at
        written = write_reports(snapshot, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Import failed: {error}", file=sys.stderr)
        return 1

    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
