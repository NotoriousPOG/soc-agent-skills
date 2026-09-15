"""Offline package checks, not a malware scanner or an LLM behavior evaluation."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "triaging-security-alerts", "investigating-aws-incidents",
    "engineering-detections", "triaging-malware-metadata",
    "correlating-security-evidence", "investigating-authentication",
    "verifying-response-actions", "evaluating-soc-analysts",
)


def check() -> tuple[int, int]:
    files = cases = 0
    for name in SKILLS:
        directory = ROOT / name
        assert directory.is_dir() and not directory.is_symlink(), name
        for required in ("SKILL.md", "RULES.md", "evals.json"):
            assert (directory / required).is_file(), (name, required)
        for path in directory.rglob("*"):
            assert not path.is_symlink(), f"symlink: {path}"
            if path.is_dir():
                continue
            assert path.suffix in {".md", ".json"}, f"unexpected artifact: {path}"
            assert not path.stat().st_mode & 0o111, f"executable artifact: {path}"
            assert path.stat().st_size < 65536, f"oversize artifact: {path}"
            content = path.read_text(encoding="utf-8")
            assert "\x00" not in content, f"binary content: {path}"
            assert not re.search(r"[\u202a-\u202e\u2066-\u2069]", content), path
            assert not re.search(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----", content), path
            assert not re.search(r"sk-or-v1-[a-f0-9]{32,}", content), path
            for example in re.findall(r"```json\n(.*?)\n```", content, re.S):
                json.loads(example)
            if path.suffix == ".json":
                json.loads(content)
            files += 1
        body = (directory / "SKILL.md").read_text()
        assert body.startswith("---\n"), name
        front, document = body[4:].split("\n---\n", 1)
        assert re.search(rf"^name: {re.escape(name)}$", front, re.M), name
        assert re.search(r"^description:", front, re.M), name
        assert set(re.findall(r"^([a-z-]+):", front, re.M)) == {"name", "description"}, name
        assert len(document.split()) <= 500, f"skill too long: {name}"
        assert len((directory / "RULES.md").read_text().split()) <= 300, name
        fixture = json.loads((directory / "evals.json").read_text())
        assert fixture["skill"] == name and fixture["scoring"] == "trajectory", name
        identifiers = set()
        assert len(fixture["fixtures"]) >= 3, name
        for item in fixture["fixtures"]:
            assert item["id"] not in identifiers, name
            identifiers.add(item["id"])
            assert item["prompt"] and item["expect"] and item["fail_if"], name
            cases += 1
    return files, cases


if __name__ == "__main__":
    file_count, case_count = check()
    print(f"PASS: {len(SKILLS)} skills, {file_count} text artifacts, {case_count} trajectory fixtures")
    print("Structural validation only; fixtures were not executed by this checker.")
