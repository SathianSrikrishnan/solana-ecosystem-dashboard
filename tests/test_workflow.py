import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RefreshWorkflowTests(unittest.TestCase):
    def test_refresh_workflow_is_bounded_and_tested(self):
        workflow_path = ROOT / ".github" / "workflows" / "refresh.yml"
        workflow = workflow_path.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("cron: '17 */6 * * *'", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python scripts/generate.py", workflow)
        self.assertIn("cancel-in-progress: false", workflow)


if __name__ == "__main__":
    unittest.main()

