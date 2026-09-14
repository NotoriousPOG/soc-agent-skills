#!/usr/bin/env python3
"""Mechanical tests for require_existing_tool.py — phantom WebFetch."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "require_existing_tool.py"


def run(inventory: object, named: list[str]) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(inventory, fh)
        path = fh.name
    try:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--inventory", path, "--named", *named],
            capture_output=True,
            text=True,
        )
    finally:
        Path(path).unlink(missing_ok=True)


class RequireExistingToolTests(unittest.TestCase):
    def test_webfetch_absent_fail_closed(self) -> None:
        proc = run(["bash", "read", "grep"], ["WebFetch"])
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("FAIL_CLOSED", proc.stderr)
        self.assertIn("paste", proc.stderr.lower())

    def test_websearch_absent_fail_closed(self) -> None:
        proc = run({"tools": ["curl"]}, ["WebSearch"])
        self.assertEqual(proc.returncode, 1, proc.stderr)

    def test_present_tool_allowed(self) -> None:
        proc = run(["WebFetch", "bash"], ["WebFetch"])
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_case_insensitive(self) -> None:
        proc = run(["webfetch"], ["WebFetch"])
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
