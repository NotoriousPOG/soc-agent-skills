# Looking up indicators — Quick Rules

> Load full `SKILL.md` when executing this skill as a formal procedure.

## Core Rules
- Persist URLs, hosts, and hashes from the alert before any network call
- MUST NOT HTTP(S) to an alert-derived host, because that detonates attacker content
- Fetching the lure origin (`GET /`) is the same violation as fetching the sample path
- Lookups take the indicator as a **string** on a declared lookup tool (e.g. VirusTotal)
- curl, wget, browsers, and HTTP escape hatches against lure hosts are fetches, not lookups
- HEAD, DNS "just to resolve", and "characterizing the domain" are not exceptions
- No lookup tool configured → stop; metadata only; do not invent a GET
- Run `scripts/deny_alert_fetch.py` on every planned URL; non-zero exit cancels the call

## Red Flags (stop and apply skill)
- User said "download / detonate / open / just hit the domain"
- Planned curl/wget/`http` to a host that appears in the alert
- Rationalizing `GET /` as "not the payload"
- About to use an HTTP escape hatch bound to the lure site
