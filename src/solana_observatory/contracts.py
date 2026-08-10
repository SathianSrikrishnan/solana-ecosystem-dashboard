"""Validation for the shared collector-to-interface data contract."""

from __future__ import annotations

from typing import Any


REQUIRED_SNAPSHOT_FIELDS = {
    "schema_version",
    "generated_at",
    "summary",
    "metrics",
}
REQUIRED_METRIC_FIELDS = {
    "id",
    "section",
    "label",
    "value",
    "unit",
    "definition",
    "why_it_matters",
    "source",
    "collected_at",
    "source_time",
    "status",
    "confidence",
    "caveat",
    "series",
}
VALID_SECTIONS = {
    "network",
    "adoption",
    "economy",
    "validators",
    "ecosystem",
    "financial_rails",
}
VALID_STATUSES = {"ok", "stale", "unavailable", "error"}
VALID_CONFIDENCE = {"high", "medium", "experimental"}
CURRENT_SCHEMA_VERSION = "0.3.0"
REQUIRED_COMPARISON_FIELDS = {
    "metric_id",
    "status",
    "grain",
    "current_average",
    "previous_average",
    "absolute_change",
    "percent_change",
    "direction",
    "previous_window",
    "current_window",
    "reason",
}
REQUIRED_ANOMALY_FIELDS = {
    "metric_id",
    "status",
    "direction",
    "observed_change_pct",
    "threshold_pct",
    "previous_window",
    "current_window",
    "known_gap",
    "caveat",
}
REQUIRED_ANALYSIS_FIELDS = {
    "status",
    "current_reading",
    "supporting_metric_ids",
    "uncertainty",
    "generated_at",
    "model",
}


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    """Raise ValueError when a snapshot cannot be safely rendered."""

    missing_snapshot_fields = REQUIRED_SNAPSHOT_FIELDS - snapshot.keys()
    if missing_snapshot_fields:
        fields = ", ".join(sorted(missing_snapshot_fields))
        raise ValueError(f"Snapshot is missing required fields: {fields}")

    if not isinstance(snapshot["metrics"], dict):
        raise ValueError("Snapshot metrics must be a dictionary")
    if snapshot["schema_version"] != CURRENT_SCHEMA_VERSION:
        raise ValueError(
            f"Snapshot schema version must be {CURRENT_SCHEMA_VERSION}"
        )

    for metric_key, metric in snapshot["metrics"].items():
        missing_metric_fields = REQUIRED_METRIC_FIELDS - metric.keys()
        if missing_metric_fields:
            fields = ", ".join(sorted(missing_metric_fields))
            raise ValueError(
                f"Metric {metric_key} is missing required fields: {fields}"
            )

        if metric["id"] != metric_key:
            raise ValueError(
                f"Metric id {metric['id']} must match its dictionary key "
                f"{metric_key}"
            )
        if metric["section"] not in VALID_SECTIONS:
            raise ValueError(
                f"Metric {metric_key} has unknown section {metric['section']}"
            )
        if metric["status"] not in VALID_STATUSES:
            raise ValueError(
                f"Metric {metric_key} has unknown status {metric['status']}"
            )
        if metric["confidence"] not in VALID_CONFIDENCE:
            raise ValueError(
                f"Metric {metric_key} has unknown confidence "
                f"{metric['confidence']}"
            )
        if not isinstance(metric["series"], list):
            raise ValueError(f"Metric {metric_key} series must be a list")

        source = metric["source"]
        if not isinstance(source, dict) or not {
            "name",
            "method",
            "url",
        }.issubset(source):
            raise ValueError(
                f"Metric {metric_key} source must include name, method, and url"
            )

    leaderboard = snapshot.get("validator_leaderboard")
    if leaderboard is not None:
        if not isinstance(leaderboard, dict) or not {
            "collected_at", "source", "caveat", "records"
        }.issubset(leaderboard):
            raise ValueError("Validator leaderboard is missing required fields")
        if not isinstance(leaderboard["records"], list) or len(leaderboard["records"]) > 10:
            raise ValueError("Validator leaderboard records must be a top-ten list")
        source = leaderboard["source"]
        if not isinstance(source, dict) or not {"name", "method", "url"}.issubset(source):
            raise ValueError("Validator leaderboard source is invalid")
        for expected_rank, record in enumerate(leaderboard["records"], start=1):
            if not isinstance(record, dict) or not {
                "rank", "vote_pubkey", "activated_stake_sol", "stake_share_pct",
                "commission_pct", "status"
            }.issubset(record):
                raise ValueError("Validator leaderboard record is missing fields")
            if record["rank"] != expected_rank:
                raise ValueError("Validator leaderboard rank must be sequential")
            if not isinstance(record["vote_pubkey"], str) or not record["vote_pubkey"]:
                raise ValueError("Validator leaderboard vote pubkey is invalid")
            if record["status"] not in {"current", "delinquent"}:
                raise ValueError("Validator leaderboard status is invalid")

    comparisons = snapshot.get("comparisons", {})
    if not isinstance(comparisons, dict):
        raise ValueError("Snapshot comparisons must be a dictionary")
    for comparison_key, comparison in comparisons.items():
        if comparison_key not in snapshot["metrics"]:
            raise ValueError(
                f"Comparison {comparison_key} references an unknown metric"
            )
        if not isinstance(comparison, dict):
            raise ValueError(f"Comparison {comparison_key} must be a dictionary")
        missing_fields = REQUIRED_COMPARISON_FIELDS - comparison.keys()
        if missing_fields:
            fields = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Comparison {comparison_key} is missing required fields: {fields}"
            )
        if comparison["metric_id"] != comparison_key:
            raise ValueError(
                f"Comparison metric id must match its key {comparison_key}"
            )
        if comparison["status"] not in {"ok", "unavailable"}:
            raise ValueError(
                f"Comparison {comparison_key} has unknown status"
            )
        if comparison["direction"] not in {
            "increased",
            "decreased",
            "flat",
            "unknown",
        }:
            raise ValueError(
                f"Comparison {comparison_key} has unknown direction"
            )

    anomalies = snapshot.get("anomalies", {})
    if not isinstance(anomalies, dict):
        raise ValueError("Snapshot anomalies must be a dictionary")
    for anomaly_key, anomaly in anomalies.items():
        if anomaly_key not in snapshot["metrics"]:
            raise ValueError(f"Anomaly {anomaly_key} references an unknown metric")
        if not isinstance(anomaly, dict):
            raise ValueError(f"Anomaly {anomaly_key} must be a dictionary")
        missing_fields = REQUIRED_ANOMALY_FIELDS - anomaly.keys()
        if missing_fields:
            fields = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Anomaly {anomaly_key} is missing required fields: {fields}"
            )
        if anomaly["metric_id"] != anomaly_key:
            raise ValueError(f"Anomaly metric id must match its key {anomaly_key}")
        if anomaly["status"] not in {"notable", "within_range", "unavailable"}:
            raise ValueError(f"Anomaly {anomaly_key} has unknown status")

    analysis = snapshot.get("analysis")
    if analysis is not None:
        if not isinstance(analysis, dict):
            raise ValueError("Snapshot analysis must be a dictionary")
        missing_fields = REQUIRED_ANALYSIS_FIELDS - analysis.keys()
        if missing_fields:
            fields = ", ".join(sorted(missing_fields))
            raise ValueError(f"Analysis is missing required fields: {fields}")
        evidence_ids = analysis["supporting_metric_ids"]
        if not isinstance(evidence_ids, list):
            raise ValueError("Analysis evidence IDs must be a list")
        if any(metric_id not in snapshot["metrics"] for metric_id in evidence_ids):
            raise ValueError("Analysis references unknown evidence")

