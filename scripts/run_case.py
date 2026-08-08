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


def _existing_status(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return fallback
    return str(saved.get("status", fallback)).strip() or fallback


def run_case(payload: dict, output_root: Path, *, overwrite: bool = False) -> dict:
    result = _load_readiness().readiness(payload)
    account = str(payload.get("target_account", "account"))
    case_dir = output_root / slugify(account)
    case_dir.mkdir(parents=True, exist_ok=True)
    readiness_path = case_dir / "readiness.json"
    research_path = case_dir / "research-map.md"
    if result["status"] == "needs_input":
        if overwrite or not readiness_path.exists():
            readiness_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return {
            **result,
            "case_dir": str(case_dir),
            "research_map_created": False,
            "existing_case_preserved": readiness_path.exists() and not overwrite,
        }

    if research_path.exists() and not overwrite:
        status = _existing_status(readiness_path, "needs_research")
        return {
            "status": status,
            "missing": [],
            "sequence_created": (case_dir / "sequence.json").exists(),
            "case_dir": str(case_dir),
            "research_map_created": False,
            "existing_case_preserved": True,
            "next_step": "Resume the existing case. Use --overwrite only to intentionally replace its research scaffold.",
        }

    template = (ROOT / "templates/research-map.md").read_text(encoding="utf-8")
    header = (
        f"<!-- Account: {payload['target_account']} | Domain: {payload['target_domain']} | "
        f"Persona: {payload['target_persona']} -->\n\n"
    )
    research_path.write_text(header + template, encoding="utf-8")
    research_result = {
        "status": "needs_research",
        "missing": [],
        "sequence_created": False,
        "case_dir": str(case_dir),
        "research_map_created": True,
        "next_step": "Complete and review research-map.md before drafting.",
    }
    readiness_path.write_text(json.dumps(research_result, indent=2) + "\n", encoding="utf-8")
    return research_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a fail-closed outbound case workspace from campaign input.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true", help="intentionally replace an existing research scaffold")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = run_case(payload, args.out.resolve(), overwrite=args.overwrite)
    print(json.dumps(result, indent=2))
    return 2 if result["status"] == "needs_input" else 0


if __name__ == "__main__":
    raise SystemExit(main())
