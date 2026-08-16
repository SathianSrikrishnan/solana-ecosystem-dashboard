import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "output" / "crypto-101.html"
DRAFT = ROOT / "docs" / "articles" / "2026-08-11-two-kinds-of-power-draft.md"


class CompanionPageTests(unittest.TestCase):
    def test_flagship_article_has_the_promised_story_structure(self):
        page = PAGE.read_text(encoding="utf-8")

        self.assertIn("Saraswati, Lakshmi", page)
        self.assertIn("and the Ledger", page)
        self.assertIn("I do not see my daughters every day", page)
        self.assertIn("two kinds of power", page.lower())
        self.assertIn("AI is polytheistic, not monotheistic", page)
        self.assertIn("Balaji Srinivasan", page)
        self.assertIn("The Saraswati test", page)
        self.assertIn("The Lakshmi test", page)
        self.assertIn('id="framework-test"', page)
        self.assertIn('aria-live="polite"', page)
        self.assertIn("data-test-question", page)
        self.assertIn("data-reel", page)
        self.assertIn("data-reel-next", page)
        self.assertIn("What I am testing in public", page)
        self.assertIn("Where the metaphor breaks", page)
        self.assertIn("Bitcoin", page)
        self.assertIn("Ethereum", page)
        self.assertIn("Solana", page)
        self.assertIn("Agentic", page)
        self.assertIn("From digital money to software that can spend", page)
        self.assertIn("validator hardware", page)
        self.assertIn("Open the Solana Observatory", page)
        self.assertIn('src="media/flagship-hero.png"', page)
        self.assertIn('src="media/flagship-saraswati.png"', page)
        self.assertIn('src="media/flagship-lakshmi.png"', page)
        self.assertIn('src="media/flagship-agentic-ledger.png"', page)
        self.assertIn('src="media/solana-logomark.svg"', page)
        self.assertNotIn("Satoshi as Brahma", page)
        self.assertNotIn("The old idea is not mine", page)
        self.assertNotIn("Mukesh Ambani", page)
        self.assertNotIn("Saraswati Advantage", page)
        self.assertNotIn('class="chapter-no"', page)
        self.assertNotRegex(page.lower(), r"saraswati and lakshmi (?:are|were) sisters")

    def test_article_draft_is_substantial_but_disciplined_and_records_critique(self):
        draft = DRAFT.read_text(encoding="utf-8")
        body = draft.split("## Draft", 1)[1].split("## Critique", 1)[0]
        words = re.findall(r"\b[\w’'-]+\b", body)

        self.assertGreaterEqual(len(words), 700)
        self.assertLessEqual(len(words), 950)
        self.assertIn("Saraswati test", body)
        self.assertIn("Lakshmi test", body)
        self.assertIn("seven", body.lower())
        self.assertIn("Balaji", body)
        self.assertIn("I do not see my daughters every day", body)
        self.assertIn("AI is polytheistic, not monotheistic", body)
        self.assertNotIn("The old idea is not mine", body)
        self.assertNotIn("Mukesh Ambani", body)
        self.assertIn("**Verdict:**", draft)


if __name__ == "__main__":
    unittest.main()
