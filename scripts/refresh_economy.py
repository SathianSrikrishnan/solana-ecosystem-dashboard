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
    parse_defillama_fee_chart,
    parse_defillama_rev,
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
        "why_it_matters": "Price gives market context for SOL-denominated activity.",
        "section": "economy",
    },
    "tvl": {
        "id": "solana_defi_tvl_usd",
        "label": "Solana DeFi TVL",
        "name": "DeFiLlama",
        "method": "v2/historicalChainTvl/Solana",
        "definition": "USD value locked in tracked Solana DeFi protocols.",
        "why_it_matters": "TVL shows capital deposited in tracked DeFi protocols.",
        "section": "economy",
    },
    "stablecoins": {
        "id": "solana_stablecoin_value_usd",
        "label": "Solana stablecoin circulating value",
        "name": "DeFiLlama",
        "method": "stablecoincharts/Solana",
        "definition": "USD value of circulating stablecoins tracked on Solana.",
        "why_it_matters": "Stablecoin value shows available dollar-like liquidity.",
        "section": "financial_rails",
    },
    "dex": {
        "id": "solana_dex_volume_usd",
        "label": "Solana daily DEX volume",
        "name": "DeFiLlama",
        "method": "overview/dexs/Solana?dataType=dailyVolume",
        "definition": "Aggregate tracked Solana spot DEX volume for one day.",
        "why_it_matters": "DEX volume shows the scale of tracked spot trading.",
        "section": "economy",
    },
    "chain_fees": {
        "id": "solana_chain_fees_usd", "label": "Solana chain fees",
        "name": "DeFiLlama", "method": "summary/fees/solana?dataType=dailyFees",
        "definition": "Base and priority transaction fees paid to Solana.",
        "why_it_matters": "Chain fees show demand for transaction execution.",
        "section": "economy",
    },
    "app_fees": {
        "id": "solana_app_fees_usd", "label": "Solana application fees",
        "name": "DeFiLlama", "method": "overview/fees/solana?dataType=dailyAppFees",
        "definition": "Fees users paid covered Solana applications.",
        "why_it_matters": "App fees show what users paid covered applications.",
        "section": "economy",
    },
    "app_revenue": {
        "id": "solana_app_revenue_usd", "label": "Solana application revenue",
        "name": "DeFiLlama", "method": "overview/fees/solana?dataType=dailyAppRevenue",
        "definition": "The covered application fees retained by protocols.",
        "why_it_matters": "App revenue shows captured value under provider definitions.",
        "section": "economy",
    },
    "rev": {
        "id": "solana_rev_usd", "label": "Solana REV (chain fees + tracked Jito tips)",
        "name": "DeFiLlama", "method": "dailyFees(Solana) + dailyFees(jito-mev-tips)",
        "definition": "Chain fees plus tracked gross Jito MEV tips.",
        "why_it_matters": "REV estimates value paid for blockspace and ordering.",
        "section": "economy",
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
        "section": details["section"],
        "label": details["label"],
        "value": None,
        "unit": "USD",
        "status": "unavailable",
        "definition": details["definition"],
        "why_it_matters": details["why_it_matters"],
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


def _normalize_fee_source(
    source_name: str, result: dict[str, Any], collected_at: str
) -> dict[str, Any]:
    if result.get("status") != "ok":
        return _unavailable_metric(
            source_name, result, collected_at, str(result.get("error", "unknown error"))
        )
    try:
        return parse_defillama_fee_chart(
            result["payload"], metric_kind=source_name,
            collected_at=collected_at, source_url=result["url"]
        )
    except (KeyError, TypeError, ValueError) as error:
        return _unavailable_metric(source_name, result, collected_at, str(error))


def _normalize_rev(
    results: dict[str, dict[str, Any]], collected_at: str
) -> dict[str, Any]:
    chain = results["chain_fees"]
    tips = results["jito_tips"]
    failed = next((item for item in (chain, tips) if item.get("status") != "ok"), None)
    if failed is not None:
        return _unavailable_metric(
            "rev", failed, collected_at, str(failed.get("error", "component unavailable"))
        )
    try:
        return parse_defillama_rev(
            chain["payload"], tips["payload"], collected_at=collected_at,
            chain_fees_url=chain["url"], jito_tips_url=tips["url"]
        )
    except (KeyError, TypeError, ValueError) as error:
        return _unavailable_metric("rev", chain, collected_at, str(error))


def _future_financial_rails_metrics(collected_at: str) -> list[dict[str, Any]]:
    """Expose important gaps without presenting research snapshots as live data."""
    return [
        {
            "id": "solana_non_stablecoin_rwa_value_usd",
            "section": "financial_rails",
            "label": "Tokenized real-world assets (excluding stablecoins)",
            "value": None,
            "unit": "USD",
            "status": "unavailable",
            "definition": (
                "Circulating market value of tokenized real-world assets on "
                "Solana, excluding the stablecoin asset class."
            ),
            "why_it_matters": (
                "This would show adoption of tokenized treasuries, equities, "
                "credit, commodities, funds, and other off-chain claims."
            ),
            "source": {
                "name": "RWA.xyz (optional adapter)",
                "method": "v4 assets aggregate; Solana; exclude Stablecoins",
                "url": "https://docs.rwa.xyz/api/authentication",
            },
            "collected_at": collected_at,
            "source_time": None,
            "confidence": "experimental",
            "caveat": (
                "Source not connected: dependable API access requires "
                "authentication. No historical article value is substituted."
            ),
            "series": [],
        },
        {
            "id": "solana_identifiable_payments_usd",
            "section": "financial_rails",
            "label": "Identifiable payment volume",
            "value": None,
            "unit": "USD",
            "status": "unavailable",
            "definition": (
                "Value transferred for identifiable commerce or remittance, "
                "with a published attribution method and coverage boundary."
            ),
            "why_it_matters": (
                "Payments would show use of Solana as financial settlement "
                "rather than only trading infrastructure."
            ),
            "source": {
                "name": "No approved live source",
                "method": "deferred pending defensible payment attribution",
                "url": "https://www.stablecoin.fyi/methodology",
            },
            "collected_at": collected_at,
            "source_time": None,
            "confidence": "experimental",
            "caveat": (
                "Raw stablecoin transfers are not payments: they can include "
                "trading, bots, rebalancing, and repeated movement."
            ),
            "series": [],
        },
    ]


def _flag_fee_sanity_violations(metrics: dict[str, dict[str, Any]]) -> None:
    app_fees = metrics["solana_app_fees_usd"]
    app_revenue = metrics["solana_app_revenue_usd"]
    if app_fees["status"] != "ok" or app_revenue["status"] != "ok":
        return
    fees_by_day = {
        point["observed_at"]: point["value"] for point in app_fees["series"]
    }
    violation_dates = [
        point["observed_at"]
        for point in app_revenue["series"]
        if point["observed_at"] in fees_by_day
        and point["value"] > fees_by_day[point["observed_at"]]
    ]
    if violation_dates:
        app_revenue["status"] = "error"
        app_revenue["caveat"] += (
            " Provider data failed the app revenue <= app fees sanity check "
            f"on {', '.join(violation_dates)}; definitions or coverage may differ."
        )


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
    metrics = {}
    for source_name in ("price", "tvl", "stablecoins", "dex"):
        metric = _normalize_source(source_name, results[source_name], collected_at)
        for companion in metric.pop("companion_metrics", []):
            metrics[companion["id"]] = companion
        metrics[metric["id"]] = metric
    for source_name in ("chain_fees", "app_fees", "app_revenue"):
        metric = _normalize_fee_source(source_name, results[source_name], collected_at)
        metrics[metric["id"]] = metric
    _flag_fee_sanity_violations(metrics)
    rev = _normalize_rev(results, collected_at)
    metrics[rev["id"]] = rev
    for metric in _future_financial_rails_metrics(collected_at):
        metrics[metric["id"]] = metric
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
