import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUERY_PATH = ROOT / "queries" / "daily_unique_fee_payers.sql"


class DuneQueryTests(unittest.TestCase):
    def test_daily_fee_payer_query_is_bounded_to_successful_complete_days(self):
        self.assertTrue(QUERY_PATH.exists(), "Daily fee-payer query is missing")

        query = QUERY_PATH.read_text(encoding="utf-8").lower()

        self.assertIn("from solana.transactions", query)
        self.assertIn("count(distinct signer)", query)
        self.assertIn("success = true", query)
        self.assertIn("current_date - interval '7' day", query)
        self.assertIn("block_date < current_date", query)


if __name__ == "__main__":
    unittest.main()
