"""Fetch bounded public economy data without API credentials."""

from __future__ import annotations

import json
from typing import Any, Callable
from urllib.request import Request, urlopen


COINGECKO_PRICE_URL = (
    "https://api.coingecko.com/api/v3/simple/price?"
    "ids=solana&vs_currencies=usd&include_24hr_change=true&"
    "include_last_updated_at=true"
)
DEFILLAMA_TVL_URL = "https://api.llama.fi/v2/historicalChainTvl/Solana"
DEFILLAMA_STABLECOIN_URL = (
    "https://stablecoins.llama.fi/stablecoincharts/Solana"
)
DEFILLAMA_DEX_URL = (
    "https://api.llama.fi/overview/dexs/Solana?"
    "excludeTotalDataChartBreakdown=true&dataType=dailyVolume"
)
USER_AGENT = "Solana-Observatory/0.2 (+public-bounty-dashboard)"


def fetch_json(
    url: str,
    *,
    opener: Callable[..., Any] = urlopen,
    timeout: int = 20,
) -> dict[str, Any] | list[Any]:
    """Fetch one public JSON object or list."""

    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with opener(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid JSON from {url}") from error
    if not isinstance(payload, (dict, list)):
        raise ValueError(f"Unexpected JSON shape from {url}")
    return payload


def fetch_economy_sources(
    *,
    opener: Callable[..., Any] = urlopen,
    timeout: int = 20,
) -> dict[str, dict[str, Any]]:
    """Fetch each economy source independently and preserve its status."""

    sources = {
        "price": COINGECKO_PRICE_URL,
        "tvl": DEFILLAMA_TVL_URL,
        "stablecoins": DEFILLAMA_STABLECOIN_URL,
        "dex": DEFILLAMA_DEX_URL,
    }
    results: dict[str, dict[str, Any]] = {}
    for source_name, url in sources.items():
        try:
            payload = fetch_json(url, opener=opener, timeout=timeout)
        except (OSError, ValueError) as error:
            results[source_name] = {
                "status": "error",
                "url": url,
                "error": str(error),
            }
        else:
            results[source_name] = {
                "status": "ok",
                "url": url,
                "payload": payload,
            }
    return results
