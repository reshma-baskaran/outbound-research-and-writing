import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skill" / "outbound-research-and-writing" / "scripts" / "validate_sequence.py"
spec = importlib.util.spec_from_file_location("validate_sequence", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class ValidationTests(unittest.TestCase):
    def valid_payload(self):
        emails = [{"subject": "A specific operating question", "body": "A grounded pressure and a small next step."}]
        emails.extend({"subject": "", "body": f"Distinct follow-up role {number}."} for number in range(2, 7))
        return {"emails": emails, "source_urls": ["https://example.com/source"]}

    def test_valid_structure(self):
        self.assertEqual([], module.validate(self.valid_payload()))

    def test_only_first_email_has_subject(self):
        payload = self.valid_payload()
        payload["emails"][2]["subject"] = "New subject"
        self.assertIn("Email 3 must not have a subject.", module.validate(payload))

    def test_rejects_research_narration(self):
        payload = self.valid_payload()
        payload["emails"][0]["body"] = "I found this in your public materials."
        errors = module.validate(payload)
        self.assertTrue(any("banned research narration" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

