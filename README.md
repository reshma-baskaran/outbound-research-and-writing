# Outbound Research & Writing

![Outbound Research and Writing cover](assets/cover.svg)

A source-backed, draft-only starter kit for researching accounts, deciding what
is safe to say, and writing six-touch outbound sequences that do not repeat
themselves.

It packages a real operating method for local use. It is not a campaign sender,
enrichment product, or library of invented outreach examples.

## The problem

Personalization often fails in one of two ways: it is generic enough to fit every account, or it turns a weak public clue into an unsupported claim. Longer sequences compound the problem by repeating the same observation six times.

This repository captures the method I use to move from account research to review-ready copy while keeping facts, hypotheses, and unknowns separate.

## What is included

- A [quickstart](QUICKSTART.md), local configuration example, and workspace initializer.
- A reusable Codex skill in [`skill/outbound-research-and-writing`](skill/outbound-research-and-writing).
- An account-use-case research schema.
- A six-touch message architecture.
- Explicit research and launch boundaries.
- A deterministic sequence-structure validator.
- Blank research-map, sequence, and review-checklist templates.
- Field notes from dormant-lead, time-sensitive, and account-personalized campaign work.

## What a fork gives you

After setup, a fork gives you a local workspace for research maps, draft
sequences, reviews, and outputs. Add your own permitted account inputs and
source URLs, use the skill to draft, and validate the sequence before human
review.

It does not include recipient records, private campaign copy, sending-platform
exports, enrichment credentials, or launch state. A successful validation is a
structural gate, not permission to send.

## How it works

```text
account list
  → research map
  → keep / rewrite / suppress / needs research
  → confirmed fact / hypothesis / unknown
  → operating problem and consequence
  → six distinct touch roles
  → structural and editorial QA
  → human approval
```

## Use the skill

See [QUICKSTART.md](QUICKSTART.md) for the full setup and workspace initializer.

Copy the skill folder into your Codex skills directory, or point Codex at the local folder and ask:

```text
Use $outbound-research-and-writing to research these accounts and draft a grounded outbound sequence.
```

Validate a sequence:

```bash
python skill/outbound-research-and-writing/scripts/validate_sequence.py path/to/sequence.json
```

The JSON document must contain an `emails` array with exactly six objects and a `source_urls` array. Only the first email may have a subject.

## What this repository does not contain

It does not publish private recipient data, sending-platform exports, confidential campaign copy, or invented portfolio examples. The [field notes](docs/field-notes.md) explain what changed in the operating method across real campaign types without presenting private work as public evidence.

## Current status

The workflow is in active use as the writing and QA layer for account-personalized
outbound and is now packaged as a local starter kit. Uploading, lead
verification, enrichment spend, and campaign launch remain explicit human
decisions.

## Author

Built by **Reshma Baskaran**, a GTM and growth marketer building practical research, outbound, and knowledge systems.
