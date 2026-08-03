"""Normalize verified Dune adoption exports into dashboard metrics."""

from __future__ import annotations

import csv
from datetime import date, datetime, timedelta
from io import StringIO
from typing import Any


REQUIRED_COLUMNS = {"activity_date", "unique_fee_payers"}


def parse_daily_fee_payers_csv(
    csv_text: str,
    *,
    collected_at: str,
    source_url: str,
) -> dict[str, Any]:
    """Return one normalized adoption metric from a Dune CSV export."""

    try:
        collected_time = datetime.fromisoformat(
            collected_at.replace("Z", "+00:00")
        )
    except ValueError as error:
        raise ValueError("collected_at must be an ISO-8601 timestamp") from error
    if collected_time.tzinfo is None:
        raise ValueError("collected_at must include a timezone")
    if not source_url.startswith(("https://dune.com/", "https://www.dune.com/")):
        raise ValueError("source_url must be a public Dune URL")

    reader = csv.DictReader(StringIO(csv_text))
    fieldnames = set(reader.fieldnames or [])
    if not REQUIRED_COLUMNS.issubset(fieldnames):
        raise ValueError(
            "Dune CSV must include activity_date and unique_fee_payers"
        )

    observations: dict[date, int] = {}
    for row in reader:
        date_text = (row.get("activity_date") or "").strip()
        count_text = (row.get("unique_fee_payers") or "").strip()
        try:
            activity_date = date.fromisoformat(date_text)
        except ValueError as error:
            raise ValueError(f"Invalid activity_date: {date_text}") from error
        if activity_date in observations:
            raise ValueError(f"Dune CSV contains duplicate date: {date_text}")
        try:
            count = int(count_text)
        except ValueError as error:
            raise ValueError(
                f"Invalid unique_fee_payers count: {count_text}"
            ) from error
        if count < 0:
            raise ValueError("unique_fee_payers cannot be negative")
        observations[activity_date] = count

    expected_dates = {
        collected_time.date() - timedelta(days=days_ago)
        for days_ago in range(1, 8)
    }
    if set(observations) != expected_dates:
        raise ValueError(
            "Dune CSV must contain the latest seven complete UTC days"
        )

    series = [
        {"observed_at": observed_at.isoformat(), "value": observations[observed_at]}
        for observed_at in sorted(observations)
    ]
    latest = series[-1]
    return {
        "id": "daily_unique_successful_fee_payers",
        "section": "adoption",
        "label": "Daily unique successful fee payers",
        "value": latest["value"],
        "unit": "wallet addresses",
        "status": "ok",
        "definition": (
            "Distinct primary signer (fee payer) addresses on successful "
            "non-vote Solana transactions during the latest complete UTC day."
        ),
        "source": {
            "name": "Dune",
            "method": "solana.transactions / daily_unique_fee_payers.sql",
            "url": source_url,
        },
        "collected_at": collected_at,
        "source_time": latest["observed_at"],
        "confidence": "high",
        "caveat": (
            "Wallet addresses are not people: one person or bot can control "
            "many addresses, and relayers may pay fees for others."
        ),
        "series": series,
    }
