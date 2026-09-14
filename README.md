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

Each skill ships a small stdlib Python gate:

- `looking-up-indicators/scripts/deny_alert_fetch.py`
- `ingesting-advisories/scripts/require_existing_tool.py`
- `retrieving-from-corpus/scripts/query_corpus.py`
- `routing-alert-notifications/scripts/notify.py`

Trajectory fixtures (not an LLM judge) live in each skill's `evals.json`.

## Install

Each folder is a self-contained skill (`SKILL.md` + `RULES.md` + `scripts/`).
Symlink or copy into the skills directory your agent reads.

```bash
git clone https://github.com/NotoriousPOG/soc-agent-skills.git
cd soc-agent-skills

# Claude Code
mkdir -p ~/.claude/skills
for s in looking-up-indicators ingesting-advisories retrieving-from-corpus routing-alert-notifications; do
  ln -s "$(pwd)/$s" ~/.claude/skills/$s
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

These skills do not replace an investigation methodology (intake → evidence →
gap analysis → schema-checked report). They sit next to it so the
methodology cannot start by detonating a lure, pretending to browse, obeying
a poisoned wiki, or POSTing secrets to a webhook the ticket invented.
