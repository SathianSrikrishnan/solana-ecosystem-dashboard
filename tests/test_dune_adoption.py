import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "src" / "solana_observatory" / "dune_adoption.py"
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory import dune_adoption


class DuneAdoptionTests(unittest.TestCase):
    collected_at = "2026-08-03T12:00:00Z"
    source_url = "https://dune.com/queries/1234567"

    def _valid_csv(self):
        return """activity_date,unique_fee_payers
2026-08-02,160
2026-07-31,140
2026-07-27,100
2026-08-01,150
2026-07-29,120
2026-07-28,110
2026-07-30,130
"""

    def _valid_signers_csv(self):
        return """activity_date,unique_successful_signers
2026-08-02,190
2026-07-31,170
2026-07-27,130
2026-08-01,180
2026-07-29,150
2026-07-28,140
2026-07-30,160
"""

    def test_daily_fee_payer_adapter_module_exists(self):
        self.assertTrue(MODULE_PATH.exists(), "Dune adoption adapter is missing")

    def test_daily_fee_payer_parser_exists(self):
        self.assertTrue(
            hasattr(dune_adoption, "parse_daily_fee_payers_csv"),
            "Daily fee-payer parser is missing",
        )

    def test_parser_builds_a_sorted_provenance_rich_metric(self):
        metric = dune_adoption.parse_daily_fee_payers_csv(
            self._valid_csv(),
            collected_at=self.collected_at,
            source_url=self.source_url,
        )

        self.assertIn("id", metric)
        self.assertEqual(metric["id"], "daily_unique_successful_fee_payers")
        self.assertEqual(metric["section"], "adoption")
        self.assertEqual(metric["value"], 160)
        self.assertEqual(metric["unit"], "wallet addresses")
        self.assertEqual(metric["status"], "ok")
        self.assertEqual(metric["source"]["name"], "Dune")
        self.assertEqual(metric["source"]["url"], self.source_url)
        self.assertEqual(metric["collected_at"], self.collected_at)
        self.assertEqual(metric["source_time"], "2026-08-02")
        self.assertEqual(metric["confidence"], "high")
        self.assertEqual(
            metric["series"][0],
            {"observed_at": "2026-07-27", "value": 100},
        )
        self.assertEqual(
            metric["series"][-1],
            {"observed_at": "2026-08-02", "value": 160},
        )
        self.assertIn("not people", metric["caveat"].lower())

    def test_parser_rejects_empty_or_incomplete_csv(self):
        for csv_text in (
            "",
            "activity_date,unique_fee_payers\n",
            "activity_date\n2026-08-02\n",
        ):
            with self.subTest(csv_text=csv_text):
                with self.assertRaises(ValueError):
                    dune_adoption.parse_daily_fee_payers_csv(
                        csv_text,
                        collected_at=self.collected_at,
                        source_url=self.source_url,
                    )

    def test_parser_rejects_duplicate_dates(self):
        csv_text = self._valid_csv().replace("2026-07-30,130", "2026-08-02,130")

        with self.assertRaisesRegex(ValueError, "duplicate"):
            dune_adoption.parse_daily_fee_payers_csv(
                csv_text,
                collected_at=self.collected_at,
                source_url=self.source_url,
            )

    def test_parser_rejects_invalid_dates_and_counts(self):
        replacements = (
            ("2026-07-30,130", "not-a-date,130"),
            ("2026-07-30,130", "2026-07-30,12.5"),
            ("2026-07-30,130", "2026-07-30,-1"),
        )
        for old, new in replacements:
            with self.subTest(replacement=new):
                with self.assertRaises(ValueError):
                    dune_adoption.parse_daily_fee_payers_csv(
                        self._valid_csv().replace(old, new),
                        collected_at=self.collected_at,
                        source_url=self.source_url,
                    )

    def test_parser_requires_the_latest_seven_complete_days(self):
        csv_text = self._valid_csv().replace("2026-07-27,100\n", "")

        with self.assertRaisesRegex(ValueError, "seven complete UTC days"):
            dune_adoption.parse_daily_fee_payers_csv(
                csv_text,
                collected_at=self.collected_at,
                source_url=self.source_url,
            )

    def test_successful_signer_parser_builds_a_sorted_metric(self):
        metric = dune_adoption.parse_daily_successful_signers_csv(
            self._valid_signers_csv(),
            collected_at=self.collected_at,
            source_url=self.source_url,
        )

        self.assertEqual(metric["id"], "daily_unique_successful_signers")
        self.assertEqual(metric["section"], "adoption")
        self.assertEqual(metric["unit"], "wallet addresses")
        self.assertEqual(metric["status"], "ok")
        self.assertEqual(metric["value"], 190)
        self.assertEqual(metric["source"]["name"], "Dune")
        self.assertEqual(metric["collected_at"], self.collected_at)
        self.assertEqual(metric["source_time"], "2026-08-02")
        self.assertEqual(
            metric["series"][0],
            {"observed_at": "2026-07-27", "value": 130},
        )
        self.assertIn("not people", metric["caveat"].lower())
        self.assertIn("several signers", metric["caveat"].lower())

    def test_successful_signer_parser_rejects_invalid_exports(self):
        invalid_exports = (
            "",
            "activity_date,unique_successful_signers\n",
            self._valid_signers_csv().replace(
                "2026-07-30,160", "2026-08-02,160"
            ),
            self._valid_signers_csv().replace("2026-07-30,160", "bad-date,160"),
            self._valid_signers_csv().replace("2026-07-30,160", "2026-07-30,-1"),
            self._valid_signers_csv().replace("2026-07-30,160", "2026-07-30,1.5"),
            self._valid_signers_csv().replace("2026-07-27,130\n", ""),
        )
        for csv_text in invalid_exports:
            with self.subTest(csv_text=csv_text):
                with self.assertRaises(ValueError):
                    dune_adoption.parse_daily_successful_signers_csv(
                        csv_text,
                        collected_at=self.collected_at,
                        source_url=self.source_url,
                    )


if __name__ == "__main__":
    unittest.main()
