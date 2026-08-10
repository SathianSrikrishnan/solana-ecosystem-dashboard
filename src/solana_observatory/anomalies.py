"""Direction-neutral review thresholds for verified comparison records."""

from __future__ import annotations

from typing import Any


THRESHOLD_RULES = {
    "estimated_non_vote_tps_vs_recent_median_pct": (25.0, "absolute", "TPS change"),
    "estimated_slot_time_vs_recent_median_pct": (20.0, "absolute", "slot-time change"),
    "delinquent_stake_share_pct": (5.0, "upper", "delinquent stake share"),
    "sol_price_24h_change_pct": (10.0, "absolute", "SOL 24-hour price move"),
}


def build_threshold_anomalies(
    metrics: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Evaluate sponsor-named operational signals against explicit rules."""
    records: dict[str, dict[str, Any]] = {}
    for metric_id, (threshold, mode, label) in THRESHOLD_RULES.items():
        if metric_id not in metrics:
            continue
        metric = metrics.get(metric_id, {})
        raw_value = metric.get("value")
        if metric.get("status") != "ok" or not isinstance(raw_value, (int, float)):
            records[metric_id] = {
                "metric_id": metric_id, "status": "unavailable", "direction": "unknown",
                "observed_change_pct": None, "threshold_pct": threshold,
                "previous_window": None, "current_window": None,
                "known_gap": "Current verified measurement unavailable.",
                "caveat": "Unavailable evidence is not an anomaly.",
                "kind": "threshold", "message": f"{label} could not be evaluated.",
            }
            continue
        value = float(raw_value)
        notable = abs(value) >= threshold if mode == "absolute" else value >= threshold
        direction = "increased" if value > 0 else "decreased" if value < 0 else "flat"
        records[metric_id] = {
            "metric_id": metric_id, "status": "notable" if notable else "within_range",
            "direction": direction, "observed_change_pct": value,
            "threshold_pct": threshold, "previous_window": None, "current_window": None,
            "known_gap": None,
            "caveat": "Crossing a review threshold is not automatically a health verdict.",
            "kind": "threshold",
            "message": f"{label} {'crossed' if notable else 'remained within'} its {threshold:g}% review threshold.",
        }
    return records


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
