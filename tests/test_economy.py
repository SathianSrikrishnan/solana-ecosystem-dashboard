import math
import unittest
from datetime import date, datetime, timedelta, timezone
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

    def _defillama_payloads(self):
        first_day = date(2026, 7, 25)
        tvl = []
        stablecoins = []
        dex = []
        for index in range(14):
            observed_day = first_day + timedelta(days=index)
            timestamp = int(
                datetime.combine(
                    observed_day, datetime.min.time(), tzinfo=timezone.utc
                ).timestamp()
            )
            tvl.append({"date": timestamp, "tvl": 1000 + index})
            stablecoins.append(
                {
                    "date": str(timestamp),
                    "totalCirculatingUSD": {
                        "peggedUSD": 2000 + index,
                        "peggedEUR": 10 + index,
                    },
                }
            )
            dex.append([timestamp, 3000 + index])
        return tvl, stablecoins, {"totalDataChart": dex}

    def _defillama_urls(self):
        return {
            "tvl": "https://api.llama.fi/v2/historicalChainTvl/Solana",
            "stablecoins": (
                "https://stablecoins.llama.fi/stablecoincharts/Solana"
            ),
            "dex": (
                "https://api.llama.fi/overview/dexs/Solana?"
                "excludeTotalDataChartBreakdown=true&dataType=dailyVolume"
            ),
        }

    def test_defillama_parser_builds_three_complete_day_metrics(self):
        tvl, stablecoins, dex = self._defillama_payloads()

        metrics = economy.parse_defillama_economy(
            tvl,
            stablecoins,
            dex,
            collected_at=self.collected_at,
            source_urls=self._defillama_urls(),
        )

        self.assertEqual(
            set(metrics),
            {
                "solana_defi_tvl_usd",
                "solana_stablecoin_value_usd",
                "solana_dex_volume_usd",
            },
        )
        tvl_metric = metrics["solana_defi_tvl_usd"]
        stable_metric = metrics["solana_stablecoin_value_usd"]
        dex_metric = metrics["solana_dex_volume_usd"]
        self.assertEqual(tvl_metric["value"], 1013.0)
        self.assertEqual(stable_metric["value"], 2036.0)
        self.assertEqual(dex_metric["value"], 3013.0)
        self.assertEqual(tvl_metric["source_time"], "2026-08-07")
        self.assertEqual(len(tvl_metric["series"]), 14)
        self.assertEqual(tvl_metric["series"][0]["observed_at"], "2026-07-25")
        self.assertEqual(stable_metric["unit"], "USD")
        self.assertEqual(dex_metric["section"], "economy")
        self.assertEqual(tvl_metric["source"]["name"], "DeFiLlama")
        self.assertIn("historicalChainTvl", tvl_metric["source"]["method"])
        self.assertIn("stablecoin", stable_metric["source"]["method"])
        self.assertIn("dailyVolume", dex_metric["source"]["method"])
        self.assertIn("coverage", tvl_metric["caveat"].lower())
        self.assertIn("payment", stable_metric["caveat"].lower())
        self.assertIn("routing", dex_metric["caveat"].lower())

    def test_defillama_datasets_can_be_normalized_independently(self):
        tvl, stablecoins, dex = self._defillama_payloads()
        urls = self._defillama_urls()

        tvl_metric = economy.parse_defillama_tvl(
            tvl, collected_at=self.collected_at, source_url=urls["tvl"]
        )
        stablecoin_metric = economy.parse_defillama_stablecoins(
            stablecoins,
            collected_at=self.collected_at,
            source_url=urls["stablecoins"],
        )
        dex_metric = economy.parse_defillama_dex(
            dex, collected_at=self.collected_at, source_url=urls["dex"]
        )

        self.assertEqual(tvl_metric["id"], "solana_defi_tvl_usd")
        self.assertEqual(
            stablecoin_metric["id"], "solana_stablecoin_value_usd"
        )
        self.assertEqual(dex_metric["id"], "solana_dex_volume_usd")

    def test_defillama_parser_ignores_the_providers_partial_current_day(self):
        tvl, stablecoins, dex = self._defillama_payloads()
        current_day = int(
            datetime(2026, 8, 8, tzinfo=timezone.utc).timestamp()
        )
        tvl.append({"date": current_day, "tvl": 9999})
        stablecoins.append(
            {
                "date": current_day,
                "totalCirculatingUSD": {"peggedUSD": 9999},
            }
        )
        dex["totalDataChart"].append([current_day, 9999])

        metrics = economy.parse_defillama_economy(
            tvl,
            stablecoins,
            dex,
            collected_at=self.collected_at,
            source_urls=self._defillama_urls(),
        )

        self.assertTrue(
            all(metric["source_time"] == "2026-08-07" for metric in metrics.values())
        )
        self.assertTrue(
            all(len(metric["series"]) == 14 for metric in metrics.values())
        )

    def test_defillama_parser_rejects_incomplete_or_duplicate_dates(self):
        tvl, stablecoins, dex = self._defillama_payloads()
        invalid_tvl_payloads = (
            tvl[:-1],
            tvl[:-1] + [dict(tvl[-2])],
            tvl[1:] + [{"date": 1786204800, "tvl": 9999}],
        )
        for invalid_tvl in invalid_tvl_payloads:
            with self.subTest(invalid_tvl=invalid_tvl):
                with self.assertRaises(ValueError):
                    economy.parse_defillama_economy(
                        invalid_tvl,
                        stablecoins,
                        dex,
                        collected_at=self.collected_at,
                        source_urls=self._defillama_urls(),
                    )

    def test_defillama_parser_rejects_invalid_values_and_sources(self):
        tvl, stablecoins, dex = self._defillama_payloads()
        invalid_cases = (
            (tvl[:-1] + [{"date": tvl[-1]["date"], "tvl": -1}], stablecoins, dex),
            (
                tvl,
                stablecoins[:-1]
                + [
                    {
                        "date": stablecoins[-1]["date"],
                        "totalCirculatingUSD": {"peggedUSD": math.inf},
                    }
                ],
                dex,
            ),
            (
                tvl,
                stablecoins,
                {
                    "totalDataChart": dex["totalDataChart"][:-1]
                    + [[dex["totalDataChart"][-1][0], "bad"]]
                },
            ),
        )
        for invalid_tvl, invalid_stables, invalid_dex in invalid_cases:
            with self.subTest(invalid_dex=invalid_dex):
                with self.assertRaises(ValueError):
                    economy.parse_defillama_economy(
                        invalid_tvl,
                        invalid_stables,
                        invalid_dex,
                        collected_at=self.collected_at,
                        source_urls=self._defillama_urls(),
                    )

        bad_urls = self._defillama_urls()
        bad_urls["tvl"] = "https://example.com/tvl"
        with self.assertRaises(ValueError):
            economy.parse_defillama_economy(
                tvl,
                stablecoins,
                dex,
                collected_at=self.collected_at,
                source_urls=bad_urls,
            )


if __name__ == "__main__":
    unittest.main()
