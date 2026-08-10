import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from refresh_ecosystem import refresh_ecosystem
from solana_observatory.ecosystem_client import (
    DEFILLAMA_PROTOCOLS_URL,
    GITHUB_AGAVE_RELEASES_URL,
)


class RefreshEcosystemTests(unittest.TestCase):
    collected_at = "2026-08-10T12:00:00Z"

    def _snapshot(self):
        return {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-10T11:00:00Z",
            "summary": {"status": "healthy", "headline": "RPC is healthy."},
            "metrics": {},
        }

    def _results(self):
        return {
            "protocols": {
                "status": "ok",
                "url": DEFILLAMA_PROTOCOLS_URL,
                "payload": [
                    {"name": "A", "chains": ["Solana"], "tvl": 10, "category": "Dexs"},
                    {"name": "B", "chains": ["Solana"], "tvl": 5, "category": "Lending"},
                ],
            },
            "agave_releases": {
                "status": "ok",
                "url": GITHUB_AGAVE_RELEASES_URL,
                "payload": [
                    {
                        "tag_name": "v4.2.0",
                        "published_at": "2026-08-07T12:00:00Z",
                        "html_url": "https://github.com/anza-xyz/agave/releases/tag/v4.2.0",
                        "draft": False,
                        "prerelease": False,
                    }
                ],
            },
        }

    def test_refresh_adds_four_live_metrics_and_two_explicit_gaps(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot = root / "snapshot.json"
            output = root / "output"
            snapshot.write_text(json.dumps(self._snapshot()), encoding="utf-8")

            refresh_ecosystem(
                snapshot,
                output,
                collected_at=self.collected_at,
                source_results=self._results(),
            )

            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            ecosystem = {
                key: metric
                for key, metric in report["metrics"].items()
                if metric["section"] == "ecosystem"
            }
            self.assertEqual(len(ecosystem), 6)
            self.assertTrue(
                all(ecosystem[key]["status"] == "ok" for key in (
                    "solana_tracked_tvl_protocols",
                    "solana_tracked_tvl_categories",
                    "agave_latest_stable_release_age_days",
                    "agave_stable_releases_90d",
                ))
            )
            self.assertEqual(ecosystem["solana_monthly_active_developers"]["status"], "unavailable")
            self.assertEqual(ecosystem["solana_retained_developers"]["status"], "unavailable")

    def test_failed_protocol_source_does_not_hide_release_metrics(self):
        results = self._results()
        results["protocols"] = {
            "status": "error",
            "url": DEFILLAMA_PROTOCOLS_URL,
            "error": "HTTP 503",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            snapshot = root / "snapshot.json"
            output = root / "output"
            snapshot.write_text(json.dumps(self._snapshot()), encoding="utf-8")
            refresh_ecosystem(
                snapshot,
                output,
                collected_at=self.collected_at,
                source_results=results,
            )
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["metrics"]["solana_tracked_tvl_protocols"]["status"], "unavailable")
            self.assertEqual(report["metrics"]["agave_stable_releases_90d"]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
