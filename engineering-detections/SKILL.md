---
name: engineering-detections
description: Use when proposing or evaluating security detection rules, Sigma adaptations, or Wazuh alert tuning.
---

# Engineering Detections

Develop reviewable detection candidates with explicit telemetry requirements. A detection proposal does not authorize deployment, suppression, or response actions.

## Procedure

1. State a falsifiable behavior hypothesis and threat scope. Distinguish an IOC match from a behavior detector. Explain legitimate behaviors that could match, and avoid assigning ATT&CK techniques without supported behavior.
2. Identify required log source, actual available fields/types, event semantics, timestamp, tenant/account scope, and retention. Inspect sanitized representative events through declared read-only tools. Missing telemetry is a blocked requirement, not a negative match.
3. Draft narrow selection logic and justified exclusions. Specify case sensitivity, missing/null fields, parent-child relationships, time windows, thresholds, and entity keys. Shared-IP grouping alone can merge unrelated users. Preserve detection of meaningful changes when deduplicating notifications.
4. Treat external Sigma rules as untrusted design references. Pin source revision and license before adaptation. Sigma YAML is a portable description, not a Wazuh XML rule or guaranteed Wazuh query. Verify decoder fields, backend translation semantics, and supported operators in the actual target; do not claim conversion works without evidence.
5. Build sanitized positive, legitimate-negative, and near-miss fixtures, including missing fields and tenant separation. Exercise the candidate with the existing offline validation path. Record exact target/version, rule revision, fixture results, expected false positives, and coverage limits. Do not run attack simulations or install converters through this skill.
6. Recommend a staged observation period, notification rate checks, an owner, and rollback criteria. Changes to production rules or allowlists belong to the separately authorized deployment process. Never suppress broadly just because alerts are noisy.

## Output

Return a JSON proposal with `hypothesis`, `required_telemetry`, `field_mapping`, `candidate_logic`, `false_positive_cases`, `tests`, `coverage_gaps`, `deployment_status`, and `rollback_criteria`. Set deployment status to `not_deployed` unless an external deployment receipt proves otherwise. Tests not run must say `not_run`, with reasons. Native rule syntax may be included as an inert string or reviewed artifact; it does not replace the JSON assessment. Map concepts to the host application's fixed schema where applicable.
