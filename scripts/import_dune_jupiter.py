"""Import verified Jupiter adoption metrics into all dashboard reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_adoption import parse_daily_jupiter_swap_csv
from solana_observatory.pipeline import write_reports


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import seven-day Jupiter signer, fee-payer overlap, and "
            "retention metrics from a reviewed Dune CSV export."
        )
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--collected-at", required=True)
    return parser.parse_args()


def _series_by_date(metric: dict, label: str) -> dict[str, int | float]:
    series = metric.get("series")
    if not isinstance(series, list):
        raise ValueError(f"Snapshot {label} metric is missing a series")
    values = {
        point.get("observed_at"): point.get("value")
        for point in series
        if isinstance(point, dict)
    }
    if len(values) != len(series) or None in values:
        raise ValueError(f"Snapshot {label} series is invalid")
    return values


def _validate_populations(metrics: dict[str, dict], snapshot: dict) -> None:
    published = snapshot.get("metrics", {})
    fee_payers = published.get("daily_unique_successful_fee_payers")
    signers = published.get("daily_unique_successful_signers")
    if fee_payers is None or signers is None:
        raise ValueError(
            "Snapshot must include successful fee-payer and signer metrics"
        )

    fees_by_date = _series_by_date(fee_payers, "fee-payer")
    signers_by_date = _series_by_date(signers, "successful-signer")
    users_by_date = _series_by_date(
        metrics["daily_unique_jupiter_swap_signers"], "Jupiter signer"
    )
    overlap_by_date = _series_by_date(
        metrics["daily_jupiter_fee_payer_overlap"], "Jupiter overlap"
    )
    if set(users_by_date) != set(fees_by_date) or set(users_by_date) != set(
        signers_by_date
    ):
        raise ValueError("Jupiter and network population dates must match")

    for observed_at, user_count in users_by_date.items():
        if user_count > signers_by_date[observed_at]:
            raise ValueError(
                f"Jupiter signer count for {observed_at} exceeds all signers"
            )
        if overlap_by_date[observed_at] > fees_by_date[observed_at]:
            raise ValueError(
                f"Jupiter fee-payer overlap for {observed_at} exceeds fee payers"
            )


def main() -> int:
    args = _arguments()
    try:
        csv_text = args.input.read_text(encoding="utf-8")
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        metrics = parse_daily_jupiter_swap_csv(
            csv_text,
            collected_at=args.collected_at,
            source_url=args.source_url,
        )
        _validate_populations(metrics, snapshot)
        snapshot["metrics"].update(metrics)
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
