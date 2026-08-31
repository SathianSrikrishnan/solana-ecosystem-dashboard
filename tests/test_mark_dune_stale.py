import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "mark_dune_stale.py"


class MarkDuneStaleTests(unittest.TestCase):
    def test_cli_preserves_values_and_marks_only_dune_metrics_stale(self):
        snapshot = json.loads((ROOT / "output" / "report.json").read_text(encoding="utf-8"))
        dune_before = {
            metric_id: metric["value"]
            for metric_id, metric in snapshot["metrics"].items()
            if metric.get("source", {}).get("name") == "Dune"
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            snapshot_path = temp / "report.json"
            output_dir = temp / "output"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--snapshot",
                    str(snapshot_path),
                    "--output",
                    str(output_dir),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
            for metric_id, value in dune_before.items():
                self.assertEqual(report["metrics"][metric_id]["value"], value)
                self.assertEqual(report["metrics"][metric_id]["status"], "stale")
            public_output = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertNotRegex(
                public_output,
                r"(?i)\b(?:http|status(?:\s+code)?)\s*402\b|\bpayment required\b",
            )
            self.assertNotIn("billing cycle", public_output.lower())


if __name__ == "__main__":
    unittest.main()
