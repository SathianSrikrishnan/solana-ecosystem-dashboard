import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.briefing import build_grounded_briefing


class BriefingTests(unittest.TestCase):
    def test_builds_an_evidence_bound_plain_english_briefing(self):
        snapshot = {
            "generated_at": "2026-08-10T12:00:00Z",
            "metrics": {"daily_volume": {"label": "Daily volume"}},
            "comparisons": {"daily_volume": {"status": "ok"}},
            "anomalies": {
                "daily_volume": {
                    "metric_id": "daily_volume",
                    "status": "notable",
                    "direction": "decreased",
                    "observed_change_pct": -18.0,
                    "threshold_pct": 15.0,
                    "known_gap": None,
                }
            },
            "timeline": [{"period": "2026"}],
        }

        briefing = build_grounded_briefing(snapshot)

        self.assertEqual(briefing["status"], "ok")
        self.assertEqual(briefing["supporting_metric_ids"], ["daily_volume"])
        self.assertIn("Daily volume", briefing["current_reading"])
        self.assertIn("18.0%", briefing["current_reading"])
        self.assertIn("not automatically", briefing["uncertainty"])
        self.assertEqual(briefing["generated_at"], snapshot["generated_at"])
        self.assertEqual(briefing["model"], "deterministic-observatory-v1")

    def test_reports_quiet_comparison_state_without_inventing_an_event(self):
        snapshot = {
            "generated_at": "2026-08-10T12:00:00Z",
            "metrics": {},
            "comparisons": {},
            "anomalies": {},
            "timeline": [],
        }

        briefing = build_grounded_briefing(snapshot)

        self.assertEqual(briefing["supporting_metric_ids"], [])
        self.assertIn("No verified comparison", briefing["current_reading"])


if __name__ == "__main__":
    unittest.main()
