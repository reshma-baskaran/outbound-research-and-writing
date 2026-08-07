---
name: outbound-research-and-writing
description: Initialize a local draft-only workspace, research accounts, map evidence to a buyer's operating problem, write or review account-personalized outbound email sequences, and run pre-launch QA. Use for cold outbound, ABM sequences, dormant-lead reactivation, time-sensitive outreach, post-event follow-up, or any campaign where claims must remain source-backed and the sequence must avoid repetition.
---

# Outbound Research and Writing

Write like an operator who understands the buyer's day. Make every account claim traceable.

## Start a new workspace

For a new user or local installation:

1. Copy `outbound-research-and-writing.config.example.json` to a local
   `outbound-research-and-writing.config.json` and set `workspace_path` outside
   the public repository.
2. Run `python3 scripts/init_workspace.py --config outbound-research-and-writing.config.json`.
3. Complete `templates/campaign-input.json` and run
   `python3 skill/outbound-research-and-writing/scripts/check_readiness.py <campaign-input.json>`.
4. Stop when the result is `needs_input`. Ask only for the listed fields and do
   not create a sequence file.
5. Complete the copied `templates/research-map.md` from permitted sources.
6. Draft into a local sequence file and run the validator before review.

The initializer creates missing files but does not overwrite existing workspace
files unless `--overwrite` is explicitly supplied. Do not add fictional
campaigns, recipients, or results to make the workflow look complete.

## Workflow

1. Validate the campaign input before researching or drafting.
2. Stop on `needs_input`, `needs_research`, or `suppress`; never represent a
   blocked sequence as completed work.
3. Build the account-use-case map in [references/research-map.md](references/research-map.md).
4. Classify every account as `keep`, `rewrite`, `suppress`, or `needs_research`.
5. Separate confirmed facts, hypotheses, and unknowns.
6. Map each usable claim to a stable claim ID, source URL, access date, status,
   and scope.
7. Map the strongest evidence to one operating problem and consequence.
8. Plan six distinct touches using [references/sequence-design.md](references/sequence-design.md).
9. Draft locally. Never upload, activate, or send without explicit approval.
10. Set `readiness_status` to `ready_for_review` only after research and input
    gates pass, then run `python scripts/validate_sequence.py <sequence.json>`.
11. Treat validator success as readiness for human review only. It is never
    recipient verification, permission to send, or campaign launch approval.
12. Read the copy once as the recipient. Rewrite anything generic, repetitive, or self-conscious.

## Research rules

- Prefer first-party sources, filings, job posts, product/support pages, and direct customer evidence.
- Preserve the source URL and access date.
- Treat interpretation as interpretation.
- If a claim lacks a usable source, use market-level language or return the account to research.
- Suppress or hard-review defunct companies, domain mismatches, obvious off-ICP records, and material distress unless the strategy explicitly targets them.
- Never narrate the research process in the email.

## Writing rules

- Open with a concrete operating pressure, not an AI category statement.
- State the consequence in the buyer's language.
- Give each touch a different job.
- Put a subject on Email 1 only; follow-ups remain in the same thread.
- Keep the CTA small and easy to answer.
- Tie governance, auditability, and handoff to a specific workflow.
- Match the signoff to the actual sender.

## Boundaries

- Do not invent account facts, customers, outcomes, meetings, or product capabilities.
- Do not upload copy, verify leads, spend enrichment credits, or launch a campaign without explicit approval.
- Keep campaigns paused or in draft unless the user explicitly asks to launch.
- If the evidence is insufficient, return the missing research fields instead of completing the sequence.
- Never use placeholders, `[BLOCKED]` copy, or duplicated bodies to satisfy the
  six-email structure.
- Never create a sequence when the sender, offer, target persona, proof,
  campaign objective, or CTA is missing.

Use [references/quality-gate.md](references/quality-gate.md) before delivery.
