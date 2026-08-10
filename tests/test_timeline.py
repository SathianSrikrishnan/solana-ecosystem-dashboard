import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.timeline import load_timeline


class TimelineTests(unittest.TestCase):
    def test_timeline_has_seven_ordered_sourced_eras(self):
        eras = load_timeline(ROOT / "data" / "history" / "solana_timeline.json")

        self.assertEqual(len(eras), 7)
        self.assertEqual([era["order"] for era in eras], list(range(1, 8)))
        self.assertEqual(eras[0]["period"], "2017–2020")
        self.assertEqual(eras[-1]["period"], "2026")
        for era in eras:
            self.assertTrue(era["title"])
            self.assertTrue(era["fact"])
            self.assertTrue(era["interpretation"])
            self.assertTrue(era["source_url"].startswith("https://"))
            self.assertIn(era["source_type"], {"primary", "authoritative"})

    def test_timeline_rejects_unsorted_or_incomplete_records(self):
        with self.assertRaisesRegex(ValueError, "ordered"):
            load_timeline(
                ROOT / "tests" / "fixtures" / "invalid_timeline.json"
            )


if __name__ == "__main__":
    unittest.main()
