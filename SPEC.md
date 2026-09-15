# SOC investigation skills

Add eight original defensive investigation skills alongside the existing four
tool-boundary skills. Scope: triage, AWS, detection engineering, malware metadata,
correlation, authentication, response verification, and analyst evaluation.

Acceptance criteria:

- Each skill has a concise SKILL.md, RULES.md, and positive, adversarial, and
  missing-evidence or missing-capability trajectory fixtures.
- Source-informed skills record inspected upstream revisions, files, and licenses.
  Upstream code, installers, dependencies, and malware samples are not imported.
- Skills distinguish observed evidence, hypotheses, incomplete coverage, and
  verified actions. Skill text never grants tool access or remediation authority.
- Existing tests and the new package checks pass. Behavioral exercises and their
  limits are reported separately from deterministic checks.
- Token efficiency guidance preserves JSON contracts and requires measurement
  with the selected model before claiming JSON/YAML savings.

This phase adds repository skills. It does not change the deployed Wazuh worker,
install globally, send notifications, execute containment, or spend OpenRouter quota.

