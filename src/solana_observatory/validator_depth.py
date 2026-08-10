"""Deterministic stake-distribution calculations from getVoteAccounts."""

from __future__ import annotations

import math
from statistics import median
from typing import Any


LAMPORTS_PER_SOL = 1_000_000_000


def _valid_stake(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value) or value < 0 or int(value) != value:
        return None
    return int(value)


def _has_recent_vote_credits(account: dict[str, Any]) -> bool:
    credits = account.get("epochCredits")
    if not isinstance(credits, list) or not credits:
        return False
    latest = credits[-1]
    return (
        isinstance(latest, list)
        and len(latest) >= 3
        and all(isinstance(value, int) and not isinstance(value, bool) for value in latest[:3])
        and latest[1] > latest[2]
    )


def calculate_validator_depth(vote_accounts: dict[str, Any]) -> dict[str, Any]:
    """Calculate stake and participation indicators without inferring operators."""

    seen: set[str] = set()
    current: list[tuple[dict[str, Any], int]] = []
    delinquent: list[tuple[dict[str, Any], int]] = []
    ignored_invalid = 0
    ignored_duplicates = 0
    for group_name, target in (("current", current), ("delinquent", delinquent)):
        group = vote_accounts.get(group_name, [])
        if not isinstance(group, list):
            group = []
        for account in group:
            if not isinstance(account, dict):
                ignored_invalid += 1
                continue
            pubkey = account.get("votePubkey")
            if not isinstance(pubkey, str) or not pubkey:
                ignored_invalid += 1
                continue
            if pubkey in seen:
                ignored_duplicates += 1
                continue
            seen.add(pubkey)
            stake = _valid_stake(account.get("activatedStake"))
            if stake is None:
                ignored_invalid += 1
                continue
            target.append((account, stake))

    active_stake = sum(stake for _, stake in current)
    delinquent_stake = sum(stake for _, stake in delinquent)
    total_stake = active_stake + delinquent_stake
    all_stakes = sorted(
        (stake for _, stake in current + delinquent), reverse=True
    )

    def share(count: int) -> float | None:
        if total_stake == 0:
            return None
        return round(sum(all_stakes[:count]) / total_stake * 100, 2)

    superminority = None
    if total_stake:
        cumulative = 0
        for index, stake in enumerate(all_stakes, start=1):
            cumulative += stake
            if cumulative * 3 >= total_stake:
                superminority = index
                break

    commissions = [
        float(account["commission"])
        for account, _ in current
        if isinstance(account.get("commission"), (int, float))
        and not isinstance(account.get("commission"), bool)
        and math.isfinite(account["commission"])
        and 0 <= account["commission"] <= 100
    ]
    credited_stake = sum(
        stake for account, stake in current if _has_recent_vote_credits(account)
    )
    ranked_accounts = sorted(
        (
            (account, stake, status)
            for status, accounts in (("current", current), ("delinquent", delinquent))
            for account, stake in accounts
        ),
        key=lambda item: (-item[1], item[0]["votePubkey"]),
    )[:10]
    leaderboard = []
    for rank, (account, stake, status) in enumerate(ranked_accounts, start=1):
        commission = account.get("commission")
        valid_commission = (
            isinstance(commission, (int, float))
            and not isinstance(commission, bool)
            and math.isfinite(commission)
            and 0 <= commission <= 100
        )
        leaderboard.append(
            {
                "rank": rank,
                "vote_pubkey": account["votePubkey"],
                "activated_stake_sol": round(stake / LAMPORTS_PER_SOL, 2),
                "stake_share_pct": (
                    None if total_stake == 0 else round(stake / total_stake * 100, 2)
                ),
                "commission_pct": float(commission) if valid_commission else None,
                "status": status,
            }
        )
    return {
        "active_stake_sol": round(active_stake / LAMPORTS_PER_SOL, 2),
        "delinquent_stake_sol": round(delinquent_stake / LAMPORTS_PER_SOL, 2),
        "delinquent_stake_share_pct": (
            None if total_stake == 0 else round(delinquent_stake / total_stake * 100, 2)
        ),
        "top_10_stake_share_pct": share(10),
        "top_25_stake_share_pct": share(25),
        "superminority_coefficient": superminority,
        "median_commission_pct": (
            None if not commissions else round(float(median(commissions)), 2)
        ),
        "vote_credit_coverage_pct": (
            None if active_stake == 0 else round(credited_stake / active_stake * 100, 2)
        ),
        "ignored_invalid_accounts": ignored_invalid,
        "ignored_duplicate_accounts": ignored_duplicates,
        "valid_accounts": len(current) + len(delinquent),
        "leaderboard": leaderboard,
    }
