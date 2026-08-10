"""Build a deterministic plain-English briefing from validated evidence."""

from __future__ import annotations

from typing import Any


def build_grounded_briefing(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Summarize notable comparison records without generating new facts."""

    notable = [
        record
        for record in snapshot.get("anomalies", {}).values()
        if record.get("status") == "notable"
    ]
    notable.sort(key=lambda record: abs(record["observed_change_pct"]), reverse=True)
    supporting_ids = [record["metric_id"] for record in notable[:3]]
    if notable:
        phrases = []
        for record in notable[:3]:
            metric = snapshot["metrics"].get(record["metric_id"], {})
            label = metric.get("label", record["metric_id"])
            phrases.append(
                f"{label} {record['direction']} by "
                f"{abs(record['observed_change_pct']):.1f}%"
            )
        current_reading = "Notable seven-day movement: " + "; ".join(phrases) + "."
    else:
        current_reading = (
            "No verified comparison crossed the current review threshold."
        )
    unavailable_count = sum(
        record.get("status") == "unavailable"
        for record in snapshot.get("anomalies", {}).values()
    )
    uncertainty = (
        "Direction is not automatically good or bad, and this briefing cannot "
        "identify causes."
    )
    if unavailable_count:
        uncertainty += f" {unavailable_count} comparison(s) lack sufficient evidence."
    return {
        "status": "ok",
        "kind": "deterministic",
        "current_reading": current_reading,
        "supporting_metric_ids": supporting_ids,
        "uncertainty": uncertainty,
        "generated_at": snapshot["generated_at"],
        "model": "deterministic-observatory-v1",
    }
