import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solana_observatory.pipeline import write_reports


class PipelineTests(unittest.TestCase):
    def test_writes_all_required_report_formats(self):
        snapshot = {
            "schema_version": "0.1.0",
            "generated_at": "2026-07-27T22:00:00Z",
            "summary": {"status": "healthy", "headline": "RPC is healthy."},
            "metrics": {},
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            written = write_reports(snapshot, output_dir)

            self.assertEqual(
                set(written),
                {
                    output_dir / "report.json",
                    output_dir / "report.md",
                    output_dir / "index.html",
                },
            )
            self.assertEqual(
                json.loads(
                    (output_dir / "report.json").read_text(encoding="utf-8")
                ),
                snapshot,
            )
            self.assertIn(
                "Solana Ecosystem Report",
                (output_dir / "report.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "<!doctype html>",
                (output_dir / "index.html").read_text(encoding="utf-8").lower(),
            )


if __name__ == "__main__":
    unittest.main()
