# Outbound Research & Writing

![Outbound Research and Writing cover](assets/cover.png)

A source-backed operating system for researching accounts, deciding what is safe to say, and writing six-touch outbound sequences that do not repeat themselves.

## The problem

Personalization often fails in one of two ways: it is generic enough to fit every account, or it turns a weak public clue into an unsupported claim. Longer sequences compound the problem by repeating the same observation six times.

This repository captures the method I use to move from account research to review-ready copy while keeping facts, hypotheses, and unknowns separate.

## What is included

- A reusable Codex skill in [`skill/outbound-research-and-writing`](skill/outbound-research-and-writing).
- An account-use-case research schema.
- A six-touch message architecture.
- Explicit research and launch boundaries.
- A deterministic sequence-structure validator.
- Field notes from dormant-lead, time-sensitive, and account-personalized campaign work.

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

The workflow is in active use as the writing and QA layer for account-personalized outbound. Uploading, lead verification, enrichment spend, and campaign launch remain explicit human decisions.

## Author

Built by **Reshma Baskaran**, a GTM and growth marketer building practical research, outbound, and knowledge systems.

