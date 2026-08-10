"""Normalize direct Solana RPC results into provenance-rich metrics."""

from __future__ import annotations

from typing import Any

from .validator_depth import calculate_validator_depth


WHY_IT_MATTERS_MIGRATION = {
    "daily_unique_successful_fee_payers": (
        "Fee payers approximate how many distinct addresses initiated "
        "successful activity and paid for execution."
    ),
    "daily_unique_successful_signers": (
        "Successful signers capture a broader set of participating addresses "
        "than fee payers alone."
    ),
    "daily_unique_jupiter_swap_signers": (
        "It shows the scale of intended swap activity through one of Solana's "
        "major application routes."
    ),
    "daily_jupiter_fee_payer_overlap": (
        "The overlap reveals how often the visible application signer also "
        "pays the transaction fee."
    ),
    "jupiter_swap_signer_7d_return_rate": (
        "Return rate distinguishes repeat use from one-time address activity."
    ),
    "sol_price_usd": (
        "Price supplies market context for SOL-denominated capital and "
        "validator economics."
    ),
    "solana_defi_tvl_usd": (
        "TVL shows how much capital is deposited in tracked Solana DeFi "
        "protocols."
    ),
    "solana_stablecoin_value_usd": (
        "Stablecoin value shows the dollar-like liquidity available for "
        "trading, saving, and settlement on Solana."
    ),
    "solana_dex_volume_usd": (
        "DEX volume shows how much spot exchange activity occurred across "
        "tracked Solana venues."
    ),
}


def merge_network_snapshot(
    prior_snapshot: dict[str, Any], fresh_snapshot: dict[str, Any]
) -> dict[str, Any]:
    """Replace refreshed RPC metrics while preserving other verified metrics."""
    merged = {
        **prior_snapshot,
        "schema_version": fresh_snapshot["schema_version"],
        "generated_at": fresh_snapshot["generated_at"],
        "summary": fresh_snapshot["summary"],
        "metrics": {
            metric_id: {
                **metric,
                **(
                    {"why_it_matters": WHY_IT_MATTERS_MIGRATION[metric_id]}
                    if "why_it_matters" not in metric
                    and metric_id in WHY_IT_MATTERS_MIGRATION
                    else {}
                ),
            }
            for metric_id, metric in prior_snapshot.get("metrics", {}).items()
        },
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
    why_it_matters: str,
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
        "why_it_matters": why_it_matters,
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
    validator_depth = calculate_validator_depth(vote_accounts)

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
            why_it_matters=(
                "It is the first check that the dashboard's live network "
                "data path is responding normally."
            ),
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
            why_it_matters=(
                "A rising slot confirms that this observer sees the chain "
                "continuing to advance."
            ),
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
            why_it_matters=(
                "Block height is a second progress marker that helps detect "
                "a stalled or lagging data source."
            ),
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
            why_it_matters=(
                "Epoch progress provides timing context for validator "
                "rewards, stake activation, and network operations."
            ),
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
            why_it_matters=(
                "Total throughput shows network load, but must be separated "
                "from user activity because it includes validator votes."
            ),
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
            why_it_matters=(
                "This is the closest live RPC measure of application and "
                "user transaction throughput."
            ),
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
            why_it_matters=(
                "Slot time indicates how quickly the chain is advancing in "
                "the most recent sample."
            ),
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
            why_it_matters=(
                "Active vote accounts show how many validators are currently "
                "participating, before considering stake concentration."
            ),
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
            why_it_matters=(
                "Delinquency is an early operational signal that part of the "
                "validator set is falling behind."
            ),
            method="getVoteAccounts",
            collected_at=collected_at,
            caveat="Temporary delinquency can recover and is not automatically malicious behavior.",
        ),
    }

    usable_depth = validator_depth["valid_accounts"] > 0
    depth_specs = {
        "active_stake_sol": (
            "Active stake",
            "SOL",
            "Activated stake assigned to currently active vote accounts.",
            "It shows how much voting power is currently participating.",
            "Vote accounts are not necessarily distinct operators or organizations.",
        ),
        "delinquent_stake_sol": (
            "Delinquent stake",
            "SOL",
            "Activated stake assigned to vote accounts currently classified as delinquent.",
            "It sizes the voting power currently failing to participate normally.",
            "Delinquency can be temporary and does not imply malicious behavior.",
        ),
        "delinquent_stake_share_pct": (
            "Delinquent stake share",
            "percent",
            "Delinquent activated stake as a share of all activated stake in this response.",
            "Stake share is more meaningful than a raw delinquent-validator count.",
            "One RPC snapshot can change quickly as validators recover or fall behind.",
        ),
        "top_10_stake_share_pct": (
            "Top 10 stake share",
            "percent",
            "Share of activated stake assigned to the ten largest vote accounts.",
            "It exposes concentration hidden by the total validator count.",
            "Vote accounts are not operators; one organization may control several accounts.",
        ),
        "top_25_stake_share_pct": (
            "Top 25 stake share",
            "percent",
            "Share of activated stake assigned to the twenty-five largest vote accounts.",
            "It provides a broader view of stake concentration beyond the largest validators.",
            "Vote accounts are not operators and ownership identity is not inferred.",
        ),
        "superminority_coefficient": (
            "Stake superminority coefficient",
            "vote accounts",
            "Minimum largest vote accounts whose combined activated stake reaches one third.",
            "A larger value means more vote accounts are required to reach consensus-blocking stake.",
            "This is calculated by vote account, not verified independent operator.",
        ),
        "median_commission_pct": (
            "Median validator commission",
            "percent",
            "Median advertised commission among active vote accounts with valid values.",
            "Commission affects how staking rewards are divided between validators and delegators.",
            "The median does not include operating cost, MEV, or total validator profitability.",
        ),
        "vote_credit_coverage_pct": (
            "Stake with recent vote credits",
            "percent",
            "Share of active stake on vote accounts whose latest epoch-credit record increased.",
            "It checks whether active voting power shows evidence of recent vote participation.",
            "One credit record is a bounded participation check, not a full performance history.",
        ),
    }
    for metric_id, (label, unit, definition, why, caveat) in depth_specs.items():
        metrics[metric_id] = _metric(
            metric_id=metric_id,
            section="validators",
            label=label,
            value=validator_depth[metric_id] if usable_depth else None,
            unit=unit,
            definition=definition,
            why_it_matters=why,
            method="getVoteAccounts",
            collected_at=collected_at,
            caveat=caveat,
        )

    health = rpc_results["getHealth"]
    summary_status = "healthy" if health == "ok" else "attention"
    headline = (
        "The selected Solana RPC endpoint reports healthy."
        if health == "ok"
        else "The selected Solana RPC endpoint needs attention."
    )

    return {
        "schema_version": "0.3.0",
        "generated_at": collected_at,
        "summary": {"status": summary_status, "headline": headline},
        "metrics": metrics,
    }
