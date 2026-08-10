"""Dependency-free access to the latest result of a public Dune query."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.request import Request, urlopen


def fetch_query_csv(
    query_id: int,
    api_key: str,
    *,
    opener: Callable[..., Any] = urlopen,
    timeout: int = 30,
) -> str:
    """Fetch the latest stored CSV result without logging the credential."""
    if not api_key:
        raise ValueError("DUNE_API_KEY is required for automatic Dune refresh")
    if not isinstance(query_id, int) or query_id <= 0:
        raise ValueError("query_id must be a positive integer")
    url = f"https://api.dune.com/api/v1/query/{query_id}/results/csv"
    request = Request(
        url,
        headers={
            "X-Dune-API-Key": api_key,
            "User-Agent": "Solana-Observatory/0.3 (+public-bounty-dashboard)",
        },
    )
    with opener(request, timeout=timeout) as response:
        return response.read().decode("utf-8")
