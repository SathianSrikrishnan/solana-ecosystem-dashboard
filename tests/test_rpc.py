import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.rpc import (
    SolanaRpcClient,
    SolanaRpcError,
    collect_network_results,
)


class RpcClientTests(unittest.TestCase):
    def test_sends_json_rpc_request_and_returns_result(self):
        requests = []

        def fake_transport(url, payload, timeout):
            requests.append((url, payload, timeout))
            return {"jsonrpc": "2.0", "id": 1, "result": 123}

        client = SolanaRpcClient(transport=fake_transport)
        result = client.call("getSlot", [{"commitment": "confirmed"}])

        self.assertEqual(result, 123)
        self.assertEqual(requests[0][1]["method"], "getSlot")
        self.assertEqual(
            requests[0][1]["params"], [{"commitment": "confirmed"}]
        )
        self.assertGreater(requests[0][2], 0)

    def test_raises_visible_error_for_rpc_error_response(self):
        def fake_transport(url, payload, timeout):
            return {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {"code": -32601, "message": "Method not found"},
            }

        client = SolanaRpcClient(transport=fake_transport)

        with self.assertRaisesRegex(SolanaRpcError, "Method not found"):
            client.call("notARealMethod")

    def test_collects_the_required_network_methods(self):
        called_methods = []

        class FakeClient:
            def call(self, method, params=None):
                called_methods.append(method)
                return method

        results = collect_network_results(FakeClient())

        self.assertEqual(
            called_methods,
            [
                "getHealth",
                "getSlot",
                "getBlockHeight",
                "getEpochInfo",
                "getRecentPerformanceSamples",
                "getRecentPrioritizationFees",
                "getVoteAccounts",
            ],
        )
        self.assertEqual(results["getSlot"], "getSlot")


if __name__ == "__main__":
    unittest.main()
