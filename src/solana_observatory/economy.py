"""Normalize public economy source responses into dashboard metrics."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import math
from typing import Any
from urllib.parse import urlparse


def _collection_time(collected_at: str) -> datetime:
    try:
        collected_time = datetime.fromisoformat(
            collected_at.replace("Z", "+00:00")
        )
    except ValueError as error:
        raise ValueError("collected_at must be an ISO-8601 timestamp") from error
    if collected_time.tzinfo is None:
        raise ValueError("collected_at must include a timezone")
    return collected_time.astimezone(timezone.utc)


def _finite_number(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be numeric") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    if positive and number <= 0:
        raise ValueError(f"{label} must be positive")
    return number


def parse_coingecko_sol_price(
    payload: dict[str, Any],
    *,
    collected_at: str,
    source_url: str,
) -> dict[str, Any]:
    """Return a live SOL/USD metric from CoinGecko simple-price data."""

    collected_time = _collection_time(collected_at)
    if urlparse(source_url).hostname != "api.coingecko.com":
        raise ValueError("source_url must use CoinGecko's public API")
    if not isinstance(payload, dict) or not isinstance(payload.get("solana"), dict):
        raise ValueError("CoinGecko payload must include solana")

    solana = payload["solana"]
    price = _finite_number(solana.get("usd"), "SOL price", positive=True)
    _finite_number(
        solana.get("usd_24h_change"), "SOL 24-hour change"
    )
    source_timestamp = solana.get("last_updated_at")
    if isinstance(source_timestamp, bool) or not isinstance(source_timestamp, int):
        raise ValueError("CoinGecko last_updated_at must be a Unix timestamp")
    source_time = datetime.fromtimestamp(source_timestamp, tz=timezone.utc)
    if source_time > collected_time:
        raise ValueError("CoinGecko source time cannot be in the future")

    return {
        "id": "sol_price_usd",
        "section": "economy",
        "label": "SOL price",
        "value": round(price, 2),
        "unit": "USD",
        "status": "ok",
        "definition": "CoinGecko's aggregated market price for one SOL in USD.",
        "source": {
            "name": "CoinGecko",
            "method": "simple/price?ids=solana",
            "url": source_url,
        },
        "collected_at": collected_at,
        "source_time": source_time.isoformat().replace("+00:00", "Z"),
        "confidence": "high",
        "caveat": (
            "Market price is volatile context, not evidence that network or "
            "application usage is growing."
        ),
        "series": [],
    }


def _complete_day_series(
    rows: list[Any],
    *,
    collected_time: datetime,
    date_value: Any,
) -> list[dict[str, Any]]:
    expected_dates = {
        collected_time.date() - timedelta(days=days_ago)
        for days_ago in range(1, 15)
    }
    observations: dict[date, float] = {}
    for row in rows:
        raw_date, raw_value = date_value(row)
        try:
            timestamp = int(raw_date)
            observed_at = datetime.fromtimestamp(
                timestamp, tz=timezone.utc
            ).date()
        except (TypeError, ValueError, OSError) as error:
            raise ValueError("DeFiLlama date must be a Unix timestamp") from error
        if observed_at >= collected_time.date():
            raise ValueError("DeFiLlama series must exclude the current UTC day")
        if observed_at in observations:
            raise ValueError(f"Duplicate DeFiLlama date: {observed_at}")
        value = _finite_number(raw_value, "DeFiLlama value")
        if value < 0:
            raise ValueError("DeFiLlama value cannot be negative")
        observations[observed_at] = value

    if not expected_dates.issubset(observations):
        raise ValueError("DeFiLlama series must include fourteen complete UTC days")
    return [
        {
            "observed_at": observed_at.isoformat(),
            "value": round(observations[observed_at], 2),
        }
        for observed_at in sorted(expected_dates)
    ]


def parse_defillama_economy(
    tvl_payload: list[dict[str, Any]],
    stablecoin_payload: list[dict[str, Any]],
    dex_payload: dict[str, Any],
    *,
    collected_at: str,
    source_urls: dict[str, str],
) -> dict[str, dict[str, Any]]:
    """Return complete-day Solana TVL, stablecoin, and DEX metrics."""

    collected_time = _collection_time(collected_at)
    expected_hosts = {
        "tvl": "api.llama.fi",
        "stablecoins": "stablecoins.llama.fi",
        "dex": "api.llama.fi",
    }
    for source_name, expected_host in expected_hosts.items():
        source_url = source_urls.get(source_name, "")
        if urlparse(source_url).hostname != expected_host:
            raise ValueError(f"{source_name} source URL must use DeFiLlama")
    if not isinstance(tvl_payload, list) or not isinstance(
        stablecoin_payload, list
    ):
        raise ValueError("DeFiLlama history payloads must be lists")
    if not isinstance(dex_payload, dict) or not isinstance(
        dex_payload.get("totalDataChart"), list
    ):
        raise ValueError("DeFiLlama DEX payload must include totalDataChart")

    def tvl_value(row: Any) -> tuple[Any, Any]:
        if not isinstance(row, dict):
            raise ValueError("DeFiLlama TVL rows must be objects")
        return row.get("date"), row.get("tvl")

    def stablecoin_value(row: Any) -> tuple[Any, Any]:
        if not isinstance(row, dict) or not isinstance(
            row.get("totalCirculatingUSD"), dict
        ):
            raise ValueError("Stablecoin rows must include totalCirculatingUSD")
        buckets = row["totalCirculatingUSD"]
        if not buckets:
            raise ValueError("Stablecoin value buckets cannot be empty")
        values = [
            _finite_number(value, "Stablecoin bucket")
            for value in buckets.values()
        ]
        if any(value < 0 for value in values):
            raise ValueError("Stablecoin bucket cannot be negative")
        return row.get("date"), sum(values)

    def dex_value(row: Any) -> tuple[Any, Any]:
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError("DEX chart rows must be timestamp/value pairs")
        return row[0], row[1]

    tvl_series = _complete_day_series(
        tvl_payload,
        collected_time=collected_time,
        date_value=tvl_value,
    )
    stablecoin_series = _complete_day_series(
        stablecoin_payload,
        collected_time=collected_time,
        date_value=stablecoin_value,
    )
    dex_series = _complete_day_series(
        dex_payload["totalDataChart"],
        collected_time=collected_time,
        date_value=dex_value,
    )

    def metric(
        *,
        metric_id: str,
        label: str,
        definition: str,
        method: str,
        source_url: str,
        caveat: str,
        series: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "id": metric_id,
            "section": "economy",
            "label": label,
            "value": series[-1]["value"],
            "unit": "USD",
            "status": "ok",
            "definition": definition,
            "source": {
                "name": "DeFiLlama",
                "method": method,
                "url": source_url,
            },
            "collected_at": collected_at,
            "source_time": series[-1]["observed_at"],
            "confidence": "high",
            "caveat": caveat,
            "series": series,
        }

    metrics = [
        metric(
            metric_id="solana_defi_tvl_usd",
            label="Solana DeFi TVL",
            definition=(
                "USD value locked in Solana DeFi protocols tracked by "
                "DeFiLlama on the latest complete UTC day."
            ),
            method="v2/historicalChainTvl/Solana",
            source_url=source_urls["tvl"],
            caveat=(
                "TVL depends on protocol coverage and methodology and can "
                "double-count economic exposure through composable assets."
            ),
            series=tvl_series,
        ),
        metric(
            metric_id="solana_stablecoin_value_usd",
            label="Solana stablecoin circulating value",
            definition=(
                "USD value of circulating stablecoins on Solana across "
                "DeFiLlama's peg buckets on the latest complete UTC day."
            ),
            method="stablecoincharts/Solana",
            source_url=source_urls["stablecoins"],
            caveat=(
                "Circulating stablecoin value is not payment volume or proof "
                "that every token is backed by cash."
            ),
            series=stablecoin_series,
        ),
        metric(
            metric_id="solana_dex_volume_usd",
            label="Solana daily DEX volume",
            definition=(
                "Aggregate Solana spot DEX volume tracked by DeFiLlama on "
                "the latest complete UTC day."
            ),
            method="overview/dexs/Solana?dataType=dailyVolume",
            source_url=source_urls["dex"],
            caveat=(
                "Routing can touch several pools, and provider adapter and "
                "deduplication coverage determine the reported total."
            ),
            series=dex_series,
        ),
    ]
    return {item["id"]: item for item in metrics}
