from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS_SCRIPT = ROOT / "skill/outbound-research-and-writing/scripts/check_readiness.py"


def _load_readiness():
    spec = importlib.util.spec_from_file_location("outbound_check_readiness", READINESS_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "account"


def run_case(payload: dict, output_root: Path) -> dict:
    result = _load_readiness().readiness(payload)
    account = str(payload.get("target_account", "account"))
    case_dir = output_root / slugify(account)
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "readiness.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if result["status"] == "needs_input":
        return {**result, "case_dir": str(case_dir), "research_map_created": False}

    template = (ROOT / "templates/research-map.md").read_text(encoding="utf-8")
    header = (
        f"<!-- Account: {payload['target_account']} | Domain: {payload['target_domain']} | "
        f"Persona: {payload['target_persona']} -->\n\n"
    )
    (case_dir / "research-map.md").write_text(header + template, encoding="utf-8")
    research_result = {
        "status": "needs_research",
        "missing": [],
        "sequence_created": False,
        "case_dir": str(case_dir),
        "research_map_created": True,
        "next_step": "Complete and review research-map.md before drafting.",
    }
    (case_dir / "readiness.json").write_text(json.dumps(research_result, indent=2) + "\n", encoding="utf-8")
    return research_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a fail-closed outbound case workspace from campaign input.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = run_case(payload, args.out.resolve())
    print(json.dumps(result, indent=2))
    return 2 if result["status"] == "needs_input" else 0


if __name__ == "__main__":
    raise SystemExit(main())
