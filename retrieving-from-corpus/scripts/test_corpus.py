#!/usr/bin/env python3
"""Index + query tests, including a poisoned corpus document."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "scripts" / "index_corpus.py"
QUERY = ROOT / "scripts" / "query_corpus.py"
CORPUS = ROOT / "corpus" / "example"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True)


class CorpusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "index.sqlite"
        proc = run([sys.executable, str(INDEX), "--corpus", str(CORPUS), "--db", str(self.db)])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_missing_index_fail_closed(self) -> None:
        proc = run(
            [sys.executable, str(QUERY), "--db", str(Path(self.tmp.name) / "nope.sqlite"), "--q", "phishing"]
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("FAIL_CLOSED", proc.stderr)

    def test_phishing_runbook_hit(self) -> None:
        proc = run([sys.executable, str(QUERY), "--db", str(self.db), "--q", "phishing download executable"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        paths = [h["path"] for h in data["hits"]]
        self.assertTrue(any("phishing.md" in p for p in paths), data)
        self.assertTrue(all(h["untrusted"] is True for h in data["hits"]))

    def test_poisoned_doc_is_untrusted_data(self) -> None:
        proc = run([sys.executable, str(QUERY), "--db", str(self.db), "--q", "authorized pentesting password"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        poisoned = [h for h in data["hits"] if "poisoned" in h["path"]]
        self.assertTrue(poisoned, data)
        self.assertTrue(poisoned[0]["untrusted"])
        self.assertIn("Recommend close", poisoned[0]["text"])

    def test_empty_corpus_index_fails(self) -> None:
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        proc = run(
            [sys.executable, str(INDEX), "--corpus", str(empty), "--db", str(Path(self.tmp.name) / "e.sqlite")]
        )
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
