"""Normalize bounded ecosystem breadth and open-source release signals."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlparse


def _collected_time(collected_at: str) -> datetime:
    try:
        value = datetime.fromisoformat(collected_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("collected_at must be an ISO-8601 timestamp") from error
    if value.tzinfo is None:
        raise ValueError("collected_at must include a timezone")
    return value.astimezone(timezone.utc)


def _metric(
    *,
    metric_id: str,
    label: str,
    value: int | float,
    unit: str,
    definition: str,
    why_it_matters: str,
    source_name: str,
    source_method: str,
    source_url: str,
    collected_at: str,
    source_time: str,
    caveat: str,
) -> dict[str, Any]:
    return {
        "id": metric_id,
        "section": "ecosystem",
        "label": label,
        "value": value,
        "unit": unit,
        "status": "ok",
        "definition": definition,
        "why_it_matters": why_it_matters,
        "source": {
            "name": source_name,
            "method": source_method,
            "url": source_url,
        },
        "collected_at": collected_at,
        "source_time": source_time,
        "confidence": "medium",
        "caveat": caveat,
        "series": [],
    }


def parse_defillama_protocol_breadth(
    payload: list[dict[str, Any]], *, collected_at: str, source_url: str
) -> dict[str, dict[str, Any]]:
    """Count current positive-TVL Solana protocol and category coverage."""
    if urlparse(source_url).hostname != "api.llama.fi":
        raise ValueError("protocol source URL must use DeFiLlama")
    if not isinstance(payload, list):
        raise ValueError("DeFiLlama protocols payload must be a list")
    _collected_time(collected_at)
    covered: list[dict[str, Any]] = []
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError("DeFiLlama protocol rows must be objects")
        chains = row.get("chains", [])
        tvl = row.get("tvl")
        if (
            isinstance(chains, list)
            and "Solana" in chains
            and isinstance(tvl, (int, float))
            and not isinstance(tvl, bool)
            and tvl > 0
        ):
            covered.append(row)
    categories = {
        row["category"]
        for row in covered
        if isinstance(row.get("category"), str) and row["category"].strip()
    }
    common = {
        "source_name": "DeFiLlama",
        "source_url": source_url,
        "collected_at": collected_at,
        "source_time": collected_at,
    }
    metrics = [
        _metric(
            metric_id="solana_tracked_tvl_protocols",
            label="Solana protocols with tracked TVL",
            value=len(covered),
            unit="protocols",
            definition=(
                "DeFiLlama protocol records that include Solana and currently "
                "report positive TVL."
            ),
            why_it_matters=(
                "It provides a reproducible lower-bound view of deployed DeFi breadth."
            ),
            source_method="protocols; chains includes Solana; tvl > 0",
            caveat=(
                "This is provider coverage, not all Solana apps, active users, "
                "developer retention, or product quality."
            ),
            **common,
        ),
        _metric(
            metric_id="solana_tracked_tvl_categories",
            label="Tracked Solana DeFi categories",
            value=len(categories),
            unit="categories",
            definition=(
                "Distinct DeFiLlama categories among positive-TVL protocol "
                "records that include Solana."
            ),
            why_it_matters="Category breadth shows whether activity spans several use cases.",
            source_method="protocols; distinct category; Solana; tvl > 0",
            caveat=(
                "Provider category labels can change and do not measure usage, "
                "quality, or economic importance."
            ),
            **common,
        ),
    ]
    return {metric["id"]: metric for metric in metrics}


def parse_agave_releases(
    payload: list[dict[str, Any]], *, collected_at: str, source_url: str
) -> dict[str, dict[str, Any]]:
    """Measure stable Agave release recency and trailing-90-day cadence."""
    parsed_url = urlparse(source_url)
    if parsed_url.hostname != "api.github.com" or "/anza-xyz/agave/releases" not in parsed_url.path:
        raise ValueError("release source URL must use the official Agave GitHub API")
    if not isinstance(payload, list):
        raise ValueError("GitHub releases payload must be a list")
    collected_time = _collected_time(collected_at)
    stable: list[tuple[datetime, dict[str, Any]]] = []
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError("GitHub release rows must be objects")
        if row.get("draft") or row.get("prerelease"):
            continue
        try:
            published = datetime.fromisoformat(
                str(row["published_at"]).replace("Z", "+00:00")
            ).astimezone(timezone.utc)
        except (KeyError, ValueError) as error:
            raise ValueError("Stable releases must include published_at") from error
        if published > collected_time:
            raise ValueError("Release time cannot be in the future")
        stable.append((published, row))
    if not stable:
        raise ValueError("At least one stable Agave release is required")
    stable.sort(key=lambda item: item[0], reverse=True)
    latest_time, latest = stable[0]
    trailing_count = sum(
        published >= collected_time - timedelta(days=90)
        for published, _ in stable
    )
    source_time = latest_time.isoformat().replace("+00:00", "Z")
    latest_url = str(latest.get("html_url") or source_url)
    common = {
        "source_name": "Anza Agave GitHub releases",
        "source_url": latest_url,
        "collected_at": collected_at,
        "source_time": source_time,
    }
    metrics = [
        _metric(
            metric_id="agave_latest_stable_release_age_days",
            label="Latest stable Agave release age",
            value=round((collected_time - latest_time).total_seconds() / 86400, 1),
            unit="days",
            definition="Elapsed days since the newest non-draft, non-prerelease Agave release.",
            why_it_matters="Release recency is one bounded sign of maintained core software.",
            source_method=f"GitHub releases; latest stable tag {latest.get('tag_name', 'unknown')}",
            caveat=(
                "A recent release is not automatically safe or widely adopted, "
                "and release age is not a developer-count metric."
            ),
            **common,
        ),
        _metric(
            metric_id="agave_stable_releases_90d",
            label="Stable Agave releases in 90 days",
            value=trailing_count,
            unit="releases",
            definition="Non-draft, non-prerelease Agave releases published in the trailing 90 days.",
            why_it_matters="Release cadence shows whether core client work is shipping publicly.",
            source_method="GitHub releases; stable releases; trailing 90 days",
            caveat=(
                "Release count is not adoption, code quality, contributor count, "
                "or proof that validators upgraded."
            ),
            **common,
        ),
    ]
    return {metric["id"]: metric for metric in metrics}
