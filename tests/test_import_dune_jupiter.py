import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "import_dune_jupiter.py"


class ImportDuneJupiterTests(unittest.TestCase):
    valid_csv = """activity_date,unique_jupiter_swap_signers,jupiter_fee_payer_overlap,returning_jupiter_swap_signers
2026-07-27,50,40,20
2026-07-28,55,45,24
2026-07-29,60,50,27
2026-07-30,65,55,31
2026-07-31,70,60,35
2026-08-01,75,65,40
2026-08-02,80,70,44
"""

    def _population_metric(self, metric_id, values):
        return {
            "id": metric_id,
            "section": "adoption",
            "label": metric_id.replace("_", " ").title(),
            "value": values[-1],
            "unit": "wallet addresses",
            "status": "ok",
            "definition": "Test population.",
            "why_it_matters": "It provides a comparison population.",
            "source": {
                "name": "Dune",
                "method": "test fixture",
                "url": "https://dune.com/queries/1234567",
            },
            "collected_at": "2026-08-03T11:00:00Z",
            "source_time": "2026-08-02",
            "confidence": "high",
            "caveat": "Wallet addresses are not people.",
            "series": [
                {"observed_at": f"2026-07-{day:02d}", "value": value}
                for day, value in zip(range(27, 32), values[:5])
            ]
            + [
                {"observed_at": "2026-08-01", "value": values[5]},
                {"observed_at": "2026-08-02", "value": values[6]},
            ],
        }

    def _snapshot(self):
        fee_payers = self._population_metric(
            "daily_unique_successful_fee_payers",
            [100, 110, 120, 130, 140, 150, 160],
        )
        signers = self._population_metric(
            "daily_unique_successful_signers",
            [130, 140, 150, 160, 170, 180, 190],
        )
        return {
            "schema_version": "0.3.0",
            "generated_at": "2026-08-03T11:00:00Z",
            "summary": {"status": "healthy", "headline": "RPC is healthy."},
            "metrics": {fee_payers["id"]: fee_payers, signers["id"]: signers},
        }

    def _run(self, input_path, snapshot_path, output_dir):
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
                "https://dune.com/queries/2468101",
                "--collected-at",
                "2026-08-03T12:00:00Z",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_import_command_exists(self):
        self.assertTrue(SCRIPT_PATH.exists(), "Jupiter import command is missing")

    def test_valid_import_updates_all_formats_atomically(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "jupiter.csv"
            snapshot_path = temp_path / "base.json"
            output_dir = temp_path / "output"
            input_path.write_text(self.valid_csv, encoding="utf-8")
            snapshot_path.write_text(json.dumps(self._snapshot()), encoding="utf-8")

            result = self._run(input_path, snapshot_path, output_dir)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(
                (output_dir / "report.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                report["metrics"]["daily_unique_jupiter_swap_signers"]["value"],
                80,
            )
            self.assertEqual(
                report["metrics"]["daily_jupiter_fee_payer_overlap"]["value"],
                70,
            )
            self.assertEqual(
                report["metrics"]["jupiter_swap_signer_7d_return_rate"]["value"],
                55.0,
            )
            markdown = (output_dir / "report.md").read_text(encoding="utf-8")
            html = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn("Jupiter Swap seven-day return rate", markdown)
            self.assertIn('data-metric="daily_jupiter_fee_payer_overlap"', html)

    def test_cross_population_failure_preserves_existing_outputs(self):
        invalid_csvs = (
            self.valid_csv.replace("2026-08-02,80,70,44", "2026-08-02,191,70,44"),
            self.valid_csv.replace("2026-08-02,80,70,44", "2026-08-02,80,161,44"),
        )
        for invalid_csv in invalid_csvs:
            with self.subTest(invalid_csv=invalid_csv):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    input_path = temp_path / "jupiter.csv"
                    snapshot_path = temp_path / "base.json"
                    output_dir = temp_path / "output"
                    output_dir.mkdir()
                    input_path.write_text(invalid_csv, encoding="utf-8")
                    snapshot_path.write_text(
                        json.dumps(self._snapshot()), encoding="utf-8"
                    )
                    for filename in ("report.json", "report.md", "index.html"):
                        (output_dir / filename).write_text(
                            "original", encoding="utf-8"
                        )

                    result = self._run(input_path, snapshot_path, output_dir)

                    self.assertNotEqual(result.returncode, 0)
                    for filename in ("report.json", "report.md", "index.html"):
                        self.assertEqual(
                            (output_dir / filename).read_text(encoding="utf-8"),
                            "original",
                        )


if __name__ == "__main__":
    unittest.main()
