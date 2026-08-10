import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.snapshot import build_network_snapshot, merge_network_snapshot


class SnapshotTests(unittest.TestCase):

    def test_network_refresh_preserves_verified_non_network_metrics(self):
        prior = {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-07T12:00:00Z",
            "summary": {"status": "healthy", "headline": "Old"},
            "metrics": {
                "daily_users": {
                    "id": "daily_users",
                    "section": "adoption",
                },
                "active_validators": {
                    "id": "active_validators",
                    "section": "validators",
                    "value": 10,
                },
                "stake_concentration": {
                    "id": "stake_concentration",
                    "section": "validators",
                    "value": 25,
                },
            },
        }
        fresh = {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-08T12:00:00Z",
            "summary": {"status": "healthy", "headline": "Fresh"},
            "metrics": {
                "rpc_health": {
                    "id": "rpc_health",
                    "section": "network",
                    "value": "ok",
                },
                "active_validators": {
                    "id": "active_validators",
                    "section": "validators",
                    "value": 11,
                },
            },
        }

        merged = merge_network_snapshot(prior, fresh)

        self.assertEqual(merged["generated_at"], fresh["generated_at"])
        self.assertEqual(merged["summary"], fresh["summary"])
        self.assertEqual(
            merged["metrics"]["daily_users"], prior["metrics"]["daily_users"]
        )
        self.assertEqual(
            merged["metrics"]["stake_concentration"],
            prior["metrics"]["stake_concentration"],
        )
        self.assertEqual(merged["metrics"]["active_validators"]["value"], 11)
        self.assertEqual(merged["metrics"]["rpc_health"]["value"], "ok")

    def test_network_refresh_upgrades_known_preserved_metrics(self):
        prior = {
            "schema_version": "0.2.0",
            "generated_at": "2026-08-08T12:00:00Z",
            "summary": {"status": "healthy", "headline": "Old"},
            "metrics": {
                "daily_unique_successful_fee_payers": {
                    "id": "daily_unique_successful_fee_payers",
                    "section": "adoption",
                    "label": "Daily unique successful fee payers",
                }
            },
        }
        fresh = {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-10T12:00:00Z",
            "summary": {"status": "healthy", "headline": "Fresh"},
            "metrics": {},
        }

        merged = merge_network_snapshot(prior, fresh)

        preserved = merged["metrics"]["daily_unique_successful_fee_payers"]
        self.assertIn("why_it_matters", preserved)
        self.assertIn("initiated", preserved["why_it_matters"].lower())
    def test_builds_provenance_rich_network_metrics(self):
        collected_at = "2026-07-27T22:00:00Z"
        rpc_results = {
            "getHealth": "ok",
            "getSlot": 355_000_000,
            "getBlockHeight": 330_000_000,
            "getEpochInfo": {
                "epoch": 812,
                "slotIndex": 100,
                "slotsInEpoch": 400,
            },
            "getRecentPerformanceSamples": [
                {
                    "numTransactions": 120_000,
                    "numNonVoteTransactions": 30_000,
                    "numSlots": 150,
                    "samplePeriodSecs": 60,
                }
            ],
            "getVoteAccounts": {
                "current": [{"votePubkey": "one"}, {"votePubkey": "two"}],
                "delinquent": [{"votePubkey": "three"}],
            },
        }

        snapshot = build_network_snapshot(rpc_results, collected_at)

        self.assertEqual(snapshot["schema_version"], "0.3.0")
        self.assertEqual(snapshot["generated_at"], collected_at)
        self.assertEqual(snapshot["metrics"]["rpc_health"]["value"], "ok")
        self.assertEqual(snapshot["metrics"]["estimated_tps"]["value"], 2000.0)
        self.assertEqual(
            snapshot["metrics"]["estimated_non_vote_tps"]["value"], 500.0
        )
        self.assertEqual(snapshot["metrics"]["epoch_progress"]["value"], 25.0)
        self.assertEqual(snapshot["metrics"]["active_validators"]["value"], 2)
        self.assertEqual(snapshot["metrics"]["delinquent_validators"]["value"], 1)
        self.assertEqual(
            snapshot["metrics"]["estimated_tps"]["source"]["method"],
            "getRecentPerformanceSamples",
        )
        self.assertIn(
            "votes",
            snapshot["metrics"]["estimated_tps"]["caveat"].lower(),
        )

    def test_builds_validator_depth_metrics_from_vote_account_stake(self):
        rpc_results = {
            "getHealth": "ok",
            "getSlot": 1,
            "getBlockHeight": 1,
            "getEpochInfo": {"epoch": 1, "slotIndex": 1, "slotsInEpoch": 2},
            "getRecentPerformanceSamples": [{"numTransactions": 10, "numNonVoteTransactions": 5, "numSlots": 2, "samplePeriodSecs": 1}],
            "getVoteAccounts": {
                "current": [{"votePubkey": "a", "activatedStake": 2_000_000_000, "commission": 5, "epochCredits": [[1, 10, 5]]}],
                "delinquent": [{"votePubkey": "b", "activatedStake": 1_000_000_000, "commission": 10, "epochCredits": []}],
            },
        }

        metrics = build_network_snapshot(
            rpc_results, "2026-08-10T12:00:00Z"
        )["metrics"]

        self.assertEqual(metrics["active_stake_sol"]["value"], 2.0)
        self.assertEqual(metrics["delinquent_stake_share_pct"]["value"], 33.33)
        self.assertEqual(metrics["superminority_coefficient"]["value"], 1)
        self.assertIn(
            "vote accounts",
            metrics["top_10_stake_share_pct"]["caveat"].lower(),
        )


if __name__ == "__main__":
    unittest.main()
