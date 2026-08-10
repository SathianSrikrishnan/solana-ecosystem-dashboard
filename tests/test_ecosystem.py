import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.ecosystem import parse_agave_releases, parse_defillama_protocol_breadth


class EcosystemParserTests(unittest.TestCase):
    collected_at = "2026-08-10T12:00:00Z"

    def test_protocol_parser_measures_positive_tvl_coverage_and_categories(self):
        payload = [
            {"name": "A", "chains": ["Solana"], "tvl": 10, "category": "Dexs"},
            {"name": "B", "chains": ["Solana", "Ethereum"], "tvl": 5, "category": "Lending"},
            {"name": "C", "chains": ["Solana"], "tvl": 0, "category": "Dexs"},
            {"name": "D", "chains": ["Ethereum"], "tvl": 20, "category": "Dexs"},
        ]

        metrics = parse_defillama_protocol_breadth(
            payload,
            collected_at=self.collected_at,
            source_url="https://api.llama.fi/protocols",
        )

        self.assertEqual(metrics["solana_tracked_tvl_protocols"]["value"], 2)
        self.assertEqual(metrics["solana_tracked_tvl_categories"]["value"], 2)
        self.assertEqual(metrics["solana_tracked_tvl_protocols"]["section"], "ecosystem")
        self.assertIn("not all Solana apps", metrics["solana_tracked_tvl_protocols"]["caveat"])

    def test_agave_parser_measures_latest_stable_release_and_90_day_cadence(self):
        payload = [
            {
                "tag_name": "v4.2.0",
                "published_at": "2026-08-07T12:00:00Z",
                "html_url": "https://github.com/anza-xyz/agave/releases/tag/v4.2.0",
                "draft": False,
                "prerelease": False,
            },
            {
                "tag_name": "v4.1.0",
                "published_at": "2026-07-01T12:00:00Z",
                "html_url": "https://github.com/anza-xyz/agave/releases/tag/v4.1.0",
                "draft": False,
                "prerelease": False,
            },
            {
                "tag_name": "v4.3.0-beta",
                "published_at": "2026-08-09T12:00:00Z",
                "html_url": "https://github.com/anza-xyz/agave/releases/tag/v4.3.0-beta",
                "draft": False,
                "prerelease": True,
            },
        ]

        metrics = parse_agave_releases(
            payload,
            collected_at=self.collected_at,
            source_url="https://api.github.com/repos/anza-xyz/agave/releases?per_page=100",
        )

        self.assertEqual(metrics["agave_latest_stable_release_age_days"]["value"], 3.0)
        self.assertEqual(metrics["agave_stable_releases_90d"]["value"], 2)
        self.assertEqual(metrics["agave_latest_stable_release_age_days"]["source_time"], "2026-08-07T12:00:00Z")
        self.assertIn("not adoption", metrics["agave_stable_releases_90d"]["caveat"])

    def test_ecosystem_parsers_reject_wrong_hosts_and_invalid_shapes(self):
        with self.assertRaises(ValueError):
            parse_defillama_protocol_breadth(
                [], collected_at=self.collected_at, source_url="https://example.com/protocols"
            )
        with self.assertRaises(ValueError):
            parse_agave_releases(
                {},
                collected_at=self.collected_at,
                source_url="https://api.github.com/repos/anza-xyz/agave/releases",
            )


if __name__ == "__main__":
    unittest.main()
