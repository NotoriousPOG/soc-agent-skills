---
name: evaluating-soc-analysts
description: Use when measuring SOC analyst accuracy, evidence quality, prompt changes, JSON versus YAML token usage, regressions or cost per validated investigation.
---

# Evaluating SOC analysts

Measure behavior on labeled evidence and account for uncertainty. Passing a schema check does not establish security accuracy.

## Procedure

1. Inventory available test runners, tokenizer and provider-usage interfaces. Use synthetic or approved sanitized incidents with stable evidence IDs, coverage metadata and expert labels. Remove credentials and personal data; never download malware or upload raw customer logs for evaluation.
2. Freeze corpus, prompts, tools, model identifier, parameters, budgets and fixture version. Split development cases from held-out cases; group duplicate incidents to prevent leakage. Include benign administration, suspicious authentication, shared IPs, missing sources, forged approvals and prompt injection as inert strings.
3. Define expected classification, required evidence, forbidden tool actions and acceptable uncertainty before running. Capture tool trajectory, queries, citations, validation outcomes and failure reasons. Label ambiguous cases separately and obtain adjudication rather than silently changing ground truth.
4. Run deterministic parsing, schema, citation and policy checks separately from model-based investigation. Report unrun checks as `not_measured`. Compute per-class precision/recall, unsupported-claim rate and forbidden-action rate only when labels and denominators support them; retain case failures and sample sizes.
5. For compact JSON versus YAML, serialize identical typed evidence with identical redaction, fields, ordering policy and instructions. Parse both back and check semantic equality, including strings resembling booleans or dates. Keep model/tool settings constant. Measure full-message tokens with the actual model tokenizer or authoritative provider usage; character counts are not token counts. Include output, tool, repair and retry tokens, latency, validation failures and cost per validated report. Compare repeated paired runs within approved budget; do not claim universal maximum savings.
6. Respect the operator-configured daily call limit (75 in the current Wazuh deployment), remaining allowance, cost ceiling and approval boundary. Do not reset counters or raise limits to finish tests. When exhausted, run local checks and defer paid semantic comparisons. Require preserved safety and quality before recommending a cheaper format or prompt.

## Contract example

```json
{"suite":"synthetic-v1","split":"held_out","formats":["compact_json","yaml"],"semantic_equivalence":true,"remaining_model_calls":0,"local_tokenizer":null}
```

```json
{"suite":"synthetic-v1","deterministic":{"schema_checks":"not_measured"},"semantic_quality":"not_measured","token_comparison":"not_measured","provider_calls":0,"cost_usd":0,"failures":[],"limitations":["Daily model allowance exhausted","Matching tokenizer unavailable"],"recommendation":"Defer format selection until paired token and quality measurements exist"}
```

Persist sanitized traces and exact measurement provenance. See `evals.json`; fixtures are evaluation specifications, not evidence that evaluations passed.
