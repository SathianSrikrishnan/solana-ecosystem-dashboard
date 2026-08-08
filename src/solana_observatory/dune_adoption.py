"""Normalize verified Dune adoption exports into dashboard metrics."""

from __future__ import annotations

import csv
from datetime import date, datetime, timedelta
from io import StringIO
from typing import Any


def _validate_context(collected_at: str, source_url: str) -> datetime:
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
    return collected_time


def _parse_daily_observations(
    csv_text: str,
    *,
    count_column: str,
    collected_time: datetime,
) -> list[dict[str, Any]]:
    required_columns = {"activity_date", count_column}

    reader = csv.DictReader(StringIO(csv_text))
    fieldnames = set(reader.fieldnames or [])
    if not required_columns.issubset(fieldnames):
        raise ValueError(f"Dune CSV must include activity_date and {count_column}")

    observations: dict[date, int] = {}
    for row in reader:
        date_text = (row.get("activity_date") or "").strip()
        count_text = (row.get(count_column) or "").strip()
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
                f"Invalid {count_column} count: {count_text}"
            ) from error
        if count < 0:
            raise ValueError(f"{count_column} cannot be negative")
        observations[activity_date] = count

    expected_dates = {
        collected_time.date() - timedelta(days=days_ago)
        for days_ago in range(1, 8)
    }
    if set(observations) != expected_dates:
        raise ValueError(
            "Dune CSV must contain the latest seven complete UTC days"
        )

    return [
        {"observed_at": observed_at.isoformat(), "value": observations[observed_at]}
        for observed_at in sorted(observations)
    ]


def parse_daily_fee_payers_csv(
    csv_text: str,
    *,
    collected_at: str,
    source_url: str,
) -> dict[str, Any]:
    """Return one normalized fee-payer metric from a Dune CSV export."""

    collected_time = _validate_context(collected_at, source_url)
    series = _parse_daily_observations(
        csv_text,
        count_column="unique_fee_payers",
        collected_time=collected_time,
    )
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


def parse_daily_successful_signers_csv(
    csv_text: str,
    *,
    collected_at: str,
    source_url: str,
) -> dict[str, Any]:
    """Return one normalized successful-signers metric from a Dune export."""

    collected_time = _validate_context(collected_at, source_url)
    series = _parse_daily_observations(
        csv_text,
        count_column="unique_successful_signers",
        collected_time=collected_time,
    )
    latest = series[-1]
    return {
        "id": "daily_unique_successful_signers",
        "section": "adoption",
        "label": "Daily unique successful signers",
        "value": latest["value"],
        "unit": "wallet addresses",
        "status": "ok",
        "definition": (
            "Distinct signer addresses on successful non-vote Solana "
            "transactions during the latest complete UTC day."
        ),
        "source": {
            "name": "Dune",
            "method": (
                "solana.transactions.signers / "
                "daily_unique_successful_signers.sql"
            ),
            "url": source_url,
        },
        "collected_at": collected_at,
        "source_time": latest["observed_at"],
        "confidence": "high",
        "caveat": (
            "Wallet addresses are not people: one person or bot can control "
            "many addresses, and one transaction may require several signers."
        ),
        "series": series,
    }


def parse_daily_jupiter_swap_csv(
    csv_text: str,
    *,
    collected_at: str,
    source_url: str,
) -> dict[str, dict[str, Any]]:
    """Return normalized Jupiter signer, overlap, and retention metrics."""

    collected_time = _validate_context(collected_at, source_url)
    users_series = _parse_daily_observations(
        csv_text,
        count_column="unique_jupiter_swap_signers",
        collected_time=collected_time,
    )
    overlap_series = _parse_daily_observations(
        csv_text,
        count_column="jupiter_fee_payer_overlap",
        collected_time=collected_time,
    )
    returning_series = _parse_daily_observations(
        csv_text,
        count_column="returning_jupiter_swap_signers",
        collected_time=collected_time,
    )

    return_rate_series = []
    for users, overlap, returning in zip(
        users_series, overlap_series, returning_series
    ):
        if overlap["value"] > users["value"]:
            raise ValueError("Jupiter fee-payer overlap cannot exceed users")
        if returning["value"] > users["value"]:
            raise ValueError("Returning Jupiter signers cannot exceed users")
        if users["value"] == 0 and (overlap["value"] or returning["value"]):
            raise ValueError("A zero-user day must have zero overlap and returns")
        return_rate = (
            0.0
            if users["value"] == 0
            else round(returning["value"] / users["value"] * 100, 2)
        )
        return_rate_series.append(
            {"observed_at": users["observed_at"], "value": return_rate}
        )

    source = {
        "name": "Dune",
        "method": (
            "jupiter_solana.aggregator_swaps + solana.transactions / "
            "daily_jupiter_swap_signers.sql"
        ),
        "url": source_url,
    }
    latest_date = users_series[-1]["observed_at"]

    def metric(
        *,
        metric_id: str,
        label: str,
        unit: str,
        definition: str,
        caveat: str,
        series: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "id": metric_id,
            "section": "adoption",
            "label": label,
            "value": series[-1]["value"],
            "unit": unit,
            "status": "ok",
            "definition": definition,
            "source": dict(source),
            "collected_at": collected_at,
            "source_time": latest_date,
            "confidence": "high",
            "caveat": caveat,
            "series": series,
        }

    metrics = [
        metric(
            metric_id="daily_unique_jupiter_swap_signers",
            label="Daily unique Jupiter Swap signers",
            unit="wallet addresses",
            definition=(
                "Distinct tx_signer addresses on intended swaps recorded by "
                "Dune's curated Jupiter aggregator table during the latest "
                "complete UTC day."
            ),
            caveat=(
                "Wallet addresses are not people, and this measures Jupiter "
                "Swap signers rather than users of a particular wallet app."
            ),
            series=users_series,
        ),
        metric(
            metric_id="daily_jupiter_fee_payer_overlap",
            label="Jupiter signer and fee-payer overlap",
            unit="wallet addresses",
            definition=(
                "Jupiter Swap signer addresses that were also the successful "
                "transaction fee payer on the same UTC day."
            ),
            caveat=(
                "This is an address intersection, not a count of people; "
                "sponsored or relayed transactions can fall outside it."
            ),
            series=overlap_series,
        ),
        metric(
            metric_id="jupiter_swap_signer_7d_return_rate",
            label="Jupiter Swap seven-day return rate",
            unit="percent",
            definition=(
                "Share of the day's Jupiter Swap signer addresses also seen "
                "at least once during the preceding seven complete UTC days."
            ),
            caveat=(
                "Returning addresses are not necessarily returning people; "
                "bots and one person using several wallets remain included."
            ),
            series=return_rate_series,
        ),
    ]
    return {item["id"]: item for item in metrics}
