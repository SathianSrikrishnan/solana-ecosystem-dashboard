import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.official_updates import parse_official_updates


class OfficialUpdatesTests(unittest.TestCase):
    def test_builds_news_and_upgrade_metrics_from_official_sources(self):
        rss = """<?xml version="1.0"?><rss><channel><item><title>Solana ships</title><link>https://solana.com/news/ships</link><pubDate>Sun, 09 Aug 2026 12:00:00 GMT</pubDate></item></channel></rss>"""
        alpenglow = "<h1>Alpenglow</h1><p>Under Development</p><p>Expected Mainnet Activation Date</p><p>Q3 2026</p>"
        simd = """simd | 0525\ntitle | Reduce Slot Times\nstatus | Draft\ncreated | 2026-05-01"""

        metrics = parse_official_updates(rss, alpenglow, simd, collected_at="2026-08-10T12:00:00Z")

        self.assertEqual(metrics["latest_official_solana_news_age_days"]["value"], 1.0)
        self.assertIn("Solana ships", metrics["latest_official_solana_news_age_days"]["source"]["method"])
        self.assertEqual(metrics["alpenglow_upgrade_status"]["value"], "Under development · Q3 2026")
        self.assertEqual(metrics["simd_0525_status"]["value"], "Draft")


if __name__ == "__main__":
    unittest.main()
