from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


BANNED = (
    "public materials",
    "public positioning",
    "i found",
    "public signal",
    "the data suggests",
    "one concrete example",
    "one more reason",
    "i thought this may be relevant",
)
PLACEHOLDER_RE = re.compile(r"\b(blocked|todo|tbd|placeholder|insert|lorem ipsum)\b|\[[^]]+\]", re.I)
TOUCH_ROLES = (
    "pressure_and_consequence",
    "buyer_seat_expansion",
    "practical_test",
    "new_angle",
    "narrow_workflow",
    "close_the_loop",
)
REQUIRED_CAMPAIGN_FIELDS = (
    "sender_identity",
    "sender_company",
    "offer",
    "target_account",
    "target_persona",
    "campaign_objective",
    "cta",
    "proof_points",
)


def _is_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _has_value(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(str(item).strip() for item in value)
    return value is not None


def validate(payload: dict, *, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []

    if payload.get("readiness_status") != "ready_for_review":
        errors.append("readiness_status must be ready_for_review before a sequence can pass QA.")

    campaign = payload.get("campaign")
    if not isinstance(campaign, dict):
        errors.append("Sequence must embed a campaign object.")
    else:
        for field in REQUIRED_CAMPAIGN_FIELDS:
            if not _has_value(campaign.get(field)):
                errors.append(f"Campaign is missing required field: {field}.")

    research_map = payload.get("research_map")
    if not isinstance(research_map, str) or not research_map.strip():
        errors.append("Sequence must reference a research_map file.")
    elif base_dir is not None and not (base_dir / research_map).resolve().is_file():
        errors.append(f"research_map does not exist: {research_map}.")

    claims = payload.get("claims")
    claim_ids: set[str] = set()
    claim_statuses: dict[str, str] = {}
    if not isinstance(claims, list) or not claims:
        errors.append("Sequence must include at least one structured claim.")
    else:
        for index, claim in enumerate(claims, 1):
            if not isinstance(claim, dict):
                errors.append(f"Claim {index} must be an object.")
                continue
            claim_id = str(claim.get("id", "")).strip()
            if not claim_id:
                errors.append(f"Claim {index} has no id.")
            elif claim_id in claim_ids:
                errors.append(f"Duplicate claim id: {claim_id}.")
            else:
                claim_ids.add(claim_id)
            if not str(claim.get("text", "")).strip():
                errors.append(f"Claim {index} has no text.")
            if not _is_https_url(claim.get("source_url")):
                errors.append(f"Claim {index} must contain a valid HTTPS source_url.")
            if not str(claim.get("accessed_at", "")).strip():
                errors.append(f"Claim {index} is missing accessed_at.")
            if claim.get("status") not in {"confirmed", "inferred"}:
                errors.append(f"Claim {index} status must be confirmed or inferred.")
            elif claim_id:
                claim_statuses[claim_id] = str(claim["status"])
            if not str(claim.get("scope", "")).strip():
                errors.append(f"Claim {index} is missing scope.")

    emails = payload.get("emails")
    if not isinstance(emails, list) or len(emails) != 6:
        return sorted(set(errors + ["Sequence must contain exactly six emails."]))

    normalized_bodies: list[str] = []
    observed_roles: list[str] = []
    for index, email in enumerate(emails, 1):
        if not isinstance(email, dict):
            errors.append(f"Email {index} must be an object.")
            continue
        body = str(email.get("body", "")).strip()
        subject = str(email.get("subject", "")).strip()
        role = str(email.get("role", "")).strip()
        observed_roles.append(role)
        if role != TOUCH_ROLES[index - 1]:
            errors.append(f"Email {index} role must be {TOUCH_ROLES[index - 1]}.")
        if not body:
            errors.append(f"Email {index} has no body.")
        if PLACEHOLDER_RE.search(body):
            errors.append(f"Email {index} contains unresolved placeholder or blocked content.")
        if index == 1 and not subject:
            errors.append("Email 1 must have a subject.")
        if index > 1 and subject:
            errors.append(f"Email {index} must not have a subject.")
        lowered = body.casefold()
        for phrase in BANNED:
            if phrase in lowered:
                errors.append(f"Email {index} contains banned research narration: {phrase!r}.")
        if len(body.split()) > 160:
            errors.append(f"Email {index} is longer than 160 words.")
        normalized = re.sub(r"\W+", " ", lowered).strip()
        if normalized:
            normalized_bodies.append(normalized)
        referenced = email.get("claim_ids")
        if not isinstance(referenced, list):
            errors.append(f"Email {index} must contain a claim_ids array.")
        else:
            unknown = sorted({str(value) for value in referenced} - claim_ids)
            if unknown:
                errors.append(f"Email {index} references unknown claim ids: {', '.join(unknown)}.")
            inferred = sorted({str(value) for value in referenced if claim_statuses.get(str(value)) == "inferred"})
            if inferred:
                errors.append(f"Email {index} cannot state inferred claims: {', '.join(inferred)}.")
        if not str(email.get("cta", "")).strip():
            errors.append(f"Email {index} has no CTA.")
        if not str(email.get("signoff", "")).strip():
            errors.append(f"Email {index} has no signoff.")
        elif isinstance(campaign, dict):
            sender = str(campaign.get("sender_identity", "")).strip()
            if sender and sender.casefold() not in str(email.get("signoff", "")).casefold():
                errors.append(f"Email {index} signoff does not match sender_identity.")

    if len(normalized_bodies) != len(set(normalized_bodies)):
        errors.append("Sequence contains duplicate email bodies.")
    if tuple(observed_roles) != TOUCH_ROLES:
        errors.append("Sequence does not contain the six required touch roles in order.")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sequence structure, evidence lineage, and review readiness.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate(payload, base_dir=args.path.parent)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Ready for human review. Recipient accuracy, editorial quality, and permission to send are NOT verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
