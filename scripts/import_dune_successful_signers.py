"""Import a verified Dune successful-signers export into dashboard reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_adoption import parse_daily_successful_signers_csv
from solana_observatory.pipeline import write_reports


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a seven-day Dune successful-signers CSV export."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--collected-at", required=True)
    return parser.parse_args()


def _validate_against_fee_payers(
    signer_metric: dict, fee_payer_metric: dict
) -> None:
    fee_payers_by_date = {
        point["observed_at"]: point["value"]
        for point in fee_payer_metric.get("series", [])
    }
    for point in signer_metric["series"]:
        observed_at = point["observed_at"]
        fee_payer_count = fee_payers_by_date.get(observed_at)
        if fee_payer_count is not None and point["value"] < fee_payer_count:
            raise ValueError(
                f"Successful signer count for {observed_at} is below fee-payer count"
            )


def main() -> int:
    args = _arguments()
    try:
        csv_text = args.input.read_text(encoding="utf-8")
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        fee_payer_metric = snapshot.get("metrics", {}).get(
            "daily_unique_successful_fee_payers"
        )
        if fee_payer_metric is None:
            raise ValueError("Snapshot is missing the successful fee-payer metric")
        metric = parse_daily_successful_signers_csv(
            csv_text,
            collected_at=args.collected_at,
            source_url=args.source_url,
        )
        _validate_against_fee_payers(metric, fee_payer_metric)
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
