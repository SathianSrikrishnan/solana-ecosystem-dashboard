"""Direction-neutral review thresholds for verified comparison records."""

from __future__ import annotations

from typing import Any


def build_anomalies(
    comparisons: dict[str, dict[str, Any]], *, threshold_pct: float = 15.0
) -> dict[str, dict[str, Any]]:
    """Classify comparison movement for review without judging health."""

    if threshold_pct <= 0:
        raise ValueError("threshold_pct must be positive")
    records: dict[str, dict[str, Any]] = {}
    for metric_id, comparison in comparisons.items():
        change = comparison.get("percent_change")
        if comparison.get("status") != "ok" or change is None:
            records[metric_id] = {
                "metric_id": metric_id,
                "status": "unavailable",
                "direction": "unknown",
                "observed_change_pct": None,
                "threshold_pct": threshold_pct,
                "previous_window": comparison.get("previous_window"),
                "current_window": comparison.get("current_window"),
                "known_gap": comparison.get("reason") or "Percent change unavailable.",
                "caveat": "Missing comparison evidence is not a network anomaly.",
            }
            continue
        records[metric_id] = {
            "metric_id": metric_id,
            "status": (
                "notable" if abs(float(change)) >= threshold_pct else "within_range"
            ),
            "direction": comparison["direction"],
            "observed_change_pct": float(change),
            "threshold_pct": threshold_pct,
            "previous_window": comparison["previous_window"],
            "current_window": comparison["current_window"],
            "known_gap": None,
            "caveat": (
                "Crossing the review threshold is not a health verdict; "
                "the metric definition and companion evidence still matter."
            ),
        }
    return records
