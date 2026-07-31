---
name: outbound-research-and-writing
description: Research accounts, map evidence to a buyer's operating problem, write or review account-personalized outbound email sequences, and run pre-launch QA. Use for cold outbound, ABM sequences, dormant-lead reactivation, time-sensitive outreach, post-event follow-up, or any campaign where claims must remain source-backed and the sequence must avoid repetition.
---

# Outbound Research and Writing

Write like an operator who understands the buyer's day. Make every account claim traceable.

## Workflow

1. Inspect the account and contact list before drafting.
2. Build the account-use-case map in [references/research-map.md](references/research-map.md).
3. Classify every account as `keep`, `rewrite`, `suppress`, or `needs_research`.
4. Separate confirmed facts, hypotheses, and unknowns.
5. Map the strongest evidence to one operating problem and consequence.
6. Plan six distinct touches using [references/sequence-design.md](references/sequence-design.md).
7. Draft locally. Never upload, activate, or send without explicit approval.
8. Run `python scripts/validate_sequence.py <sequence.json>`.
9. Read the copy once as the recipient. Rewrite anything generic, repetitive, or self-conscious.

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

Use [references/quality-gate.md](references/quality-gate.md) before delivery.

