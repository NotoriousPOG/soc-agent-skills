# Investigating AWS Incidents - Quick Rules

Load full SKILL.md when executing this skill as a formal procedure.

- Read-only by default; no new AWS permissions or tools.
- Separate caller, target identity, account, session, and collector.
- Record source event time and indexed time separately.
- Compare rotation and abuse; probable authorization is not verified.
- MFA=false on SSO records alone does not establish absent IdP MFA.
- Separate denied attempts, successful API calls, and observed impact.
- Do not treat IAM activity as a collector endpoint compromise.
- Redact credential values and sensitive raw payloads.
- Use JSON evidence references and explicit coverage gaps.
- Leave mutations to separately authorized response workflows.
