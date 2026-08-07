from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = (
    "sender_identity",
    "sender_company",
    "offer",
    "target_account",
    "target_domain",
    "target_persona",
    "campaign_objective",
    "cta",
    "proof_points",
)


def has_value(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(str(item).strip() for item in value)
    return value is not None


def readiness(payload: dict) -> dict:
    missing = [field for field in REQUIRED_FIELDS if not has_value(payload.get(field))]
    status = "needs_input" if missing else "ready_for_research"
    return {
        "status": status,
        "missing": missing,
        "sequence_created": False,
        "next_step": "Supply only the missing fields." if missing else "Build and review the account research map.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail closed when a campaign lacks required inputs.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    result = readiness(payload)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 2 if result["status"] == "needs_input" else 0


if __name__ == "__main__":
    raise SystemExit(main())
