import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "output" / "crypto-101.html"
DRAFT = ROOT / "docs" / "articles" / "2026-08-11-two-kinds-of-power-draft.md"


class CompanionPageTests(unittest.TestCase):
    def test_short_article_has_the_promised_beginner_structure(self):
        page = PAGE.read_text(encoding="utf-8")

        self.assertIn("Two Kinds of Power", page)
        self.assertIn("Bitcoin", page)
        self.assertIn("Ethereum", page)
        self.assertIn("Solana", page)
        self.assertIn("Agentic rails", page)
        self.assertIn("validator hardware", page)
        self.assertIn("Open the Solana Observatory", page)
        self.assertIn('src="media/crypto-101-balance.png"', page)
        self.assertIn('src="media/solana-logomark.svg"', page)
        self.assertNotIn("Satoshi as Brahma", page)
        self.assertNotRegex(page.lower(), r"saraswati and lakshmi (?:are|were) sisters")

    def test_article_draft_is_short_and_records_the_critique(self):
        draft = DRAFT.read_text(encoding="utf-8")
        body = draft.split("## Draft", 1)[1].split("## Critique", 1)[0]
        words = re.findall(r"\b[\w’'-]+\b", body)

        self.assertGreaterEqual(len(words), 250)
        self.assertLessEqual(len(words), 350)
        self.assertIn("**Verdict:**", draft)


if __name__ == "__main__":
    unittest.main()
