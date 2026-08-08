"""Normalize public economy source responses into dashboard metrics."""

from __future__ import annotations

from datetime import datetime, timezone
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
