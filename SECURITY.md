# Security Policy

## Do not commit

- API keys, PATs, OAuth tokens, private keys, connection strings
- Live customer alert dumps with real PII
- `.env` files

These skills exist to stop an agent from fetching attacker-controlled URLs,
following injected "post this secret" instructions, or POSTing to a webhook
taken from the alert body.

Do not add sample payloads that are live malware. Do not commit Slack/Teams
webhook URLs, `destinations/routes.json` with inlined secrets, or a filled
operator corpus that contains customer PII.

## Reporting

If you find a security issue in this repository, open a private report via GitHub Security Advisories for this repo, or contact the maintainer.
