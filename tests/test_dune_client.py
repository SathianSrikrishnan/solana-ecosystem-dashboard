import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_client import fetch_query_csv


class _Response:
    def __enter__(self): return self
    def __exit__(self, *args): return None
    def read(self): return b"activity_date,value\n2026-08-09,1\n"


class DuneClientTests(unittest.TestCase):
    def test_fetches_csv_with_dune_api_header(self):
        captured = {}
        def opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return _Response()

        result = fetch_query_csv(123, "secret", opener=opener)

        self.assertIn("activity_date", result)
        self.assertEqual(captured["request"].get_header("X-dune-api-key"), "secret")
        self.assertIn("/query/123/results/csv", captured["request"].full_url)

    def test_requires_a_key_without_exposing_it(self):
        with self.assertRaisesRegex(ValueError, "DUNE_API_KEY"):
            fetch_query_csv(123, "")


if __name__ == "__main__":
    unittest.main()
