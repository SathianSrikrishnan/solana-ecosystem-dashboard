"""Refresh all verified Dune adoption slices from their latest stored results."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_adoption import (
    mark_dune_metrics_stale, parse_daily_fee_payers_csv,
    parse_daily_jupiter_swap_csv, parse_daily_successful_signers_csv,
)
from solana_observatory.dune_client import fetch_query_csv
from solana_observatory.pipeline import write_reports

QUERIES = {"fee_payers": 8213434, "signers": 8264418, "jupiter": 8264526}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    api_key = os.environ.get("DUNE_API_KEY", "")
    if not api_key:
        print("DUNE_API_KEY is not configured; preserving the last verified Dune metrics.")
        return 0
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        fee = parse_daily_fee_payers_csv(fetch_query_csv(QUERIES["fee_payers"], api_key), collected_at=collected_at, source_url=f"https://dune.com/queries/{QUERIES['fee_payers']}")
        signers = parse_daily_successful_signers_csv(fetch_query_csv(QUERIES["signers"], api_key), collected_at=collected_at, source_url=f"https://dune.com/queries/{QUERIES['signers']}")
        jupiter = parse_daily_jupiter_swap_csv(fetch_query_csv(QUERIES["jupiter"], api_key), collected_at=collected_at, source_url=f"https://dune.com/queries/{QUERIES['jupiter']}")
        snapshot["metrics"].update({fee["id"]: fee, signers["id"]: signers, **jupiter})
        snapshot["generated_at"] = collected_at
        written = write_reports(snapshot, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Dune refresh failed without replacing verified data: {error}", file=sys.stderr)
        if "snapshot" in locals() and mark_dune_metrics_stale(snapshot, reason=str(error)):
            written = write_reports(snapshot, args.output)
            for path in written: print(path)
        return 0
    for path in written: print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
