import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "import_dune_fee_payers.py"


class ImportDuneFeePayersTests(unittest.TestCase):
    valid_csv = """activity_date,unique_fee_payers
2026-07-27,100
2026-07-28,110
2026-07-29,120
2026-07-30,130
2026-07-31,140
2026-08-01,150
2026-08-02,160
"""

    def _snapshot(self):
        return {
            "schema_version": "0.2.0",
            "generated_at": "2026-08-03T11:00:00Z",
            "summary": {"status": "healthy", "headline": "RPC is healthy."},
            "metrics": {},
        }

    def _run_import(self, input_path, snapshot_path, output_dir):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--input",
                str(input_path),
                "--snapshot",
                str(snapshot_path),
                "--output",
                str(output_dir),
                "--source-url",
                "https://dune.com/queries/1234567",
                "--collected-at",
                "2026-08-03T12:00:00Z",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_import_command_exists(self):
        self.assertTrue(SCRIPT_PATH.exists(), "Dune import command is missing")

    def test_valid_import_updates_all_report_formats(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "fee_payers.csv"
            snapshot_path = temp_path / "base.json"
            output_dir = temp_path / "output"
            input_path.write_text(self.valid_csv, encoding="utf-8")
            snapshot_path.write_text(
                json.dumps(self._snapshot()),
                encoding="utf-8",
            )

            result = self._run_import(input_path, snapshot_path, output_dir)

            self.assertEqual(result.returncode, 0, result.stderr)
            for filename in ("report.json", "report.md", "index.html"):
                self.assertTrue((output_dir / filename).exists())
            report = json.loads(
                (output_dir / "report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                report["metrics"]["daily_unique_successful_fee_payers"]["value"],
                160,
            )
            self.assertIn(
                "Daily unique successful fee payers",
                (output_dir / "report.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                'data-metric="daily_unique_successful_fee_payers"',
                (output_dir / "index.html").read_text(encoding="utf-8"),
            )

    def test_invalid_import_leaves_existing_reports_untouched(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "fee_payers.csv"
            snapshot_path = temp_path / "base.json"
            output_dir = temp_path / "output"
            output_dir.mkdir()
            input_path.write_text(
                "activity_date,unique_fee_payers\n",
                encoding="utf-8",
            )
            snapshot_path.write_text(
                json.dumps(self._snapshot()),
                encoding="utf-8",
            )
            for filename in ("report.json", "report.md", "index.html"):
                (output_dir / filename).write_text("original", encoding="utf-8")

            result = self._run_import(input_path, snapshot_path, output_dir)

            self.assertNotEqual(result.returncode, 0)
            for filename in ("report.json", "report.md", "index.html"):
                self.assertEqual(
                    (output_dir / filename).read_text(encoding="utf-8"),
                    "original",
                )


if __name__ == "__main__":
    unittest.main()
