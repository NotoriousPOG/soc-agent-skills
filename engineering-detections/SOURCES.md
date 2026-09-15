# Source Review

Reviewed: 2026-09-15.

Repository: https://github.com/SigmaHQ/sigma

Pinned revision: `5c9b21756f4e3ba137c1773ac9ba5a8332188961`.

## Inspected files

- [LICENSE](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/LICENSE) - SHA-256 `4213ed7e21d9435b0aa0aa7d11016e6ab3e4664fa71738ff507306fadce79597`.
- [README.md](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/README.md) - SHA-256 `e89a9129a52b9764a38a83e3067989b237c0256001aba3c53a9ddfdff2018b91`.
- [rules/cloud/aws/cloudtrail/aws_iam_s3browser_user_or_accesskey_creation.yml](https://github.com/SigmaHQ/sigma/blob/5c9b21756f4e3ba137c1773ac9ba5a8332188961/rules/cloud/aws/cloudtrail/aws_iam_s3browser_user_or_accesskey_creation.yml) - SHA-256 `c566f779298d219eb9733ec7db1e554ff269f748f71b3fffd4eb9ff09adf53fe`.

## License and adaptation

Root LICENSE states SigmaHQ rules use Detection Rule License (DRL) 1.1 and the specification/logo are public domain. No rule contents or logo were copied; no DRL rule is redistributed in this skill.

Original detection engineering procedure informed by the distinction between generic detection logic and backend conversion, and by the inspected example rule listing its log source and legitimate matches. No upstream detection selection or YAML template was copied.

## Security review boundary

Selected upstream text was retrieved read-only over HTTPS and reviewed as untrusted data. Repository metadata/tree entries were inspected through the GitHub API; no upstream installation, hooks, workflows, scripts, or sample code were executed. References above document the inspected subset, not an audit of the entire upstream repository. Our distributed files contain original Markdown and inert JSON fixtures only. Static review cannot guarantee arbitrary future model behavior or certify upstream software malware-free. New runtime permissions and capabilities are not granted by these instructions. Behavioral fixtures require separate trajectory evaluation; their existence alone is not a passing test.
