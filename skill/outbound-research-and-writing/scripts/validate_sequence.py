from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def validate(payload: dict) -> list[str]:
    errors: list[str] = []
    emails = payload.get("emails")
    if not isinstance(emails, list) or len(emails) != 6:
        return ["Sequence must contain exactly six emails."]

    for index, email in enumerate(emails, 1):
        if not isinstance(email, dict):
            errors.append(f"Email {index} must be an object.")
            continue
        body = str(email.get("body", "")).strip()
        subject = str(email.get("subject", "")).strip()
        if not body:
            errors.append(f"Email {index} has no body.")
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

    source_urls = payload.get("source_urls")
    if not isinstance(source_urls, list) or not any(str(url).startswith("http") for url in source_urls):
        errors.append("Sequence must include at least one source URL in the research record.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a six-touch outbound sequence JSON file.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Sequence passes structural QA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

