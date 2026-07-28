import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.snapshot import build_network_snapshot


class SnapshotTests(unittest.TestCase):
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

        self.assertEqual(snapshot["schema_version"], "0.2.0")
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


if __name__ == "__main__":
    unittest.main()
