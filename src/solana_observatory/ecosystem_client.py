"""Fetch bounded no-key ecosystem signals independently."""

from __future__ import annotations

from typing import Any, Callable
from urllib.request import urlopen

from .economy_client import fetch_json


DEFILLAMA_PROTOCOLS_URL = "https://api.llama.fi/protocols"
GITHUB_AGAVE_RELEASES_URL = (
    "https://api.github.com/repos/anza-xyz/agave/releases?per_page=100"
)


def fetch_ecosystem_sources(
    *, opener: Callable[..., Any] = urlopen, timeout: int = 20
) -> dict[str, dict[str, Any]]:
    sources = {
        "protocols": DEFILLAMA_PROTOCOLS_URL,
        "agave_releases": GITHUB_AGAVE_RELEASES_URL,
    }
    results: dict[str, dict[str, Any]] = {}
    for name, url in sources.items():
        try:
            payload = fetch_json(url, opener=opener, timeout=timeout)
        except (OSError, ValueError) as error:
            results[name] = {"status": "error", "url": url, "error": str(error)}
        else:
            results[name] = {"status": "ok", "url": url, "payload": payload}
    return results
