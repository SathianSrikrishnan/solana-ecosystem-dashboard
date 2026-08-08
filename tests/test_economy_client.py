import json
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory import economy_client


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class EconomyClientTests(unittest.TestCase):
    def test_fetch_json_sets_user_agent_timeout_and_decodes_payload(self):
        calls = []

        def opener(request, timeout):
            calls.append((request, timeout))
            return FakeResponse({"solana": {"usd": 76.31}})

        payload = economy_client.fetch_json(
            economy_client.COINGECKO_PRICE_URL,
            opener=opener,
            timeout=17,
        )

        self.assertEqual(payload["solana"]["usd"], 76.31)
        self.assertEqual(len(calls), 1)
        request, timeout = calls[0]
        self.assertEqual(timeout, 17)
        self.assertIn("Solana-Observatory", request.get_header("User-agent"))

    def test_fetch_json_rejects_malformed_or_scalar_payloads(self):
        class RawResponse(FakeResponse):
            def __init__(self, body):
                self.body = body

        invalid_bodies = (b"not-json", b"123", b'"text"')
        for body in invalid_bodies:
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    economy_client.fetch_json(
                        economy_client.COINGECKO_PRICE_URL,
                        opener=lambda request, timeout: RawResponse(body),
                    )

    def test_source_collection_isolates_one_failed_request(self):
        payloads = {
            economy_client.COINGECKO_PRICE_URL: {"solana": {"usd": 76.31}},
            economy_client.DEFILLAMA_TVL_URL: [{"date": 1, "tvl": 2}],
            economy_client.DEFILLAMA_DEX_URL: {"totalDataChart": [[1, 2]]},
        }

        def opener(request, timeout):
            if request.full_url == economy_client.DEFILLAMA_STABLECOIN_URL:
                raise OSError("stablecoin source unavailable")
            return FakeResponse(payloads[request.full_url])

        results = economy_client.fetch_economy_sources(opener=opener, timeout=9)

        self.assertEqual(set(results), {"price", "tvl", "stablecoins", "dex"})
        self.assertEqual(results["price"]["status"], "ok")
        self.assertEqual(results["tvl"]["status"], "ok")
        self.assertEqual(results["dex"]["status"], "ok")
        self.assertEqual(results["stablecoins"]["status"], "error")
        self.assertIn("unavailable", results["stablecoins"]["error"])
        self.assertEqual(
            results["stablecoins"]["url"],
            economy_client.DEFILLAMA_STABLECOIN_URL,
        )
        self.assertNotIn("payload", results["stablecoins"])


if __name__ == "__main__":
    unittest.main()
