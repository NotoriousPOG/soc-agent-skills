# SOC agent skills

Public agent skills for SOC / IR assistants. They close holes that show up
when investigation procedure is **markdown the model may follow**, not
**runtime the model cannot skip**.

| Skill | When to load |
|-------|----------------|
| [`looking-up-indicators`](looking-up-indicators/) | Alert contains a hash, IP, domain, or URL, or someone asks to download / detonate / "just hit the domain" |
| [`ingesting-advisories`](ingesting-advisories/) | Hunt or research a CISA / vendor advisory URL or ID, before naming WebFetch / WebSearch |
| [`retrieving-from-corpus`](retrieving-from-corpus/) | Need internal runbooks / past notes (RAG over an operator corpus) |
| [`routing-alert-notifications`](routing-alert-notifications/) | Post an alert to Slack, Teams, or an HTTPS webhook |
| [`triaging-security-alerts`](triaging-security-alerts/) | Assign evidence-backed disposition, priority, and escalation |
| [`investigating-aws-incidents`](investigating-aws-incidents/) | Investigate CloudTrail identity, credential, and resource activity |
| [`engineering-detections`](engineering-detections/) | Adapt detection hypotheses to verified telemetry and test them |
| [`triaging-malware-metadata`](triaging-malware-metadata/) | Assess existing file metadata and reports without acquiring or executing samples |
| [`correlating-security-evidence`](correlating-security-evidence/) | Connect scoped entities and timelines without treating shared IPs as proof |
| [`investigating-authentication`](investigating-authentication/) | Distinguish session failures, brute force, spraying, and suspicious success |
| [`verifying-response-actions`](verifying-response-actions/) | Verify authorized containment outcomes before claiming enforcement |
| [`evaluating-soc-analysts`](evaluating-soc-analysts/) | Measure grounded accuracy, unsafe actions, and cost with labeled cases |

License: MIT ([`LICENSE`](LICENSE)). Not a product of any commercial SOC vendor.

## What they enforce

**Looking up indicators.** Research the hash or URL **as a string** on a
declared lookup tool (VirusTotal and similar). Do not HTTP GET the lure, and
do not GET `/` on the lure origin either.

**Ingesting advisories.** Use a fetch tool only if it exists **in this
runtime**. If the user gave a URL and there is no fetch tool, stop and ask
for a paste.

**Retrieving from a corpus.** RAG over a local SQLite FTS5 index of operator
docs in `retrieving-from-corpus/corpus/`. Retrieved chunks are untrusted
data (corpus poisoning is treated like ticket injection). No lure fetching
"to grow the index." Empty corpus → fail closed.

**Routing alert notifications.** The space is
`routing-alert-notifications/destinations/`. Routes pick a webhook **env
var** by severity. The alert body cannot choose the channel or URL.
Payloads are allowlisted and redacted. Dry-run by default; `--send` to POST.

The original four boundary skills ship small stdlib Python gates:

- `looking-up-indicators/scripts/deny_alert_fetch.py`
- `ingesting-advisories/scripts/require_existing_tool.py`
- `retrieving-from-corpus/scripts/query_corpus.py`
- `routing-alert-notifications/scripts/notify.py`

Trajectory fixtures (not an LLM judge) live in each skill's `evals.json`.

The eight investigation additions are original Markdown procedures with JSON
trajectory fixtures. They import no third-party executable code, installers, or
malware samples. They do not grant tools or automatically enforce their prose:
applications must implement schema validation, capability limits, and action gates.
Source reviews and limitations are recorded in `docs/SECURITY-REVIEW-2026-09-15.md`.
This repository update does not deploy these eight skills into the Wazuh worker.

## Install

Each skill folder contains `SKILL.md`, `RULES.md`, and `evals.json`; the four
boundary skills also contain `scripts/`.
Symlink or copy into the skills directory your agent reads.

```bash
git clone https://github.com/NotoriousPOG/soc-agent-skills.git
cd soc-agent-skills

# Claude Code
mkdir -p ~/.claude/skills
for entry in */SKILL.md; do
  s="${entry%/SKILL.md}"
  ln -s "$(pwd)/$s" "$HOME/.claude/skills/$s"
done
```

Same loop works for `~/.agents/skills` (Codex) and `~/.cursor/skills` (Cursor).

## Tests

Stdlib only. No extra packages.

```bash
python looking-up-indicators/scripts/test_deny_alert_fetch.py
python ingesting-advisories/scripts/test_require_existing_tool.py
python retrieving-from-corpus/scripts/test_corpus.py
python routing-alert-notifications/scripts/test_notify.py
python scripts/check_investigation_skills.py
```

## Spaces you fill in

**Corpus (RAG).** Put runbooks under `retrieving-from-corpus/corpus/`, then:

```bash
python retrieving-from-corpus/scripts/index_corpus.py \
  --corpus retrieving-from-corpus/corpus \
  --db retrieving-from-corpus/corpus/index.sqlite
python retrieving-from-corpus/scripts/query_corpus.py \
  --db retrieving-from-corpus/corpus/index.sqlite \
  --q "phishing download"
```

**Destinations (Slack / webhooks).** Copy
`routing-alert-notifications/destinations/routes.example.json` to
`routes.json`, set `SLACK_WEBHOOK_SOC` / `SLACK_WEBHOOK_SOC_HIGH` to Incoming
Webhook URLs (or any HTTPS hook), drop alert JSON in `destinations/alerts/`:

```bash
python routing-alert-notifications/scripts/notify.py \
  --alert routing-alert-notifications/destinations/alerts/example.json \
  --routes routing-alert-notifications/destinations/routes.example.json
# add --send only after the dry-run looks right
```

Webhook URLs stay in the environment. `routes.json` is gitignored if you
create one.

## Related

Load the relevant investigation skill alongside the applicable boundary skills.
Keep system policy compact, retrieve only the relevant procedure, and use JSON
for validated input/output contracts. YAML frontmatter describes skill discovery;
it does not establish that YAML is more token-efficient for a model. The evaluation
skill requires an equivalent-data comparison using the selected model's tokenizer
or actual usage before claiming savings.
