import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.dune_client import execute_query, fetch_query_csv


class _Response:
    def __enter__(self): return self
    def __exit__(self, *args): return None
    def read(self): return b"activity_date,value\n2026-08-09,1\n"


class _JsonResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self): return self
    def __exit__(self, *args): return None
    def read(self): return self.payload.encode("utf-8")


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

    def test_executes_on_small_engine_and_returns_reported_credit_cost(self):
        captured = []
        responses = iter(
            [
                _JsonResponse('{"execution_id":"execution-1","state":"QUERY_STATE_PENDING"}'),
                _JsonResponse('{"is_execution_finished":false,"state":"QUERY_STATE_EXECUTING"}'),
                _JsonResponse('{"is_execution_finished":true,"state":"QUERY_STATE_COMPLETED","execution_cost_credits":3.25}'),
            ]
        )

        def opener(request, timeout):
            captured.append((request, timeout))
            return next(responses)

        cost = execute_query(
            123,
            "secret",
            opener=opener,
            sleeper=lambda _: None,
            poll_interval=0,
        )

        self.assertEqual(cost, 3.25)
        self.assertEqual(captured[0][0].method, "POST")
        self.assertEqual(captured[0][0].data, b'{"performance":"small"}')
        self.assertIn("/query/123/execute", captured[0][0].full_url)
        self.assertIn("/execution/execution-1/status", captured[-1][0].full_url)
        self.assertTrue(
            all(request.get_header("X-dune-api-key") == "secret" for request, _ in captured)
        )

    def test_failed_execution_raises_without_exposing_the_key(self):
        responses = iter(
            [
                _JsonResponse('{"execution_id":"execution-1","state":"QUERY_STATE_PENDING"}'),
                _JsonResponse('{"is_execution_finished":true,"state":"QUERY_STATE_FAILED","error":{"message":"bad query"}}'),
            ]
        )

        with self.assertRaisesRegex(RuntimeError, "QUERY_STATE_FAILED") as raised:
            execute_query(
                123,
                "secret-value",
                opener=lambda request, timeout: next(responses),
                sleeper=lambda _: None,
                poll_interval=0,
            )

        self.assertNotIn("secret-value", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
