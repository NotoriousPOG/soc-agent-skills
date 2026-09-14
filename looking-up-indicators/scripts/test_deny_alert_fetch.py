#!/usr/bin/env python3
"""Mechanical tests for deny_alert_fetch.py — the lure-origin miss."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "deny_alert_fetch.py"


def run(iocs: dict, extra: list[str]) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(iocs, fh)
        path = fh.name
    try:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--iocs", path, *extra],
            capture_output=True,
            text=True,
        )
    finally:
        Path(path).unlink(missing_ok=True)


class DenyAlertFetchTests(unittest.TestCase):
    IOCS = {
        "urls": ["http://httpbingo.org/get?payload=invoice.exe"],
        "hosts": ["laptop-finance-7"],
        "hashes": ["da39a3ee5e6b4b0d3255bfef95601890afd80709"],
    }

    def test_sample_path_denied(self) -> None:
        proc = run(self.IOCS, ["--url", "http://httpbingo.org/get?payload=invoice.exe"])
        self.assertEqual(proc.returncode, 1, proc.stderr)

    def test_origin_root_denied(self) -> None:
        """The live miss: GET / on the lure origin, 'characterizing the domain'."""
        proc = run(self.IOCS, ["--url", "https://httpbingo.org/"])
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("IOC set", proc.stderr)

    def test_head_on_origin_denied(self) -> None:
        proc = run(self.IOCS, ["--host", "httpbingo.org"])
        self.assertEqual(proc.returncode, 1, proc.stderr)

    def test_declared_lookup_allowed(self) -> None:
        proc = run(
            self.IOCS,
            [
                "--url",
                "https://www.virustotal.com/api/v3/files/da39a3ee5e6b4b0d3255bfef95601890afd80709",
                "--allow-host",
                "www.virustotal.com",
            ],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_unrelated_host_allowed(self) -> None:
        proc = run(self.IOCS, ["--url", "https://api.github.com/rate_limit"])
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
