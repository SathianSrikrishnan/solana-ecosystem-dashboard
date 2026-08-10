import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.contracts import validate_snapshot
from solana_observatory.snapshot import build_network_snapshot


class ContractTests(unittest.TestCase):
    def test_contract_requires_current_schema_and_why_it_matters(self):
        snapshot = {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-10T12:00:00Z",
            "summary": {"status": "healthy", "headline": "Healthy."},
            "metrics": {
                "rpc_health": {
                    "id": "rpc_health",
                    "section": "network",
                    "label": "RPC health",
                    "value": "ok",
                    "unit": "status",
                    "definition": "Health reported by one RPC node.",
                    "source": {
                        "name": "Solana JSON-RPC",
                        "method": "getHealth",
                        "url": "https://api.mainnet-beta.solana.com",
                    },
                    "collected_at": "2026-08-10T12:00:00Z",
                    "source_time": None,
                    "status": "ok",
                    "confidence": "high",
                    "caveat": "One node is not the whole network.",
                    "series": [],
                }
            },
        }

        with self.assertRaisesRegex(ValueError, "why_it_matters"):
            validate_snapshot(snapshot)

        snapshot["metrics"]["rpc_health"]["why_it_matters"] = (
            "It is the first check that the selected data path is usable."
        )
        validate_snapshot(snapshot)

        snapshot["schema_version"] = "0.2.0"
        with self.assertRaisesRegex(ValueError, "schema version"):
            validate_snapshot(snapshot)

    def test_network_snapshot_satisfies_shared_metric_contract(self):
        snapshot = build_network_snapshot(
            {
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
                    "current": [{"votePubkey": "one"}],
                    "delinquent": [],
                },
            },
            "2026-07-27T22:00:00Z",
        )

        validate_snapshot(snapshot)

        metric = snapshot["metrics"]["estimated_non_vote_tps"]
        self.assertEqual(metric["id"], "estimated_non_vote_tps")
        self.assertEqual(metric["section"], "network")
        self.assertIsNone(metric["source_time"])
        self.assertEqual(metric["series"], [])

    def test_contract_rejects_a_metric_without_provenance(self):
        snapshot = {
            "schema_version": "0.3.0",
            "generated_at": "2026-07-27T22:00:00Z",
            "summary": {"status": "healthy", "headline": "Healthy."},
            "metrics": {
                "daily_fee_payers": {
                    "id": "daily_fee_payers",
                    "section": "adoption",
                    "label": "Daily fee payers",
                    "value": 10,
                    "unit": "wallets",
                }
            },
        }

        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate_snapshot(snapshot)

    def test_contract_rejects_a_metric_key_id_mismatch(self):
        snapshot = {
            "schema_version": "0.3.0",
            "generated_at": "2026-07-27T22:00:00Z",
            "summary": {"status": "healthy", "headline": "Healthy."},
            "metrics": {
                "daily_fee_payers": {
                    "id": "daily_signers",
                    "section": "adoption",
                    "label": "Daily fee payers",
                    "value": 10,
                    "unit": "wallets",
                    "definition": "Wallets that paid a transaction fee.",
                    "why_it_matters": "It measures initiated activity.",
                    "source": {"name": "Dune", "method": "query:123", "url": ""},
                    "collected_at": "2026-07-27T22:00:00Z",
                    "source_time": "2026-07-27",
                    "status": "ok",
                    "confidence": "high",
                    "caveat": "Wallets are not people.",
                    "series": [],
                }
            },
        }

        with self.assertRaisesRegex(ValueError, "must match its dictionary key"):
            validate_snapshot(snapshot)


if __name__ == "__main__":
    unittest.main()
