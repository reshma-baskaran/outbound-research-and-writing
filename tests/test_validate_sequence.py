import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


module = load("validate_sequence", ROOT / "skill/outbound-research-and-writing/scripts/validate_sequence.py")
readiness_module = load("check_readiness", ROOT / "skill/outbound-research-and-writing/scripts/check_readiness.py")
init_module = load("init_workspace", ROOT / "scripts/init_workspace.py")
case_module = load("run_case", ROOT / "scripts/run_case.py")


class ValidationTests(unittest.TestCase):
    def valid_payload(self):
        campaign = {
            "sender_identity": "Alex",
            "sender_company": "Example",
            "offer": "Documented workflow review",
            "target_account": "Close",
            "target_persona": "VP Marketing",
            "campaign_objective": "Validate one operating problem",
            "cta": "Open to comparing notes?",
            "proof_points": ["Approved proof point"],
        }
        claims = [{
            "id": "close-001",
            "text": "Close publishes a CRM product page.",
            "source_url": "https://close.com/crm",
            "accessed_at": "2026-08-07",
            "status": "confirmed",
            "scope": "Company-published claim",
        }]
        emails = []
        for index, role in enumerate(module.TOUCH_ROLES, 1):
            emails.append({
                "role": role,
                "subject": "A specific operating question" if index == 1 else "",
                "body": f"Hi [first name],\n\nDistinct grounded message for touch {index} with a small next step.",
                "claim_ids": ["close-001"] if index == 1 else [],
                "cta": "Worth comparing notes?",
                "signoff": "Alex",
            })
        return {
            "readiness_status": "ready_for_review",
            "campaign": campaign,
            "research_map": "research-map.md",
            "claims": claims,
            "emails": emails,
        }

    def test_valid_review_ready_sequence(self):
        self.assertEqual([], module.validate(self.valid_payload()))

    def test_sparse_close_input_returns_needs_input(self):
        result = readiness_module.readiness({"target_account": "Close", "target_domain": "close.com"})
        self.assertEqual("needs_input", result["status"])
        self.assertIn("offer", result["missing"])
        self.assertIn("target_persona", result["missing"])
        self.assertFalse(result["sequence_created"])

    def test_run_case_does_not_create_sequence_or_research_map_when_input_is_missing(self):
        with TemporaryDirectory() as directory:
            result = case_module.run_case(
                {"target_account": "Close", "target_domain": "close.com"},
                Path(directory),
            )
            case_dir = Path(result["case_dir"])
            self.assertEqual("needs_input", result["status"])
            self.assertTrue((case_dir / "readiness.json").exists())
            self.assertFalse((case_dir / "research-map.md").exists())
            self.assertFalse((case_dir / "sequence.json").exists())

    def test_run_case_creates_only_research_scaffold_when_input_is_complete(self):
        campaign = {
            "sender_identity": "Alex",
            "sender_company": "Example",
            "offer": "Documented workflow review",
            "target_account": "Close",
            "target_domain": "close.com",
            "target_persona": "VP Marketing",
            "campaign_objective": "Validate one operating problem",
            "cta": "Open to comparing notes?",
            "proof_points": ["Approved proof point"],
        }
        with TemporaryDirectory() as directory:
            result = case_module.run_case(campaign, Path(directory))
            case_dir = Path(result["case_dir"])
            self.assertEqual("needs_research", result["status"])
            self.assertTrue((case_dir / "research-map.md").exists())
            self.assertFalse((case_dir / "sequence.json").exists())

    def test_run_case_preserves_completed_research_and_readiness_on_rerun(self):
        campaign = {
            "sender_identity": "Alex",
            "sender_company": "Example",
            "offer": "Documented workflow review",
            "target_account": "Close",
            "target_domain": "close.com",
            "target_persona": "VP Marketing",
            "campaign_objective": "Validate one operating problem",
            "cta": "Open to comparing notes?",
            "proof_points": ["Approved proof point"],
        }
        with TemporaryDirectory() as directory:
            root = Path(directory)
            first = case_module.run_case(campaign, root)
            case_dir = Path(first["case_dir"])
            research = case_dir / "research-map.md"
            readiness = case_dir / "readiness.json"
            research.write_text("completed research\n", encoding="utf-8")
            readiness.write_text('{"status":"ready_for_review"}\n', encoding="utf-8")

            second = case_module.run_case(campaign, root)

            self.assertEqual("completed research\n", research.read_text(encoding="utf-8"))
            self.assertEqual("ready_for_review", second["status"])
            self.assertTrue(second["existing_case_preserved"])
            self.assertFalse(second["research_map_created"])

    def test_run_case_overwrite_requires_explicit_flag(self):
        campaign = {
            "sender_identity": "Alex",
            "sender_company": "Example",
            "offer": "Documented workflow review",
            "target_account": "Close",
            "target_domain": "close.com",
            "target_persona": "VP Marketing",
            "campaign_objective": "Validate one operating problem",
            "cta": "Open to comparing notes?",
            "proof_points": ["Approved proof point"],
        }
        with TemporaryDirectory() as directory:
            root = Path(directory)
            first = case_module.run_case(campaign, root)
            case_dir = Path(first["case_dir"])
            research = case_dir / "research-map.md"
            research.write_text("completed research\n", encoding="utf-8")

            replaced = case_module.run_case(campaign, root, overwrite=True)

            self.assertNotEqual("completed research\n", research.read_text(encoding="utf-8"))
            self.assertTrue(replaced["research_map_created"])

    def test_rejects_blocked_placeholders(self):
        payload = self.valid_payload()
        payload["emails"][0]["body"] = "Hi [first name],\n\n[BLOCKED: offer missing]"
        self.assertTrue(any("placeholder" in error for error in module.validate(payload)))

    def test_requires_first_name_greeting_but_allows_its_token(self):
        payload = self.valid_payload()
        self.assertEqual([], module.validate(payload))
        payload["emails"][0]["body"] = "A grounded message without a greeting."
        errors = module.validate(payload)
        self.assertTrue(any("must start" in error for error in errors))

    def test_rejects_any_other_unresolved_recipient_placeholder(self):
        payload = self.valid_payload()
        payload["emails"][0]["body"] = "Hi [first name],\n\nRelevant idea for [company name]."
        errors = module.validate(payload)
        self.assertTrue(any("placeholder" in error for error in errors))

    def test_rejects_duplicate_bodies(self):
        payload = self.valid_payload()
        for email in payload["emails"]:
            email["body"] = "Hi [first name],\n\nClose has doubled revenue."
        self.assertIn("Sequence contains duplicate email bodies.", module.validate(payload))

    def test_rejects_bad_source_and_unknown_claim(self):
        payload = self.valid_payload()
        payload["claims"][0]["source_url"] = "http://x"
        payload["emails"][0]["claim_ids"] = ["missing"]
        errors = module.validate(payload)
        self.assertTrue(any("valid HTTPS" in error for error in errors))
        self.assertTrue(any("unknown claim ids" in error for error in errors))

    def test_rejects_inferred_claims_in_recipient_copy_and_wrong_signoff(self):
        payload = self.valid_payload()
        payload["claims"][0]["status"] = "inferred"
        payload["emails"][0]["signoff"] = "Someone else"
        errors = module.validate(payload)
        self.assertTrue(any("cannot state inferred claims" in error for error in errors))
        self.assertTrue(any("signoff does not match" in error for error in errors))

    def test_rejects_missing_campaign_fields_and_wrong_status(self):
        payload = self.valid_payload()
        payload["campaign"]["offer"] = ""
        payload["readiness_status"] = "needs_input"
        errors = module.validate(payload)
        self.assertTrue(any("offer" in error for error in errors))
        self.assertTrue(any("readiness_status" in error for error in errors))

    def test_checks_research_map_on_cli_path(self):
        payload = self.valid_payload()
        with TemporaryDirectory() as directory:
            errors = module.validate(payload, base_dir=Path(directory))
        self.assertTrue(any("research_map does not exist" in error for error in errors))

    def test_only_first_email_has_subject(self):
        payload = self.valid_payload()
        payload["emails"][2]["subject"] = "New subject"
        self.assertIn("Email 3 must not have a subject.", module.validate(payload))

    def test_rejects_research_narration(self):
        payload = self.valid_payload()
        payload["emails"][0]["body"] = "Hi [first name],\n\nI found this in your public materials."
        errors = module.validate(payload)
        self.assertTrue(any("banned research narration" in error for error in errors))

    def test_workspace_initializer_creates_new_templates(self):
        with TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            created, skipped = init_module.install_workspace(workspace)
            self.assertGreater(len(created), 0)
            self.assertEqual([], skipped)
            self.assertTrue((workspace / "templates/research-map.md").exists())
            self.assertTrue((workspace / "templates/sequence.json").exists())
            self.assertTrue((workspace / "templates/campaign-input.json").exists())


if __name__ == "__main__":
    unittest.main()
