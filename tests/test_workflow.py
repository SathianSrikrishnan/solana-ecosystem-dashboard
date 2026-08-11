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
        self.assertIn("execute_dune_queries:", workflow)
        self.assertIn("type: boolean", workflow)
        self.assertIn("python scripts/execute_dune_queries.py", workflow)
        self.assertIn("python scripts/refresh_dune.py", workflow)
        self.assertLess(
            workflow.index("python scripts/execute_dune_queries.py"),
            workflow.index("python scripts/refresh_dune.py"),
        )

    def test_pages_workflow_publishes_the_static_output(self):
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("path: output", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("workflow_run:", workflow)
        self.assertIn('workflows: ["Refresh Solana reports"]', workflow)
        self.assertIn("conclusion == 'success'", workflow)

    def test_dune_workflow_checks_daily_but_executes_only_when_three_days_old(self):
        workflow_path = ROOT / ".github" / "workflows" / "dune-adoption.yml"
        workflow = workflow_path.read_text(encoding="utf-8")

        self.assertIn("cron: '43 7 * * *'", workflow)
        self.assertIn("concurrency:", workflow)
        self.assertIn("group: report-refresh", workflow)
        self.assertIn("python scripts/dune_refresh_due.py", workflow)
        self.assertIn("python scripts/execute_dune_queries.py", workflow)
        self.assertIn("steps.due.outputs.due == 'true'", workflow)
        self.assertIn("python scripts/refresh_dune.py", workflow)
        self.assertIn("DUNE_API_KEY", workflow)


if __name__ == "__main__":
    unittest.main()
