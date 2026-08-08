"""Normalize direct Solana RPC results into provenance-rich metrics."""

from __future__ import annotations

from typing import Any


def merge_network_snapshot(
    prior_snapshot: dict[str, Any], fresh_snapshot: dict[str, Any]
) -> dict[str, Any]:
    """Replace refreshed RPC metrics while preserving other verified metrics."""
    merged = {
        **prior_snapshot,
        "schema_version": fresh_snapshot["schema_version"],
        "generated_at": fresh_snapshot["generated_at"],
        "summary": fresh_snapshot["summary"],
        "metrics": dict(prior_snapshot.get("metrics", {})),
    }
    merged["metrics"].update(fresh_snapshot["metrics"])
    return merged


RPC_URL = "https://api.mainnet-beta.solana.com"


def _metric(
    *,
    metric_id: str,
    section: str,
    label: str,
    value: Any,
    unit: str,
    definition: str,
    method: str,
    collected_at: str,
    caveat: str,
    confidence: str = "high",
) -> dict[str, Any]:
    return {
        "id": metric_id,
        "section": section,
        "label": label,
        "value": value,
        "unit": unit,
        "status": "ok" if value is not None else "unavailable",
        "definition": definition,
        "source": {
            "name": "Solana JSON-RPC",
            "method": method,
            "url": RPC_URL,
        },
        "collected_at": collected_at,
        "source_time": None,
        "confidence": confidence,
        "caveat": caveat,
        "series": [],
    }


def build_network_snapshot(
    rpc_results: dict[str, Any], collected_at: str
) -> dict[str, Any]:
    """Build the first normalized snapshot from direct RPC method results."""

    epoch_info = rpc_results["getEpochInfo"]
    performance = rpc_results["getRecentPerformanceSamples"][0]
    vote_accounts = rpc_results["getVoteAccounts"]

    sample_period = performance["samplePeriodSecs"]
    estimated_tps = performance["numTransactions"] / sample_period
    estimated_non_vote_tps = (
        performance["numNonVoteTransactions"] / sample_period
    )
    estimated_slot_time = sample_period / performance["numSlots"]
    epoch_progress = (
        epoch_info["slotIndex"] / epoch_info["slotsInEpoch"] * 100
    )

    metrics = {
        "rpc_health": _metric(
            metric_id="rpc_health",
            section="network",
            label="RPC health",
            value=rpc_results["getHealth"],
            unit="status",
            definition="Health response from the selected public RPC node.",
            method="getHealth",
            collected_at=collected_at,
            caveat="This checks one public RPC endpoint, not every validator.",
        ),
        "current_slot": _metric(
            metric_id="current_slot",
            section="network",
            label="Current slot",
            value=rpc_results["getSlot"],
            unit="slot",
            definition="Latest slot reported by the selected public RPC node.",
            method="getSlot",
            collected_at=collected_at,
            caveat="Different RPC nodes can be a few slots apart.",
        ),
        "block_height": _metric(
            metric_id="block_height",
            section="network",
            label="Block height",
            value=rpc_results["getBlockHeight"],
            unit="block",
            definition="Current block height reported by the selected RPC node.",
            method="getBlockHeight",
            collected_at=collected_at,
            caveat="This is network progress, not a measure of user adoption.",
        ),
        "epoch_progress": _metric(
            metric_id="epoch_progress",
            section="network",
            label="Epoch progress",
            value=round(epoch_progress, 2),
            unit="percent",
            definition="Share of the current epoch's slots already completed.",
            method="getEpochInfo",
            collected_at=collected_at,
            caveat="Epoch progress describes validator timing, not economic growth.",
        ),
        "estimated_tps": _metric(
            metric_id="estimated_tps",
            section="network",
            label="Estimated total TPS",
            value=round(estimated_tps, 2),
            unit="transactions/second",
            definition="All transactions in the latest RPC performance sample divided by sample seconds.",
            method="getRecentPerformanceSamples",
            collected_at=collected_at,
            caveat="Includes validator votes, so it is not the same as user activity.",
        ),
        "estimated_non_vote_tps": _metric(
            metric_id="estimated_non_vote_tps",
            section="network",
            label="Estimated non-vote TPS",
            value=round(estimated_non_vote_tps, 2),
            unit="transactions/second",
            definition="Non-vote transactions in the latest RPC performance sample divided by sample seconds.",
            method="getRecentPerformanceSamples",
            collected_at=collected_at,
            caveat="Non-vote transactions can still include bots and automated programs.",
        ),
        "estimated_slot_time": _metric(
            metric_id="estimated_slot_time",
            section="network",
            label="Estimated slot time",
            value=round(estimated_slot_time, 3),
            unit="seconds",
            definition="Latest performance sample duration divided by slots produced.",
            method="getRecentPerformanceSamples",
            collected_at=collected_at,
            caveat="This is a short recent estimate and can move between samples.",
        ),
        "active_validators": _metric(
            metric_id="active_validators",
            section="validators",
            label="Active validators",
            value=len(vote_accounts["current"]),
            unit="validators",
            definition="Vote accounts currently classified as active by the RPC response.",
            method="getVoteAccounts",
            collected_at=collected_at,
            caveat="A validator count does not describe how evenly stake is distributed.",
        ),
        "delinquent_validators": _metric(
            metric_id="delinquent_validators",
            section="validators",
            label="Delinquent validators",
            value=len(vote_accounts["delinquent"]),
            unit="validators",
            definition="Vote accounts currently classified as delinquent by the RPC response.",
            method="getVoteAccounts",
            collected_at=collected_at,
            caveat="Temporary delinquency can recover and is not automatically malicious behavior.",
        ),
    }

    health = rpc_results["getHealth"]
    summary_status = "healthy" if health == "ok" else "attention"
    headline = (
        "The selected Solana RPC endpoint reports healthy."
        if health == "ok"
        else "The selected Solana RPC endpoint needs attention."
    )

    return {
        "schema_version": "0.2.0",
        "generated_at": collected_at,
        "summary": {"status": summary_status, "headline": headline},
        "metrics": metrics,
    }
