import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SubmissionPackageTests(unittest.TestCase):
    def test_walkthrough_and_release_checklist_are_bounded_and_linked(self):
        demo = (ROOT / "docs" / "DEMO-SCRIPT.md").read_text(encoding="utf-8")
        checklist = (ROOT / "docs" / "SUBMISSION-CHECKLIST.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("30-minute recording session", demo)
        self.assertIn("10–12 minute", demo)
        self.assertIn("Inside MonkeDAO", demo)
        self.assertIn("Do not submit", checklist)
        self.assertIn("explicit action-time approval", checklist)
        self.assertIn("GitHub Actions", checklist)
        self.assertIn("https://sathian.ai/writings/inside-monkedao", checklist)


if __name__ == "__main__":
    unittest.main()
