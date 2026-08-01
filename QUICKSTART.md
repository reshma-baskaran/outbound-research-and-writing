# Quickstart

Outbound Research & Writing is a draft-only starter kit for moving from
account research to grounded outbound copy. It gives you the research map,
sequence structure, skill instructions, and QA boundary; it does not send,
upload, enrich, or activate a campaign.

## 1. Clone the starter kit

```bash
git clone https://github.com/reshma-baskaran/outbound-research-and-writing.git
cd outbound-research-and-writing
```

## 2. Create a local workspace

Copy the configuration example and change `workspace_path` to a location
outside this public repository:

```bash
cp outbound-research-and-writing.config.example.json outbound-research-and-writing.config.json
python3 scripts/init_workspace.py --config outbound-research-and-writing.config.json
```

The local configuration file is ignored by Git. The initializer creates blank
research, sequence, review, output, and template folders without overwriting
existing files unless `--overwrite` is explicitly supplied.

## 3. Use the research map

Open the copied `templates/research-map.md` and complete it from sources you
are allowed to use. Keep confirmed facts, hypotheses, and unknowns separate.
Preserve the source URL and access date for each account-specific claim.

## 4. Draft and validate a sequence

Use the copied `templates/sequence.json` as the structural starting point. Add
your own six emails and source URLs, then run:

```bash
python3 skill/outbound-research-and-writing/scripts/validate_sequence.py \
  /path/to/your/sequence.json
```

The validator requires exactly six emails, allows a subject only on Email 1,
rejects research narration and long bodies, and requires at least one source
URL. It does not judge strategy or replace human review.

## 5. Use the skill

Copy `skill/outbound-research-and-writing` into your Codex skills directory, or
point Codex at the local folder and ask it to use the skill for an account
research map or grounded sequence draft.

## What this does not do

This public starter kit does not contain recipient records, private campaign
copy, sending-platform exports, enrichment credentials, or launch state. Keep
campaigns paused or in draft until a human reviews the evidence, copy, sender,
audience, and send controls.
