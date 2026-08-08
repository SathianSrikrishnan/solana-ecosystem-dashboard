import math
import unittest
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory import economy


class EconomyParserTests(unittest.TestCase):
    collected_at = "2026-08-08T16:00:00Z"
    coingecko_url = (
        "https://api.coingecko.com/api/v3/simple/price?"
        "ids=solana&vs_currencies=usd&include_24hr_change=true&"
        "include_last_updated_at=true"
    )

    def _price_payload(self):
        return {
            "solana": {
                "usd": 76.31,
                "usd_24h_change": 3.2622383487,
                "last_updated_at": 1786200000,
            }
        }

    def test_coin_price_parser_builds_a_live_provenance_rich_metric(self):
        metric = economy.parse_coingecko_sol_price(
            self._price_payload(),
            collected_at=self.collected_at,
            source_url=self.coingecko_url,
        )

        expected_source_time = datetime.fromtimestamp(
            1786200000, tz=timezone.utc
        ).isoformat().replace("+00:00", "Z")
        self.assertEqual(metric["id"], "sol_price_usd")
        self.assertEqual(metric["section"], "economy")
        self.assertEqual(metric["label"], "SOL price")
        self.assertEqual(metric["value"], 76.31)
        self.assertEqual(metric["unit"], "USD")
        self.assertEqual(metric["status"], "ok")
        self.assertEqual(metric["source"]["name"], "CoinGecko")
        self.assertEqual(metric["source"]["url"], self.coingecko_url)
        self.assertEqual(metric["collected_at"], self.collected_at)
        self.assertEqual(metric["source_time"], expected_source_time)
        self.assertEqual(metric["confidence"], "high")
        self.assertEqual(metric["series"], [])
        self.assertIn("not", metric["caveat"].lower())
        self.assertIn("network", metric["caveat"].lower())

    def test_coin_price_parser_rejects_invalid_payloads(self):
        invalid_payloads = (
            {},
            {"solana": {}},
            {"solana": {"usd": -1, "last_updated_at": 1786200000}},
            {"solana": {"usd": "bad", "last_updated_at": 1786200000}},
            {"solana": {"usd": math.nan, "last_updated_at": 1786200000}},
            {"solana": {"usd": 76.31}},
            {"solana": {"usd": 76.31, "last_updated_at": 1786210000}},
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    economy.parse_coingecko_sol_price(
                        payload,
                        collected_at=self.collected_at,
                        source_url=self.coingecko_url,
                    )

    def test_coin_price_parser_rejects_invalid_context(self):
        contexts = (
            ("2026-08-08T16:00:00", self.coingecko_url),
            (self.collected_at, "https://example.com/price"),
        )
        for collected_at, source_url in contexts:
            with self.subTest(collected_at=collected_at, source_url=source_url):
                with self.assertRaises(ValueError):
                    economy.parse_coingecko_sol_price(
                        self._price_payload(),
                        collected_at=collected_at,
                        source_url=source_url,
                    )


if __name__ == "__main__":
    unittest.main()
