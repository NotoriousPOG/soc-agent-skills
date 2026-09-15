# Investigation skill review

## Scope and method

The eight investigation packages are original procedures written for this repository.
Upstream sources were inspected as text through GitHub; no upstream installer,
script, dependency, binary, sample, or archive was installed or executed. Original
text is covered by this repository's MIT license. Per-skill SOURCES.md records
upstream file references and license observations for the four source-informed
procedures; it does not relicense upstream content.

Review covers the newly added packages and offline package checker. It is not
a certification of upstream repositories or a claim that any AI is immune to
prompt injection. A whole-repository malware scan was not performed. Static text
inspection and restricted artifact types reduce risk but cannot prove absence
of all malicious behavior in a future model or integration.

## Source decisions

- UnitOneAI SecuritySkills: use triage concepts, not copied instructions. Its
  inspected triage document references NIST Rev. 2; do not inherit stale framework
  versions, preset organizational SLAs, or automatic closure decisions.
- AWS incident response playbooks: original AWS procedure only. The inspected
  repository has different statements for documentation and code licensing;
  no upstream prose or code is vendored. Environment-specific response commands
  are outside the new skill's authority.
- SigmaHQ: detection content has Detection Rule License terms. No rules or
  conversion code are copied. A rule is a hypothesis until field mapping,
  telemetry, deployment and controlled validation are verified.
- Analyst AI Pack: sample parsing/execution workflows are excluded. The local
  skill consumes existing metadata and reports and identifies a separate sandbox
  handoff when necessary. It never downloads or detonates samples.

## Integration boundaries

Only Markdown and JSON are allowed inside the eight new packages. They contain
no scripts, hooks, executable tool grants, network clients, or credential readers.
The new root checker uses the Python standard library for local text/JSON checks;
it makes no network calls or subprocess calls. Source URLs are provenance, not
instructions to automatically fetch them during an investigation.

Untrusted alerts, corpus chunks, and tool results cannot choose notification
routes or authorize containment. Declared tool inventories and application policy
remain authoritative. Response verification reports observed states and supplies
no ban executor. No global installation or production deployment is part of this
change; OpenRouter quota and the existing Wazuh webhook are unchanged.

## Validation evidence

Before authoring, an isolated assistant received eight safety scenarios without
the new skills: ambiguous IAM rotation, repeated HTTP 401s, shared-IP correlation,
HTTP 202 ban acceptance, lure fetching, exhausted paid-call quota, timed-out
endpoint queries, and a Sigma rule without telemetry. All eight baseline answers
handled their safety boundary correctly. No safety failure or measured behavioral
improvement was demonstrated by that baseline. This is a coverage and consistency
addition, not evidence of improved live-model accuracy.

Final deterministic validation: all 19 existing Python regression tests passed
(5 indicator, 4 capability, 4 corpus, 6 notification). The notification test uses
a mocked sender; no live webhook was contacted. Package validation passed for
eight skills, 28 text artifacts, and 24 trajectory fixture definitions. Embedded
JSON examples parse. All 28 skill artifacts are ASCII, non-executable regular
files without symlinks. The check is also included in the existing CI workflow.

Static review found no malicious payload, credential-collection instruction,
executable hook, or unauthorized action escalation in the new local artifacts.
Adversarial instructions appear only as explicitly untrusted fixture content.
A separate assistant reviewed the four custom-analysis packages and the checker.
The primary assistant reviewed all eight procedures and their quick rules.
With-skill behavioral review results are recorded in the companion review.
Trajectory fixture counts are specifications, not counts of executed model tests.
No paid OpenRouter call or live Discord message is part of the review.
