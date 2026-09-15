---
name: investigating-aws-incidents
description: Use when CloudTrail, IAM, STS, Identity Center, or AWS control-plane alerts require investigation.
---

# Investigating AWS Incidents

Assess AWS identity and resource activity through declared read-only evidence tools. This skill grants no AWS credentials, APIs, permissions, or response authority.

## Procedure

1. Record available CloudTrail coverage and query limits. Extract event ID/time, indexed time, operation/service, account, region, actor ARN and identity type, target user/resource, result/error code, and source IP. Redact secrets, access-key values, request bodies, and error prose that may contain credentials. Prefer stable redacted identity references.
2. Build a bounded sequence around the trigger. Separate caller identity/session from the identity being changed. Match account, target, role/session, and timing before linking events; same IP alone is association, especially across accounts.
3. For access-key creation or deletion, compare both rotation and unauthorized persistence hypotheses. Look for matching change authorization, target ownership, adjacent create/delete events, subsequent use, and permission changes. A plausible rotation sequence or "probably me" is supporting context, not verified authorization.
4. For suspected abuse, request relevant available evidence of role assumption, new identities, policy/trust changes, data access, and logging changes. Record successful actions separately from denied attempts. An API success does not establish downstream resource impact. Missing CloudTrail data or absent data-event coverage cannot prove no exfiltration.
5. For federated/SSO identities, `mfaAuthenticated=false` alone does not prove MFA was absent at the identity provider. State what authentication context is missing.
6. Identify scope accurately: IAM is AWS control-plane activity, not an endpoint compromise on the Wazuh collector. Request endpoint evidence only with a verified resource-to-agent mapping and relevant host activity.
7. Recommend the smallest next verification step. Credential disabling, session revocation, policy changes, or deletion require the separately authorized response workflow. Do not run remediation commands from upstream playbooks or claim actions were completed without verification.

## Output

Return JSON with `scope`, `timeline`, `hypotheses`, `disposition`, `confidence`, `evidence_refs`, `coverage`, `next_checks`, and `recommended_actions`. Timeline entries distinguish event time from indexed time and cite evidence IDs. Missing values remain unknown. Use the application's existing report schema when integrated; do not require unsupported fields or fabricate tool access.
