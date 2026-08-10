import sys
import unittest
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.comparisons import build_comparison


class ComparisonTests(unittest.TestCase):
    def _metric(self, values):
        first_day = date(2026, 7, 27)
        return {
            "id": "daily_volume",
            "series": [
                {
                    "observed_at": (first_day + timedelta(days=index)).isoformat(),
                    "value": value,
                }
                for index, value in enumerate(values)
            ],
        }

    def test_compares_latest_seven_complete_days_with_preceding_seven(self):
        comparison = build_comparison(self._metric([100] * 7 + [125] * 7))

        self.assertEqual(comparison["status"], "ok")
        self.assertEqual(comparison["metric_id"], "daily_volume")
        self.assertEqual(comparison["current_average"], 125.0)
        self.assertEqual(comparison["previous_average"], 100.0)
        self.assertEqual(comparison["absolute_change"], 25.0)
        self.assertEqual(comparison["percent_change"], 25.0)
        self.assertEqual(comparison["direction"], "increased")
        self.assertEqual(comparison["previous_window"], ["2026-07-27", "2026-08-02"])
        self.assertEqual(comparison["current_window"], ["2026-08-03", "2026-08-09"])

    def test_reports_insufficient_history_without_inventing_change(self):
        comparison = build_comparison(self._metric([100] * 13))

        self.assertEqual(comparison["status"], "unavailable")
        self.assertIsNone(comparison["percent_change"])
        self.assertIn("14", comparison["reason"])

    def test_zero_baseline_keeps_absolute_change_but_not_percent_change(self):
        comparison = build_comparison(self._metric([0] * 7 + [10] * 7))

        self.assertEqual(comparison["status"], "ok")
        self.assertEqual(comparison["absolute_change"], 10.0)
        self.assertIsNone(comparison["percent_change"])
        self.assertEqual(comparison["direction"], "increased")

    def test_rejects_series_that_is_not_daily_and_contiguous(self):
        metric = self._metric([100] * 14)
        metric["series"][8]["observed_at"] = "2026-08-10T12:00:00Z"

        comparison = build_comparison(metric)

        self.assertEqual(comparison["status"], "unavailable")
        self.assertIn("daily", comparison["reason"])


if __name__ == "__main__":
    unittest.main()
