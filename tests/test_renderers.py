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
            "schema_version": "0.3.0",
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
                    "why_it_matters": "It confirms the selected data path responds.",
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
                    "why_it_matters": "It approximates live application throughput.",
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
                    "why_it_matters": "It shows current validator participation.",
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
            "financial-rails",
            "methods",
        ):
            self.assertIn(f'href="#{section}"', rendered)
            self.assertIn(f'id="{section}"', rendered)

        self.assertIn('aria-label="Dashboard sections"', rendered)

    def test_html_opens_with_six_product_questions(self):
        rendered = render_html(self.snapshot)

        self.assertIn("Is Solana working?", rendered)
        self.assertIn(
            "Are people and applications returning?",
            rendered,
        )
        self.assertIn("Is useful economic activity growing?", rendered)
        self.assertIn(
            "Is the network resilient and decentralized?", rendered
        )
        self.assertIn("Is Solana continuing to compound?", rendered)
        self.assertIn(
            "Is Solana becoming real financial infrastructure?", rendered
        )

    def test_html_opens_with_six_balanced_signal_states(self):
        rendered = render_html(self.snapshot)

        self.assertEqual(rendered.count('class="signal-card"'), 6)
        self.assertIn("RPC health", rendered)
        self.assertIn("Active validators", rendered)
        self.assertEqual(rendered.count("Awaiting verified data"), 4)
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
        self.assertEqual(rendered.count("Data adapter planned"), 4)
        self.assertIn("Expected evidence:", rendered)

    def test_html_explains_measurement_value_and_interpretive_risk(self):
        rendered = render_html(self.snapshot)

        self.assertIn("What this measures", rendered)
        self.assertIn("Why it matters", rendered)
        self.assertIn("What could fool you", rendered)
        self.assertIn("See the evidence", rendered)
        self.assertIn(
            "It confirms the selected data path responds.", rendered
        )

    def test_html_keeps_evidence_and_interpretation_visually_separate(self):
        rendered = render_html(self.snapshot)

        self.assertIn("Verified facts", rendered)
        self.assertIn("Interpretation", rendered)
        self.assertIn("Automatic evidence briefing", rendered)
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

    def test_html_labels_deterministic_explanation_without_claiming_ai(self):
        self.snapshot["analysis"] = {
            "status": "ok",
            "kind": "deterministic",
            "current_reading": "No comparison crossed the review threshold.",
            "supporting_metric_ids": [],
            "uncertainty": "Direction is not automatically good or bad.",
            "generated_at": "2026-07-27T22:01:00Z",
            "model": "deterministic-observatory-v1",
        }

        rendered = render_html(self.snapshot)

        self.assertIn("Deterministic", rendered)
        self.assertIn("Automatic evidence briefing", rendered)
        self.assertIn("Engine:", rendered)
        self.assertNotIn("AI-generated", rendered)

    def test_html_shows_unavailable_metrics_without_inventing_a_zero(self):
        self.snapshot["metrics"]["rpc_health"]["value"] = None
        self.snapshot["metrics"]["rpc_health"]["status"] = "unavailable"

        rendered = render_html(self.snapshot)

        self.assertIn('data-status="unavailable"', rendered)
        self.assertIn("Not available", rendered)
        self.assertIn("2 of 3 metrics reporting", rendered)
        self.assertNotIn(">None<", rendered)

    def test_html_separates_source_reliability_from_directional_comparison(self):
        first_day = __import__("datetime").date(2026, 7, 27)
        self.snapshot["metrics"]["estimated_non_vote_tps"]["series"] = [
            {
                "observed_at": str(first_day + __import__("datetime").timedelta(days=index)),
                "value": value,
            }
            for index, value in enumerate([100] * 7 + [125] * 7)
        ]

        rendered = render_html(self.snapshot)

        self.assertIn("Data reporting", rendered)
        self.assertIn("7-day average +25.0%", rendered)
        self.assertIn("Jul 27–Aug 02", rendered)
        self.assertIn("Aug 03–Aug 09", rendered)
        self.assertIn("Direction is not a health verdict", rendered)
        self.assertNotIn('status-ok">ok</span>', rendered)

        self.snapshot["comparisons"] = {
            "estimated_non_vote_tps": {
                "metric_id": "estimated_non_vote_tps",
                "status": "ok",
                "grain": "daily",
                "current_average": 125.0,
                "previous_average": 100.0,
                "absolute_change": 25.0,
                "percent_change": 25.0,
                "direction": "increased",
                "previous_window": ["2026-07-27", "2026-08-02"],
                "current_window": ["2026-08-03", "2026-08-09"],
                "reason": None,
            }
        }
        markdown = render_markdown(self.snapshot)
        self.assertIn("7-day average change: `+25.0%`", markdown)

    def test_html_includes_mobile_layout_and_accessible_skip_link(self):
        rendered = render_html(self.snapshot)

        self.assertIn('class="skip-link"', rendered)
        self.assertIn('href="#main-content"', rendered)
        self.assertIn("@media (max-width: 680px)", rendered)

    def test_html_renders_a_compact_sourced_seven_era_history(self):
        self.snapshot["timeline"] = [
            {
                "order": index,
                "period": str(2019 + index),
                "title": f"Era {index}",
                "fact": f"Fact {index}",
                "interpretation": f"Interpretation {index}",
                "source_label": f"Source {index}",
                "source_url": f"https://example.com/{index}",
                "source_type": "primary",
            }
            for index in range(1, 8)
        ]

        rendered = render_html(self.snapshot)

        self.assertIn('id="history"', rendered)
        self.assertEqual(rendered.count('class="era"'), 7)
        self.assertIn("Why now?", rendered)
        self.assertIn("Verified historical fact", rendered)
        self.assertIn("Observatory interpretation", rendered)
        self.assertIn('href="https://example.com/7"', rendered)

    def test_html_includes_a_beginner_learn_and_project_guide(self):
        rendered = render_html(self.snapshot)

        self.assertIn('href="#learn"', rendered)
        self.assertIn('id="learn"', rendered)
        self.assertIn("How do I use this dashboard?", rendered)
        self.assertIn("How do I learn the concepts?", rendered)
        self.assertIn("Why might Solana matter?", rendered)
        self.assertIn("Why was this built?", rendered)
        self.assertIn("Tooth Fairy Network", rendered)
        self.assertIn("planned", rendered.lower())
        self.assertIn("Start with the six questions", rendered)

    def test_html_shows_an_honest_identity_and_automation_lens(self):
        base = self.snapshot["metrics"]["active_validators"]
        for metric_id, label, value in (
            ("daily_unique_successful_signers", "Successful signers", 1000),
            ("daily_unique_jupiter_swap_signers", "Jupiter swap signers", 100),
            ("jupiter_swap_signer_7d_return_rate", "Jupiter return rate", 25.0),
        ):
            self.snapshot["metrics"][metric_id] = {
                **base,
                "id": metric_id,
                "section": "adoption",
                "label": label,
                "value": value,
                "unit": "percent" if "rate" in metric_id else "wallet addresses",
            }

        rendered = render_html(self.snapshot)

        self.assertIn("Identity and automation lens", rendered)
        self.assertIn("Jupiter share of successful signers", rendered)
        self.assertIn("10.0%", rendered)
        self.assertIn("Returning Jupiter signer rate", rendered)
        self.assertIn("We cannot classify bots yet", rendered)
        self.assertIn("Evidence still needed", rendered)

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
