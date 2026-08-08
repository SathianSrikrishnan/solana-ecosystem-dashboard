"""Refresh public Solana economy metrics without hiding source failures."""

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
from solana_observatory.economy import (
    parse_coingecko_sol_price,
    parse_defillama_dex,
    parse_defillama_stablecoins,
    parse_defillama_tvl,
)
from solana_observatory.economy_client import fetch_economy_sources
from solana_observatory.pipeline import write_reports


SOURCE_DETAILS = {
    "price": {
        "id": "sol_price_usd",
        "label": "SOL price",
        "name": "CoinGecko",
        "method": "simple/price?ids=solana",
        "definition": "CoinGecko's aggregated market price for one SOL in USD.",
    },
    "tvl": {
        "id": "solana_defi_tvl_usd",
        "label": "Solana DeFi TVL",
        "name": "DeFiLlama",
        "method": "v2/historicalChainTvl/Solana",
        "definition": "USD value locked in tracked Solana DeFi protocols.",
    },
    "stablecoins": {
        "id": "solana_stablecoin_value_usd",
        "label": "Solana stablecoin circulating value",
        "name": "DeFiLlama",
        "method": "stablecoincharts/Solana",
        "definition": "USD value of circulating stablecoins tracked on Solana.",
    },
    "dex": {
        "id": "solana_dex_volume_usd",
        "label": "Solana daily DEX volume",
        "name": "DeFiLlama",
        "method": "overview/dexs/Solana?dataType=dailyVolume",
        "definition": "Aggregate tracked Solana spot DEX volume for one day.",
    },
}


def _unavailable_metric(
    source_name: str,
    result: dict[str, Any],
    collected_at: str,
    error: str,
) -> dict[str, Any]:
    details = SOURCE_DETAILS[source_name]
    return {
        "id": details["id"],
        "section": "economy",
        "label": details["label"],
        "value": None,
        "unit": "USD",
        "status": "unavailable",
        "definition": details["definition"],
        "source": {
            "name": details["name"],
            "method": details["method"],
            "url": result["url"],
        },
        "collected_at": collected_at,
        "source_time": None,
        "confidence": "experimental",
        "caveat": f"This source could not be verified during refresh: {error}",
        "series": [],
    }


def _normalize_source(
    source_name: str, result: dict[str, Any], collected_at: str
) -> dict[str, Any]:
    if result.get("status") != "ok":
        return _unavailable_metric(
            source_name,
            result,
            collected_at,
            str(result.get("error", "unknown error")),
        )
    try:
        if source_name == "price":
            return parse_coingecko_sol_price(
                result["payload"],
                collected_at=collected_at,
                source_url=result["url"],
            )
        parser = {
            "tvl": parse_defillama_tvl,
            "stablecoins": parse_defillama_stablecoins,
            "dex": parse_defillama_dex,
        }[source_name]
        return parser(
            result["payload"],
            collected_at=collected_at,
            source_url=result["url"],
        )
    except (KeyError, TypeError, ValueError) as error:
        return _unavailable_metric(source_name, result, collected_at, str(error))


def refresh_economy(
    snapshot_path: Path,
    output_dir: Path,
    *,
    collected_at: str,
    source_results: dict[str, dict[str, Any]] | None = None,
) -> list[Path]:
    """Merge independently collected economy metrics into one snapshot."""
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    validate_snapshot(snapshot)
    results = (
        source_results
        if source_results is not None
        else fetch_economy_sources()
    )
    metrics = {
        metric["id"]: metric
        for source_name in SOURCE_DETAILS
        for metric in [_normalize_source(source_name, results[source_name], collected_at)]
    }
    snapshot["metrics"].update(metrics)
    snapshot["generated_at"] = collected_at
    return write_reports(snapshot, output_dir)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh public economy metrics.")
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _arguments()
    collected_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        written = refresh_economy(
            args.snapshot, args.output, collected_at=collected_at
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Economy refresh failed: {error}", file=sys.stderr)
        return 1
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
