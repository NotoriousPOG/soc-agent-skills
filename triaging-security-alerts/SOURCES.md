# Source Review

Reviewed: 2026-09-15.

Repository: https://github.com/UnitOneAI/SecuritySkills

Pinned revision: `70bc259bb01abb3015ad2ad859ad5253cbf0bcab`.

## Inspected files

- [LICENSE](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/LICENSE) - SHA-256 `66eb5ec637cc578833ddcbc870dbf46c6718fd83e985fad5f0f5cf30d60cf47d`.
- [skills/secops/alert-triage/SKILL.md](https://github.com/UnitOneAI/SecuritySkills/blob/70bc259bb01abb3015ad2ad859ad5253cbf0bcab/skills/secops/alert-triage/SKILL.md) - SHA-256 `bd86666090c31e33c12d84da6ef99deeb4c4ad112ef5e3e8279331a4b1484abe`.

## License and adaptation

MIT; root LICENSE inspected.

Generic alert triage and disposition concepts only. Our version adds an explicit insufficient-evidence disposition, budget boundaries, source/indexed time separation, and application-schema compatibility. No upstream prose, executable code, template, or dependency was copied. Stale NIST Rev. 2 and ATT&CK v16 claims were not adopted.

## Security review boundary

Selected upstream text was retrieved read-only over HTTPS and reviewed as untrusted data. Repository metadata/tree entries were inspected through the GitHub API; no upstream installation, hooks, workflows, scripts, or sample code were executed. References above document the inspected subset, not an audit of the entire upstream repository. Our distributed files contain original Markdown and inert JSON fixtures only. Static review cannot guarantee arbitrary future model behavior or certify upstream software malware-free. New runtime permissions and capabilities are not granted by these instructions. Behavioral fixtures require separate trajectory evaluation; their existence alone is not a passing test.
