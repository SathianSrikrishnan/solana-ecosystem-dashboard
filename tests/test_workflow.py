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
        self.assertIn(
            "python scripts/refresh_economy.py --snapshot output/report.json --output output",
            workflow,
        )
        self.assertLess(
            workflow.index("python scripts/generate.py"),
            workflow.index("python scripts/refresh_economy.py"),
        )
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("uses: actions/checkout@v7", workflow)
        self.assertIn("uses: actions/setup-python@v7", workflow)
        self.assertIn("DUNE_API_KEY", workflow)
        self.assertIn("python scripts/refresh_dune.py", workflow)

    def test_pages_workflow_publishes_the_static_output(self):
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("path: output", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("workflow_run:", workflow)
        self.assertIn('workflows: ["Refresh Solana reports"]', workflow)
        self.assertIn("conclusion == 'success'", workflow)


if __name__ == "__main__":
    unittest.main()
