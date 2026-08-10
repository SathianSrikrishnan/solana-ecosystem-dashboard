import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from refresh_economy import refresh_economy
from solana_observatory.economy_client import (
    COINGECKO_PRICE_URL,
    DEFILLAMA_DEX_URL,
    DEFILLAMA_STABLECOIN_URL,
    DEFILLAMA_TVL_URL,
    DEFILLAMA_CHAIN_FEES_URL,
    DEFILLAMA_APP_FEES_URL,
    DEFILLAMA_APP_REVENUE_URL,
    DEFILLAMA_JITO_TIPS_URL,
)


class RefreshEconomyTests(unittest.TestCase):
    collected_at = "2026-08-08T16:00:00Z"

    def _snapshot(self):
        return {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-08T15:00:00Z",
            "summary": {"status": "healthy", "headline": "RPC is healthy."},
            "metrics": {},
        }

    def _source_results(self):
        first_day = date(2026, 7, 25)
        tvl, stablecoins, dex = [], [], []
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
                    "date": timestamp,
                    "totalCirculatingUSD": {"peggedUSD": 2000 + index},
                }
            )
            dex.append([timestamp, 3000 + index])
        return {
            "price": {
                "status": "ok",
                "url": COINGECKO_PRICE_URL,
                "payload": {
                    "solana": {
                        "usd": 76.31,
                        "usd_24h_change": 3.2,
                        "last_updated_at": 1786200000,
                    }
                },
            },
            "tvl": {"status": "ok", "url": DEFILLAMA_TVL_URL, "payload": tvl},
            "stablecoins": {
                "status": "ok",
                "url": DEFILLAMA_STABLECOIN_URL,
                "payload": stablecoins,
            },
            "dex": {
                "status": "ok",
                "url": DEFILLAMA_DEX_URL,
                "payload": {"totalDataChart": dex},
            },
            "chain_fees": {
                "status": "ok", "url": DEFILLAMA_CHAIN_FEES_URL,
                "payload": {"totalDataChart": dex},
            },
            "app_fees": {
                "status": "ok", "url": DEFILLAMA_APP_FEES_URL,
                "payload": {"totalDataChart": dex},
            },
            "app_revenue": {
                "status": "ok", "url": DEFILLAMA_APP_REVENUE_URL,
                "payload": {"totalDataChart": dex},
            },
            "jito_tips": {
                "status": "ok", "url": DEFILLAMA_JITO_TIPS_URL,
                "payload": {"totalDataChart": [[row[0], 100] for row in dex]},
            },
        }

    def test_successful_refresh_adds_eight_metrics_to_every_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot_path = root / "snapshot.json"
            output_dir = root / "output"
            snapshot_path.write_text(
                json.dumps(self._snapshot()), encoding="utf-8"
            )

            refresh_economy(
                snapshot_path,
                output_dir,
                collected_at=self.collected_at,
                source_results=self._source_results(),
            )

            report = json.loads(
                (output_dir / "report.json").read_text(encoding="utf-8")
            )
            economy_ids = {
                key
                for key, metric in report["metrics"].items()
                if metric["section"] == "economy"
            }
            self.assertEqual(
                economy_ids,
                {
                    "sol_price_usd",
                    "solana_defi_tvl_usd",
                    "solana_dex_volume_usd",
                    "solana_chain_fees_usd",
                    "solana_app_fees_usd",
                    "solana_app_revenue_usd",
                    "solana_rev_usd",
                },
            )
            self.assertEqual(
                report["metrics"]["solana_stablecoin_value_usd"]["section"],
                "financial_rails",
            )
            self.assertEqual(
                report["metrics"]["solana_non_stablecoin_rwa_value_usd"]["status"],
                "unavailable",
            )
            self.assertEqual(
                report["metrics"]["solana_identifiable_payments_usd"]["status"],
                "unavailable",
            )
            self.assertIn(
                "authentication",
                report["metrics"]["solana_non_stablecoin_rwa_value_usd"]["caveat"],
            )
            self.assertIn(
                "not payments",
                report["metrics"]["solana_identifiable_payments_usd"]["caveat"],
            )
            markdown = (output_dir / "report.md").read_text(encoding="utf-8")
            html = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn("Solana daily DEX volume", markdown)
            self.assertIn('data-metric="sol_price_usd"', html)
            self.assertIn('data-metric="solana_rev_usd"', html)

    def test_one_failed_source_marks_only_its_metric_unavailable(self):
        results = self._source_results()
        results["tvl"] = {
            "status": "error",
            "url": DEFILLAMA_TVL_URL,
            "error": "HTTP 503",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot_path = root / "snapshot.json"
            output_dir = root / "output"
            snapshot_path.write_text(
                json.dumps(self._snapshot()), encoding="utf-8"
            )

            refresh_economy(
                snapshot_path,
                output_dir,
                collected_at=self.collected_at,
                source_results=results,
            )

            report = json.loads(
                (output_dir / "report.json").read_text(encoding="utf-8")
            )
            tvl = report["metrics"]["solana_defi_tvl_usd"]
            self.assertEqual(tvl["status"], "unavailable")
            self.assertIsNone(tvl["value"])
            self.assertEqual(tvl["source"]["url"], DEFILLAMA_TVL_URL)
            self.assertIn("HTTP 503", tvl["caveat"])
            self.assertTrue(
                all(
                    report["metrics"][metric_id]["status"] == "ok"
                    for metric_id in (
                        "sol_price_usd",
                        "solana_stablecoin_value_usd",
                        "solana_dex_volume_usd",
                    )
                )
            )

    def test_failed_jito_component_only_makes_rev_unavailable(self):
        results = self._source_results()
        results["jito_tips"] = {
            "status": "error",
            "url": DEFILLAMA_JITO_TIPS_URL,
            "error": "HTTP 503",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot_path = root / "snapshot.json"
            output_dir = root / "output"
            snapshot_path.write_text(json.dumps(self._snapshot()), encoding="utf-8")

            refresh_economy(
                snapshot_path,
                output_dir,
                collected_at=self.collected_at,
                source_results=results,
            )

            report = json.loads(
                (output_dir / "report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(report["metrics"]["solana_rev_usd"]["status"], "unavailable")
            self.assertEqual(report["metrics"]["solana_chain_fees_usd"]["status"], "ok")
            self.assertEqual(report["metrics"]["solana_app_fees_usd"]["status"], "ok")
            self.assertEqual(report["metrics"]["solana_app_revenue_usd"]["status"], "ok")

    def test_app_revenue_above_app_fees_is_visibly_flagged(self):
        results = self._source_results()
        results["app_revenue"]["payload"] = {
            "totalDataChart": [
                [row[0], row[1] + 1]
                for row in results["app_fees"]["payload"]["totalDataChart"]
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot_path = root / "snapshot.json"
            output_dir = root / "output"
            snapshot_path.write_text(json.dumps(self._snapshot()), encoding="utf-8")

            refresh_economy(
                snapshot_path,
                output_dir,
                collected_at=self.collected_at,
                source_results=results,
            )

            report = json.loads(
                (output_dir / "report.json").read_text(encoding="utf-8")
            )
            revenue = report["metrics"]["solana_app_revenue_usd"]
            self.assertEqual(revenue["status"], "error")
            self.assertIn("sanity check", revenue["caveat"])

    def test_invalid_snapshot_preserves_existing_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot_path = root / "snapshot.json"
            output_dir = root / "output"
            output_dir.mkdir()
            snapshot_path.write_text(
                json.dumps({"metrics": {}}), encoding="utf-8"
            )
            for name in ("report.json", "report.md", "index.html"):
                (output_dir / name).write_text("original", encoding="utf-8")

            with self.assertRaises(ValueError):
                refresh_economy(
                    snapshot_path,
                    output_dir,
                    collected_at=self.collected_at,
                    source_results=self._source_results(),
                )

            for name in ("report.json", "report.md", "index.html"):
                self.assertEqual(
                    (output_dir / name).read_text(encoding="utf-8"),
                    "original",
                )


if __name__ == "__main__":
    unittest.main()
