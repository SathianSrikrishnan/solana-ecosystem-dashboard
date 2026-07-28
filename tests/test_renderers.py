import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.renderers import render_html, render_json, render_markdown


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {
            "schema_version": "0.1.0",
            "generated_at": "2026-07-27T22:00:00Z",
            "summary": {"status": "healthy", "headline": "Solana RPC is healthy."},
            "metrics": {
                "rpc_health": {
                    "label": "RPC health",
                    "value": "ok",
                    "unit": "status",
                    "status": "ok",
                    "definition": "Health response from the selected RPC node.",
                    "source": {
                        "name": "Solana JSON-RPC",
                        "method": "getHealth",
                        "url": "https://api.mainnet-beta.solana.com",
                    },
                    "collected_at": "2026-07-27T22:00:00Z",
                    "confidence": "high",
                    "caveat": "This checks one RPC endpoint, not every validator.",
                }
            },
        }

    def test_json_is_machine_readable(self):
        rendered = render_json(self.snapshot)
        self.assertEqual(json.loads(rendered), self.snapshot)

    def test_markdown_includes_freshness_source_and_caveat(self):
        rendered = render_markdown(self.snapshot)
        self.assertIn("2026-07-27T22:00:00Z", rendered)
        self.assertIn("Solana JSON-RPC", rendered)
        self.assertIn("This checks one RPC endpoint", rendered)

    def test_html_embeds_snapshot_and_plain_english_sections(self):
        rendered = render_html(self.snapshot)
        self.assertIn("<!doctype html>", rendered.lower())
        self.assertIn("What is happening now?", rendered)
        self.assertIn("How to read this", rendered)
        self.assertIn('"rpc_health"', rendered)


if __name__ == "__main__":
    unittest.main()

