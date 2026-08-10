import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.validator_depth import calculate_validator_depth


class ValidatorDepthTests(unittest.TestCase):
    def test_calculates_stake_concentration_delinquency_and_vote_coverage(self):
        vote_accounts = {
            "current": [
                {"votePubkey": "a", "activatedStake": 40_000_000_000, "commission": 5, "epochCredits": [[812, 100, 90]]},
                {"votePubkey": "b", "activatedStake": 30_000_000_000, "commission": 10, "epochCredits": []},
                {"votePubkey": "c", "activatedStake": 20_000_000_000, "commission": 15, "epochCredits": [[812, 80, 70]]},
                {"votePubkey": "bad", "activatedStake": "invalid", "commission": 100, "epochCredits": []},
            ],
            "delinquent": [
                {"votePubkey": "d", "activatedStake": 10_000_000_000, "commission": 20, "epochCredits": []},
                {"votePubkey": "a", "activatedStake": 999_000_000_000, "commission": 100, "epochCredits": []},
            ],
        }

        result = calculate_validator_depth(vote_accounts)

        self.assertEqual(result["active_stake_sol"], 90.0)
        self.assertEqual(result["delinquent_stake_sol"], 10.0)
        self.assertEqual(result["delinquent_stake_share_pct"], 10.0)
        self.assertEqual(result["top_10_stake_share_pct"], 100.0)
        self.assertEqual(result["top_25_stake_share_pct"], 100.0)
        self.assertEqual(result["superminority_coefficient"], 1)
        self.assertEqual(result["median_commission_pct"], 10.0)
        self.assertEqual(result["vote_credit_coverage_pct"], 66.67)
        self.assertEqual(result["ignored_invalid_accounts"], 1)
        self.assertEqual(result["ignored_duplicate_accounts"], 1)

    def test_zero_stake_returns_unavailable_ratios(self):
        result = calculate_validator_depth(
            {
                "current": [{"votePubkey": "a", "activatedStake": 0, "commission": 5, "epochCredits": []}],
                "delinquent": [],
            }
        )

        self.assertIsNone(result["delinquent_stake_share_pct"])
        self.assertIsNone(result["top_10_stake_share_pct"])
        self.assertIsNone(result["superminority_coefficient"])
        self.assertIsNone(result["vote_credit_coverage_pct"])


if __name__ == "__main__":
    unittest.main()
