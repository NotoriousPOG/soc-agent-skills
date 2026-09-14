# SOC agent skills

Two public agent skills for SOC / IR assistants. They close holes that show up
when investigation procedure is **markdown the model may follow**, not
**runtime the model cannot skip**.

| Skill | When to load |
|-------|----------------|
| [`looking-up-indicators`](looking-up-indicators/) | Alert contains a hash, IP, domain, or URL, or someone asks to download / detonate / "just hit the domain" |
| [`ingesting-advisories`](ingesting-advisories/) | Hunt or research a CISA / vendor advisory URL or ID, before naming WebFetch / WebSearch |

License: MIT ([`LICENSE`](LICENSE)). Not a product of any commercial SOC vendor.

## What they enforce

**Looking up indicators.** Research the hash or URL **as a string** on a
declared lookup tool (VirusTotal and similar). Do not HTTP GET the lure, and
do not GET `/` on the lure origin either. "Characterizing the domain" is not
an exception. If no lookup tool is configured, stop.

**Ingesting advisories.** Use a fetch tool only if it exists **in this
runtime**. If the user gave a URL and there is no fetch tool, stop and ask
for a paste. Do not name WebFetch or WebSearch because another product has
them. Do not imply a platform-owned threat-intel corpus.

Each skill ships a small stdlib Python gate the agent is told to run before
the network call:

- `looking-up-indicators/scripts/deny_alert_fetch.py`
- `ingesting-advisories/scripts/require_existing_tool.py`

Trajectory fixtures (not an LLM judge) live in each skill's `evals.json`.

## Install

Each folder is a self-contained skill (`SKILL.md` + `RULES.md` + `scripts/`).
Symlink or copy into the skills directory your agent reads.

```bash
git clone https://github.com/NotoriousPOG/soc-agent-skills.git
cd soc-agent-skills

# Claude Code
mkdir -p ~/.claude/skills
ln -s "$(pwd)/looking-up-indicators" ~/.claude/skills/looking-up-indicators
ln -s "$(pwd)/ingesting-advisories" ~/.claude/skills/ingesting-advisories

# Codex
mkdir -p ~/.agents/skills
ln -s "$(pwd)/looking-up-indicators" ~/.agents/skills/looking-up-indicators
ln -s "$(pwd)/ingesting-advisories" ~/.agents/skills/ingesting-advisories

# Cursor
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/looking-up-indicators" ~/.cursor/skills/looking-up-indicators
ln -s "$(pwd)/ingesting-advisories" ~/.cursor/skills/ingesting-advisories
```

Grok / other SKILL.md loaders: point them at the same two folders.

## Tests

Stdlib only. No extra packages.

```bash
python looking-up-indicators/scripts/test_deny_alert_fetch.py
python ingesting-advisories/scripts/test_require_existing_tool.py
```

The lure-origin case (`GET https://httpbingo.org/` when the alert URL is
`http://httpbingo.org/get?payload=invoice.exe`) is an expected **deny**.

## Using the gates from a skill run

```bash
# After extracting IOCs from the alert into iocs.json
python looking-up-indicators/scripts/deny_alert_fetch.py \
  --iocs iocs.json \
  --url "$PLANNED_URL"
# exit 1 → do not send the request
# --allow-host www.virustotal.com  for a declared lookup API

# Before naming a fetch tool
python ingesting-advisories/scripts/require_existing_tool.py \
  --inventory tools.json \
  --named WebFetch
# exit 1 → ask for a paste; do not fetch
```

`iocs.json` shape:

```json
{
  "urls": ["http://httpbingo.org/get?payload=invoice.exe"],
  "hosts": ["laptop-finance-7"],
  "ips": [],
  "hashes": ["da39a3ee5e6b4b0d3255bfef95601890afd80709"]
}
```

`tools.json` shape: `["bash", "read"]` or `{"tools": ["bash", "read"]}`.

## Related

These skills do not replace an investigation methodology (intake → evidence →
gap analysis → schema-checked report). They sit in front of it so the
methodology cannot start by detonating the lure or by pretending to browse.
