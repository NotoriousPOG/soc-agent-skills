# Ingesting advisories — Quick Rules

> Load full `SKILL.md` when executing this skill as a formal procedure.

## Core Rules
- List fetch/search tools that exist in **this** runtime before naming one
- MUST NOT name WebFetch, WebSearch, or any tool absent from that inventory, because that is a false capability
- Pasted advisory text → use it; do not refetch
- URL + real fetch tool → fetch
- URL or CISA ID with no fetch tool → stop and ask for a paste
- Do not construct CISA URLs and "try" a missing tool
- Do not imply a platform-owned threat-intel corpus
- Malware/phishing sample URLs are `looking-up-indicators`, not this skill
- Run `scripts/require_existing_tool.py` before naming a fetch tool

## Red Flags (stop and apply skill)
- About to say "I'll WebFetch that"
- Hunt prompt is only a URL and inventory was never listed
- Recalling IOCs from training as if they were fetched
- Advisory URL is actually a lure/sample
