"""Refresh bounded ecosystem breadth and release metrics."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.contracts import validate_snapshot
from solana_observatory.ecosystem import parse_agave_releases, parse_defillama_protocol_breadth
from solana_observatory.ecosystem_client import fetch_ecosystem_sources
from solana_observatory.pipeline import write_reports


def _unavailable_metric(
    *, metric_id: str, label: str, unit: str, definition: str,
    why_it_matters: str, source_name: str, source_method: str,
    source_url: str, collected_at: str, caveat: str,
) -> dict[str, Any]:
    return {
        "id": metric_id,
        "section": "ecosystem",
        "label": label,
        "value": None,
        "unit": unit,
        "status": "unavailable",
        "definition": definition,
        "why_it_matters": why_it_matters,
        "source": {"name": source_name, "method": source_method, "url": source_url},
        "collected_at": collected_at,
        "source_time": None,
        "confidence": "experimental",
        "caveat": caveat,
        "series": [],
    }


def _source_failure_metrics(
    source_name: str, result: dict[str, Any], collected_at: str
) -> dict[str, dict[str, Any]]:
    error = str(result.get("error", "source could not be verified"))
    if source_name == "protocols":
        specs = (
            ("solana_tracked_tvl_protocols", "Solana protocols with tracked TVL", "protocols"),
            ("solana_tracked_tvl_categories", "Tracked Solana DeFi categories", "categories"),
        )
        name = "DeFiLlama"
        method = "protocols; Solana positive TVL coverage"
    else:
        specs = (
            ("agave_latest_stable_release_age_days", "Latest stable Agave release age", "days"),
            ("agave_stable_releases_90d", "Stable Agave releases in 90 days", "releases"),
        )
        name = "Anza Agave GitHub releases"
        method = "GitHub stable releases"
    return {
        metric_id: _unavailable_metric(
            metric_id=metric_id,
            label=label,
            unit=unit,
            definition="The live ecosystem source could not be normalized.",
            why_it_matters="This source contributes one bounded ecosystem signal.",
            source_name=name,
            source_method=method,
            source_url=result["url"],
            collected_at=collected_at,
            caveat=f"Source refresh failed visibly: {error}",
        )
        for metric_id, label, unit in specs
    }


def _developer_gaps(collected_at: str) -> dict[str, dict[str, Any]]:
    url = "https://www.developerreport.com/"
    specs = (
        (
            "solana_monthly_active_developers",
            "Monthly active Solana developers",
            "developers",
            "Developers contributing to attributable open-source Solana repositories in a month.",
            "It would show the current size of the attributable builder base.",
        ),
        (
            "solana_retained_developers",
            "Retained Solana developers",
            "developers",
            "Attributable Solana developers active across a defined prior and current period.",
            "Retention would separate durable building from one-time repository activity.",
        ),
    )
    return {
        metric_id: _unavailable_metric(
            metric_id=metric_id,
            label=label,
            unit=unit,
            definition=definition,
            why_it_matters=why,
            source_name="Electric Capital Developer Report",
            source_method="optional reproducible developer dataset",
            source_url=url,
            collected_at=collected_at,
            caveat=(
                "Source not connected: no dependable no-key live export and "
                "repository-attribution contract has been verified."
            ),
        )
        for metric_id, label, unit, definition, why in specs
    }


def refresh_ecosystem(
    snapshot_path: Path,
    output_dir: Path,
    *,
    collected_at: str,
    source_results: dict[str, dict[str, Any]] | None = None,
) -> list[Path]:
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    validate_snapshot(snapshot)
    results = source_results if source_results is not None else fetch_ecosystem_sources()
    metrics: dict[str, dict[str, Any]] = {}
    for name in ("protocols", "agave_releases"):
        result = results[name]
        if result.get("status") != "ok":
            metrics.update(_source_failure_metrics(name, result, collected_at))
            continue
        try:
            parsed = (
                parse_defillama_protocol_breadth(
                    result["payload"], collected_at=collected_at, source_url=result["url"]
                )
                if name == "protocols"
                else parse_agave_releases(
                    result["payload"], collected_at=collected_at, source_url=result["url"]
                )
            )
        except (KeyError, TypeError, ValueError) as error:
            failed = {**result, "error": str(error)}
            metrics.update(_source_failure_metrics(name, failed, collected_at))
        else:
            metrics.update(parsed)
    metrics.update(_developer_gaps(collected_at))
    snapshot["metrics"].update(metrics)
    snapshot["generated_at"] = collected_at
    return write_reports(snapshot, output_dir)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh ecosystem metrics.")
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _arguments()
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        written = refresh_ecosystem(
            args.snapshot, args.output, collected_at=collected_at
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Ecosystem refresh failed: {error}", file=sys.stderr)
        return 1
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
