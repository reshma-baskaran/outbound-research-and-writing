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

## 3. Check campaign readiness

Complete the copied `templates/campaign-input.json`, then run:

```bash
python3 skill/outbound-research-and-writing/scripts/check_readiness.py \
  /path/to/campaign-input.json
```

The minimum bundle is sender identity, sender company, offer, target account
and domain, target persona, campaign objective, CTA, and at least one approved
proof point. A `needs_input` result is a hard stop: ask only for the listed
fields and do not create a sequence.

Create a resumable account case:

```bash
python3 scripts/run_case.py \
  --input /path/to/campaign-input.json \
  --out /path/outside/the/repository/cases
```

Incomplete input creates only `readiness.json`. Complete input creates a blank
account-specific research map and advances to `needs_research`; it still does
not create a sequence.

## 4. Use the research map

Open the copied `templates/research-map.md` and complete it from sources you
are allowed to use. Keep confirmed facts, hypotheses, and unknowns separate.
Preserve the source URL and access date for each account-specific claim.

## 5. Draft and validate a sequence

Use the copied `templates/sequence.json` as the structural starting point. Add
your own six emails and source URLs, then run:

```bash
python3 skill/outbound-research-and-writing/scripts/validate_sequence.py \
  /path/to/your/sequence.json
```

The validator requires a `ready_for_review` state, complete campaign input, an
existing research map, structured claims with HTTPS sources, six distinct
touch roles, CTAs, and signoffs. It rejects placeholders, duplicate bodies,
unknown claim IDs, research narration, and long bodies. Success means ready
for human review only; it does not verify recipient data or authorize sending.

The one allowed review-stage recipient token is `Hi [first name],` at the
start of every email. Each `signoff` must exactly match the campaign's
`sender_identity`; the repository never supplies Reshma's name as a default.

## 6. Use the skill

Copy `skill/outbound-research-and-writing` into your Codex skills directory, or
point Codex at the local folder and ask it to use the skill for an account
research map or grounded sequence draft.

## What this does not do

This public starter kit does not contain recipient records, private campaign
copy, sending-platform exports, enrichment credentials, or launch state. Keep
campaigns paused or in draft until a human reviews the evidence, copy, sender,
audience, and send controls.
