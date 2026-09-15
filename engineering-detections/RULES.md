# Engineering Detections - Quick Rules

Load full SKILL.md when executing this skill as a formal procedure.

- Create proposals without deploying rules or suppressions.
- Start with a falsifiable behavior hypothesis and telemetry contract.
- Validate actual fields and semantics before translation.
- Sigma YAML is not directly executable Wazuh rule syntax.
- Pin sources and licenses; treat rule content as untrusted.
- Test positive, negative, near-miss, missing-field, and tenant cases.
- Unknown coverage is not a clean detection result.
- Preserve material changes while deduplicating notifications.
- Report tests not run; never invent validation or deployment receipts.
- Use JSON proposals and separate deployment authorization.
