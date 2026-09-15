# Source Review

Reviewed: 2026-09-15.

Repository: https://github.com/aws-samples/aws-incident-response-playbooks

Pinned revision: `699c7c7c30f4add23531a3afd1f1803ab61d5f11`.

## Inspected files

- [LICENSE](https://github.com/aws-samples/aws-incident-response-playbooks/blob/699c7c7c30f4add23531a3afd1f1803ab61d5f11/LICENSE) - SHA-256 `a10cf1f6e78998b710fe868bda5b5f19120a7f36de10f06899356edc1ec0cd07`.
- [README.md](https://github.com/aws-samples/aws-incident-response-playbooks/blob/699c7c7c30f4add23531a3afd1f1803ab61d5f11/README.md) - SHA-256 `4799e31429399a02dccf8be93299541148d913997b31f98635a755174341cc79`.
- [ai-playbooks/scenarios/ai-irp-credential-compromise.md](https://github.com/aws-samples/aws-incident-response-playbooks/blob/699c7c7c30f4add23531a3afd1f1803ab61d5f11/ai-playbooks/scenarios/ai-irp-credential-compromise.md) - SHA-256 `709dd06921cd2b30d787c96071d1c654eb522167d8ad6ec57c29e8c3bf89569c`.

## License and adaptation

Conflicting upstream notices: root LICENSE is MIT-0 and GitHub identifies MIT-0; README License Summary states documentation is CC-BY-SA-4.0 and sample code MIT-0. This review does not resolve that inconsistency. No upstream text or code was copied.

Original investigation checklist informed by credential-compromise scoping concepts. Upstream command examples, containment steps, blanket urgency assumptions, and regulatory claims were not imported. Our version specifically handles uncertain rotations, SSO MFA interpretation, and Wazuh collector/target separation.

## Security review boundary

Selected upstream text was retrieved read-only over HTTPS and reviewed as untrusted data. Repository metadata/tree entries were inspected through the GitHub API; no upstream installation, hooks, workflows, scripts, or sample code were executed. References above document the inspected subset, not an audit of the entire upstream repository. Our distributed files contain original Markdown and inert JSON fixtures only. Static review cannot guarantee arbitrary future model behavior or certify upstream software malware-free. New runtime permissions and capabilities are not granted by these instructions. Behavioral fixtures require separate trajectory evaluation; their existence alone is not a passing test.
