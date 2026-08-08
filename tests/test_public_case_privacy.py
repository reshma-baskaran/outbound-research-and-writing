from pathlib import Path
import unittest


CASE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "cases"
    / "event-led-insurance-outreach.md"
)


class PublicCasePrivacyTests(unittest.TestCase):
    def test_case_declares_real_source_and_outcome_boundary(self):
        text = CASE_PATH.read_text(encoding="utf-8")
        self.assertIn("real senior-operator outreach packet", text)
        self.assertIn("## Outcome boundary", text)
        self.assertIn("does **not** establish that they were sent", text)

    def test_case_excludes_source_identifiers(self):
        text = CASE_PATH.read_text(encoding="utf-8").lower()
        prohibited = (
            "axa xl",
            "lloyd's",
            "markel",
            "the hartford",
            "metlife",
            "principal financial",
            "nuplay",
            "nurix",
            "linkedin.com",
        )
        for value in prohibited:
            with self.subTest(value=value):
                self.assertNotIn(value, text)


if __name__ == "__main__":
    unittest.main()
