"""Normalize bounded first-party Solana news and upgrade sources."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import re
from typing import Any
from xml.etree import ElementTree


NEWS_URL = "https://solana.com/news/rss.xml"
ALPENGLOW_URL = "https://solana.com/upgrades/alpenglow"
SIMD_0525_URL = "https://github.com/solana-foundation/solana-improvement-documents/blob/main/proposals/0525-reduce-slot-times.md"


def _metric(metric_id: str, label: str, value: Any, unit: str, definition: str,
            why: str, method: str, url: str, collected_at: str, source_time: str | None,
            caveat: str) -> dict[str, Any]:
    return {
        "id": metric_id, "section": "ecosystem", "label": label, "value": value,
        "unit": unit, "status": "ok", "definition": definition,
        "why_it_matters": why,
        "source": {"name": "Official Solana source", "method": method, "url": url},
        "collected_at": collected_at, "source_time": source_time,
        "confidence": "high", "caveat": caveat, "series": [],
    }


def parse_official_updates(
    rss_text: str, alpenglow_html: str, simd_text: str, *, collected_at: str
) -> dict[str, dict[str, Any]]:
    """Build current-news and named-upgrade metrics from official text."""
    collected = datetime.fromisoformat(collected_at.replace("Z", "+00:00")).astimezone(timezone.utc)
    root = ElementTree.fromstring(rss_text)
    item = root.find("./channel/item")
    if item is None:
        raise ValueError("Solana RSS has no news item")
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    published = parsedate_to_datetime(item.findtext("pubDate") or "").astimezone(timezone.utc)
    if not title or not link.startswith("https://solana.com/") or published > collected:
        raise ValueError("Latest Solana news item is invalid")
    age_days = round((collected - published).total_seconds() / 86400, 1)

    normalized_alpenglow = re.sub(r"\s+", " ", alpenglow_html).lower()
    recognized_status = any(
        status in normalized_alpenglow
        for status in ("in development", "under development")
    )
    if not recognized_status or "q3 2026" not in normalized_alpenglow:
        raise ValueError("Alpenglow page no longer exposes the expected status")
    status_match = re.search(
        r"^status\s*(?:\||:)\s*['\"]?([^'\"\r\n]+)",
        simd_text,
        re.MULTILINE | re.IGNORECASE,
    )
    if not status_match:
        raise ValueError("SIMD-0525 status is missing")
    simd_status = status_match.group(1).strip()

    return {
        "latest_official_solana_news_age_days": _metric(
            "latest_official_solana_news_age_days", "Latest official Solana news age",
            age_days, "days", "Elapsed days since the newest item in Solana's official RSS feed.",
            "It keeps current ecosystem developments visible without treating social sentiment as fact.",
            f"RSS latest item: {title}", link, collected_at,
            published.isoformat().replace("+00:00", "Z"),
            "This is one official editorial feed, not a complete view of community news or sentiment.",
        ),
        "alpenglow_upgrade_status": _metric(
            "alpenglow_upgrade_status", "Alpenglow upgrade status",
            "In development · Q3 2026", "official roadmap",
            "Current phase and expected activation window shown on Solana's official upgrade page.",
            "It tracks the named consensus upgrade without implying that a roadmap date is guaranteed.",
            "Alpenglow Phase 1 - Votor", ALPENGLOW_URL, collected_at, None,
            "Roadmap dates can move; announced development is not mainnet activation.",
        ),
        "simd_0525_status": _metric(
            "simd_0525_status", "SIMD-0525 shorter-slot proposal",
            simd_status, "proposal status",
            "Current status declared in the official SIMD-0525 proposal for staged shorter slots.",
            "It tracks a sponsor-named proposal that could materially change Solana latency.",
            "SIMD-0525 front matter", SIMD_0525_URL, collected_at, None,
            "A SIMD status is not proof that code is deployed or activated on mainnet.",
        ),
    }
