import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory import ecosystem_client


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class EcosystemClientTests(unittest.TestCase):
    def test_collection_isolates_a_failed_source(self):
        def opener(request, timeout):
            if request.full_url == ecosystem_client.GITHUB_AGAVE_RELEASES_URL:
                raise OSError("GitHub unavailable")
            return FakeResponse([])

        results = ecosystem_client.fetch_ecosystem_sources(opener=opener, timeout=7)

        self.assertEqual(set(results), {"protocols", "agave_releases"})
        self.assertEqual(results["protocols"]["status"], "ok")
        self.assertEqual(results["agave_releases"]["status"], "error")
        self.assertIn("GitHub unavailable", results["agave_releases"]["error"])


if __name__ == "__main__":
    unittest.main()
