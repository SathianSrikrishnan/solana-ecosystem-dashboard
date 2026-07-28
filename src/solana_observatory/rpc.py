"""Small, dependency-free Solana JSON-RPC client."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any
from urllib.request import Request, urlopen

from .snapshot import RPC_URL


class SolanaRpcError(RuntimeError):
    """Raised when the HTTP or JSON-RPC response cannot provide a result."""


Transport = Callable[[str, dict[str, Any], float], dict[str, Any]]


def _urlopen_transport(
    url: str, payload: dict[str, Any], timeout: float
) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "solana-ecosystem-dashboard/0.1",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


class SolanaRpcClient:
    def __init__(
        self,
        url: str = RPC_URL,
        *,
        timeout: float = 20.0,
        transport: Transport = _urlopen_transport,
    ) -> None:
        self.url = url
        self.timeout = timeout
        self.transport = transport
        self._request_id = 0

    def call(self, method: str, params: list[Any] | None = None) -> Any:
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params or [],
        }
        response = self.transport(self.url, payload, self.timeout)
        if "error" in response:
            error = response["error"]
            raise SolanaRpcError(
                f"{method} failed ({error.get('code')}): {error.get('message')}"
            )
        if "result" not in response:
            raise SolanaRpcError(f"{method} returned no result")
        return response["result"]


def collect_network_results(client: SolanaRpcClient) -> dict[str, Any]:
    """Collect the bounded RPC methods needed by the first snapshot."""

    calls: list[tuple[str, list[Any] | None]] = [
        ("getHealth", None),
        ("getSlot", [{"commitment": "confirmed"}]),
        ("getBlockHeight", [{"commitment": "confirmed"}]),
        ("getEpochInfo", [{"commitment": "confirmed"}]),
        ("getRecentPerformanceSamples", [1]),
        ("getVoteAccounts", [{"commitment": "confirmed"}]),
    ]
    return {method: client.call(method, params) for method, params in calls}

