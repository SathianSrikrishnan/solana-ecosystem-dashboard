"""Dependency-free access to the latest result of a public Dune query."""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import Any
from urllib.request import Request, urlopen


USER_AGENT = "Solana-Observatory/0.3 (+public-bounty-dashboard)"


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
            "User-Agent": USER_AGENT,
        },
    )
    with opener(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def execute_query(
    query_id: int,
    api_key: str,
    *,
    opener: Callable[..., Any] = urlopen,
    sleeper: Callable[[float], None] = time.sleep,
    poll_interval: float = 2,
    max_polls: int = 90,
    timeout: int = 30,
) -> float:
    """Execute one saved query on Dune's small engine and return its credit cost."""
    if not api_key:
        raise ValueError("DUNE_API_KEY is required for a Dune query execution")
    if not isinstance(query_id, int) or query_id <= 0:
        raise ValueError("query_id must be a positive integer")
    headers = {
        "X-Dune-API-Key": api_key,
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }
    request = Request(
        f"https://api.dune.com/api/v1/query/{query_id}/execute",
        data=b'{"performance":"small","query_parameters":{}}',
        headers=headers,
        method="POST",
    )
    with opener(request, timeout=timeout) as response:
        submitted = json.loads(response.read().decode("utf-8"))
    execution_id = submitted.get("execution_id")
    if not isinstance(execution_id, str) or not execution_id:
        raise RuntimeError("Dune did not return an execution ID")

    for _ in range(max_polls):
        status_request = Request(
            f"https://api.dune.com/api/v1/execution/{execution_id}/status",
            headers=headers,
        )
        with opener(status_request, timeout=timeout) as response:
            status = json.loads(response.read().decode("utf-8"))
        if status.get("is_execution_finished"):
            state = status.get("state", "unknown")
            if state != "QUERY_STATE_COMPLETED":
                raise RuntimeError(f"Dune execution ended in {state}")
            cost = status.get("execution_cost_credits")
            if not isinstance(cost, (int, float)) or cost < 0:
                raise RuntimeError("Dune did not report a valid execution credit cost")
            return float(cost)
        sleeper(poll_interval)
    raise TimeoutError("Dune execution did not finish within the bounded polling window")
