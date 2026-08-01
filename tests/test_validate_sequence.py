import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skill" / "outbound-research-and-writing" / "scripts" / "validate_sequence.py"
spec = importlib.util.spec_from_file_location("validate_sequence", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


INIT_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_workspace.py"
init_spec = importlib.util.spec_from_file_location("init_workspace", INIT_SCRIPT)
init_module = importlib.util.module_from_spec(init_spec)
assert init_spec.loader
init_spec.loader.exec_module(init_module)


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

    def test_workspace_initializer_creates_blank_templates(self):
        with TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            created, skipped = init_module.install_workspace(workspace)
            self.assertGreater(len(created), 0)
            self.assertEqual([], skipped)
            self.assertTrue((workspace / "templates/research-map.md").exists())
            self.assertTrue((workspace / "templates/sequence.json").exists())


if __name__ == "__main__":
    unittest.main()
