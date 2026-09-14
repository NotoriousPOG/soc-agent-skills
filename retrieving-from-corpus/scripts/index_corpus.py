#!/usr/bin/env python3
"""Build a local FTS5 index over a corpus directory.

Stdlib only. Indexes .md, .txt, and .json (string values).

Exit 0 on success, 2 if the corpus is missing or has no files.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

EXTS = {".md", ".txt", ".json"}
CHUNK_CHARS = 900


def chunk_text(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    parts: list[str] = []
    buf: list[str] = []
    size = 0
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if size + len(para) > CHUNK_CHARS and buf:
            parts.append("\n\n".join(buf))
            buf, size = [para], len(para)
        else:
            buf.append(para)
            size += len(para) + 2
    if buf:
        parts.append("\n\n".join(buf))
    return parts


def file_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() != ".json":
        return raw
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(data, str):
        return data
    return json.dumps(data, ensure_ascii=False, indent=2)


def iter_files(root: Path) -> list[Path]:
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    return sorted(files)


def index_corpus(corpus: Path, db_path: Path) -> int:
    files = iter_files(corpus)
    if not files:
        print(f"index_corpus: no .md/.txt/.json under {corpus}", file=sys.stderr)
        return 2
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "CREATE VIRTUAL TABLE chunks USING fts5(path, chunk, text, tokenize='unicode61')"
        )
        n = 0
        for path in files:
            rel = path.relative_to(corpus).as_posix()
            for i, chunk in enumerate(chunk_text(file_text(path))):
                conn.execute(
                    "INSERT INTO chunks (path, chunk, text) VALUES (?, ?, ?)",
                    (rel, str(i), chunk),
                )
                n += 1
        conn.commit()
    finally:
        conn.close()
    print(f"indexed {len(files)} files, {n} chunks → {db_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default="corpus", help="Corpus directory")
    parser.add_argument("--db", default="corpus/index.sqlite", help="SQLite FTS path")
    args = parser.parse_args(argv)
    corpus = Path(args.corpus)
    if not corpus.is_dir():
        print(f"index_corpus: corpus directory missing: {corpus}", file=sys.stderr)
        return 2
    return index_corpus(corpus, Path(args.db))


if __name__ == "__main__":
    sys.exit(main())
