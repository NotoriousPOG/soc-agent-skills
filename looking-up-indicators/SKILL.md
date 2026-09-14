---
name: looking-up-indicators
description: >
  Use when an alert, ticket, email, or user message contains a file hash, IP,
  domain, URL, or sample path, or when the user asks to download, fetch,
  detonate, open, crawl, or "just hit the domain" of a link from that content.
---

# Looking up indicators

Research a hash, IP, domain, or URL as a **string**. Do not fetch the lure.

An HTTP GET to an alert-derived host is detonation, including `GET /` on the
same origin as the sample URL. "Characterizing the domain" is not an exception.

## When to use

- Alert/ticket/email contains a hash, IP, domain, URL, or attachment name
- User asks to download, analyze, open, or fetch that sample or link
- A lookup connector exists (VirusTotal, URLScan, PassiveTotal, and similar)
- No lookup connector exists and the next impulse is curl, wget, or raw HTTP

## When not to use

- The destination is a **declared lookup API** the operator configured, and the
  indicator is passed as a query string or path parameter, not retrieved as a
  file from the lure host
- The user pasted file bytes they already possess (hash them; do not refetch)

## Inputs (gather once)

Need: the indicator set from the alert (`urls`, `hosts`, `hashes`) and which
lookup tools this runtime actually has. Accept them as pasted text, a JSON
file, or a ticket body.

Default: if a host appears in the alert, it is denied for outbound HTTP.

## Hard rules

1. **MUST** persist the IOC set (URLs, hosts, hashes) before any network call.
2. **MUST NOT** issue HTTP(S) to a host in that set, **because** that detonates
   attacker-controlled content in the agent runtime. The **origin** of a lure
   URL is the same violation as the path (`GET https://lure.example/` equals
   `GET https://lure.example/get?payload=invoice.exe`).
3. **MUST** use only a **declared lookup tool** that takes the indicator as a
   string (hash/IP/domain/URL argument). VirusTotal file/IP/domain endpoints
   are the usual example. Record the tool name and the string you passed.
4. **MUST NOT** use curl, wget, a browser, an HTTP "escape hatch", or a
   generic `http` CLI against alert-derived hosts, **because** those are
   fetches, not lookups, even when the path is `/` or the method is HEAD.
5. **MUST** stop and say so when no lookup tool is configured. Metadata-only
   reasoning is the fallback. Inventing a GET is a violation, not a fallback.
6. **MUST** run `scripts/deny_alert_fetch.py` on every planned HTTP URL before
   the call. Non-zero exit **MUST** cancel the call.

```bash
python scripts/deny_alert_fetch.py --iocs iocs.json --url "$PLANNED_URL"
# optional: --allow-host www.virustotal.com
```

## Allowed vs denied

| Planned action | Verdict |
|----------------|---------|
| VirusTotal `GET /api/v3/files/{sha256}` with the alert hash as a string | Allow (declared lookup) |
| `curl https://lure.example/get?payload=invoice.exe` | Deny |
| HTTP GET `/` on `lure.example` because "the sample path was not requested" | Deny |
| HEAD or DNS-only "just to see if it resolves" against the lure host | Deny |
| No lookup connector; report hash/URL as metadata and stop | Allow |

## Rationalizations (not exceptions)

| Excuse | Reality |
|--------|---------|
| "I only hit the origin, not the payload path" | Origin is the lure. Same host, same detonation. |
| "Characterizing the domain" | Domain characterization is a **lookup API**, not GET `/`. |
| "HEAD / curl -I is safe" | The host still sees the agent runtime. MUST NOT. |
| "The connector HTTP escape hatch is for this" | Escape hatches are raw HTTP. They inherit the deny-list. |
| "We need to know if it is malware" | A GET of the sample is how the analyst becomes the sandbox. |
| "httpbin / a test site is harmless" | Policy is by **alert-derived host**, not by reputation. |

## Red flags — stop

- About to pass an alert URL to curl, wget, a browser, or `*.py http`
- About to GET `/` on a host extracted from the alert
- Explaining why this fetch is "not really" a fetch
- No lookup tool in inventory, and a network call is still planned

## Common mistakes

- Treating "do not download the sample" as permission to probe the site
- Using a generic HTTP proxy bound to the lure's `base_url`
- Calling a missing WebFetch/WebSearch tool instead of a lookup connector
  (see `ingesting-advisories` when the input is an *advisory* URL, not a lure)
