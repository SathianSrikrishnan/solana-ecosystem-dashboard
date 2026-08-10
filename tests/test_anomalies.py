import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.anomalies import build_anomalies, build_threshold_anomalies


class AnomalyTests(unittest.TestCase):
    def _comparison(self, change, direction="increased"):
        return {
            "metric_id": "daily_volume",
            "status": "ok",
            "grain": "daily",
            "current_average": 120.0,
            "previous_average": 100.0,
            "absolute_change": 20.0,
            "percent_change": change,
            "direction": direction,
            "previous_window": ["2026-07-27", "2026-08-02"],
            "current_window": ["2026-08-03", "2026-08-09"],
            "reason": None,
        }

    def test_flags_notable_movement_without_calling_it_good_or_bad(self):
        anomalies = build_anomalies(
            {"daily_volume": self._comparison(18.0)}, threshold_pct=15.0
        )

        record = anomalies["daily_volume"]
        self.assertEqual(record["status"], "notable")
        self.assertEqual(record["direction"], "increased")
        self.assertEqual(record["observed_change_pct"], 18.0)
        self.assertEqual(record["threshold_pct"], 15.0)
        self.assertIn("not a health verdict", record["caveat"])

    def test_keeps_below_threshold_and_unavailable_comparisons_visible(self):
        unavailable = self._comparison(None, "unknown")
        unavailable.update(status="unavailable", reason="Missing days")

        anomalies = build_anomalies(
            {
                "daily_volume": self._comparison(-4.0, "decreased"),
                "missing_metric": unavailable | {"metric_id": "missing_metric"},
            },
            threshold_pct=15.0,
        )

        self.assertEqual(anomalies["daily_volume"]["status"], "within_range")
        self.assertEqual(anomalies["missing_metric"]["status"], "unavailable")
        self.assertEqual(anomalies["missing_metric"]["known_gap"], "Missing days")

    def test_monitors_sponsor_named_operational_thresholds(self):
        metrics = {
            "estimated_non_vote_tps_vs_recent_median_pct": {"status": "ok", "value": -31.0},
            "estimated_slot_time_vs_recent_median_pct": {"status": "ok", "value": 8.0},
            "delinquent_stake_share_pct": {"status": "ok", "value": 6.2},
            "sol_price_24h_change_pct": {"status": "ok", "value": 11.0},
        }

        alerts = build_threshold_anomalies(metrics)

        self.assertEqual(alerts["estimated_non_vote_tps_vs_recent_median_pct"]["status"], "notable")
        self.assertEqual(alerts["estimated_slot_time_vs_recent_median_pct"]["status"], "within_range")
        self.assertEqual(alerts["delinquent_stake_share_pct"]["status"], "notable")
        self.assertEqual(alerts["sol_price_24h_change_pct"]["status"], "notable")
        self.assertIn("review threshold", alerts["sol_price_24h_change_pct"]["message"])


if __name__ == "__main__":
    unittest.main()
