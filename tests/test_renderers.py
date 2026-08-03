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
            "schema_version": "0.2.0",
            "generated_at": "2026-07-27T22:00:00Z",
            "summary": {"status": "healthy", "headline": "Solana RPC is healthy."},
            "metrics": {
                "rpc_health": {
                    "id": "rpc_health",
                    "section": "network",
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
                    "source_time": None,
                    "confidence": "high",
                    "caveat": "This checks one RPC endpoint, not every validator.",
                    "series": [],
                },
                "estimated_non_vote_tps": {
                    "id": "estimated_non_vote_tps",
                    "section": "network",
                    "label": "Estimated non-vote TPS",
                    "value": 2081.32,
                    "unit": "transactions/second",
                    "status": "ok",
                    "definition": "Non-vote transactions divided by sample seconds.",
                    "source": {
                        "name": "Solana JSON-RPC",
                        "method": "getRecentPerformanceSamples",
                        "url": "https://api.mainnet-beta.solana.com",
                    },
                    "collected_at": "2026-07-27T22:00:00Z",
                    "source_time": None,
                    "confidence": "high",
                    "caveat": "Non-vote transactions can include bots.",
                    "series": [],
                },
                "active_validators": {
                    "id": "active_validators",
                    "section": "validators",
                    "label": "Active validators",
                    "value": 692,
                    "unit": "validators",
                    "status": "ok",
                    "definition": "Vote accounts classified as active.",
                    "source": {
                        "name": "Solana JSON-RPC",
                        "method": "getVoteAccounts",
                        "url": "https://api.mainnet-beta.solana.com",
                    },
                    "collected_at": "2026-07-27T22:00:00Z",
                    "source_time": None,
                    "confidence": "high",
                    "caveat": "Count does not describe stake distribution.",
                    "series": [],
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

    def test_html_provides_navigation_and_all_dashboard_sections(self):
        rendered = render_html(self.snapshot)

        for section in (
            "overview",
            "network",
            "adoption",
            "economy",
            "validators",
            "ecosystem",
            "methods",
        ):
            self.assertIn(f'href="#{section}"', rendered)
            self.assertIn(f'id="{section}"', rendered)

        self.assertIn('aria-label="Dashboard sections"', rendered)

    def test_html_opens_with_three_product_questions(self):
        rendered = render_html(self.snapshot)

        self.assertIn("Is the network functioning properly?", rendered)
        self.assertIn(
            "Is application and wallet activity growing or returning?",
            rendered,
        )
        self.assertIn("Is meaningful economic activity increasing?", rendered)

    def test_html_opens_with_three_balanced_signal_states(self):
        rendered = render_html(self.snapshot)

        self.assertEqual(rendered.count('class="signal-card"'), 3)
        self.assertIn("RPC health", rendered)
        self.assertEqual(rendered.count("Awaiting verified data"), 2)
        self.assertIn("3 of 3 metrics reporting", rendered)

    def test_html_groups_metrics_and_marks_unpopulated_sections_as_upcoming(self):
        rendered = render_html(self.snapshot)

        network_start = rendered.index('id="network"')
        validators_start = rendered.index('id="validators"')
        self.assertLess(
            network_start,
            rendered.index('data-metric="estimated_non_vote_tps"'),
        )
        self.assertLess(
            validators_start,
            rendered.index('data-metric="active_validators"'),
        )
        self.assertEqual(rendered.count("Data adapter planned"), 3)

    def test_html_keeps_evidence_and_interpretation_visually_separate(self):
        rendered = render_html(self.snapshot)

        self.assertIn("Verified facts", rendered)
        self.assertIn("Interpretation", rendered)
        self.assertIn("Automatic AI briefing", rendered)
        self.assertIn("Analysis unavailable for this snapshot", rendered)
        self.assertIn("<strong>Collected:</strong> 2026-07-27T22:00:00Z", rendered)
        self.assertIn("<strong>Confidence:</strong> high", rendered)

    def test_html_renders_grounded_automatic_analysis_when_present(self):
        self.snapshot["analysis"] = {
            "status": "ok",
            "current_reading": "The RPC endpoint is responding normally.",
            "supporting_metric_ids": ["rpc_health", "active_validators"],
            "uncertainty": "This snapshot does not yet measure adoption or economics.",
            "generated_at": "2026-07-27T22:01:00Z",
            "model": "example-grounded-model",
        }

        rendered = render_html(self.snapshot)

        self.assertIn("The RPC endpoint is responding normally.", rendered)
        self.assertIn("rpc_health, active_validators", rendered)
        self.assertIn(
            "This snapshot does not yet measure adoption or economics.",
            rendered,
        )
        self.assertIn("2026-07-27T22:01:00Z", rendered)
        self.assertIn("example-grounded-model", rendered)

    def test_html_shows_unavailable_metrics_without_inventing_a_zero(self):
        self.snapshot["metrics"]["rpc_health"]["value"] = None
        self.snapshot["metrics"]["rpc_health"]["status"] = "unavailable"

        rendered = render_html(self.snapshot)

        self.assertIn('data-status="unavailable"', rendered)
        self.assertIn("Not available", rendered)
        self.assertIn("2 of 3 metrics reporting", rendered)
        self.assertNotIn(">None<", rendered)

    def test_html_includes_mobile_layout_and_accessible_skip_link(self):
        rendered = render_html(self.snapshot)

        self.assertIn('class="skip-link"', rendered)
        self.assertIn('href="#main-content"', rendered)
        self.assertIn("@media (max-width: 680px)", rendered)

    def test_html_uses_distinctive_local_typography_and_respects_reduced_motion(self):
        rendered = render_html(self.snapshot)

        self.assertNotIn("Inter,", rendered)
        self.assertIn("Bahnschrift", rendered)
        self.assertIn("@media (prefers-reduced-motion: reduce)", rendered)

    def test_html_has_no_trailing_whitespace(self):
        rendered = render_html(self.snapshot)

        self.assertFalse(
            any(line != line.rstrip() for line in rendered.splitlines())
        )


if __name__ == "__main__":
    unittest.main()
