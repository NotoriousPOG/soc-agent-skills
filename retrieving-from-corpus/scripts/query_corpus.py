#!/usr/bin/env python3
"""Query a local FTS5 corpus index. Prints JSON hits; untrusted is always true.

Exit 0 with hits, 1 with zero hits, 2 on missing DB / usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path


def fts_query(raw: str) -> str:
    """Turn free text into an FTS5 MATCH string of quoted terms (AND)."""
    terms = re.findall(r"[A-Za-z0-9_./:-]+", raw)
    if not terms:
        return '""'
    return " AND ".join('"' + t.replace('"', "") + '"' for t in terms[:12])


def query(db_path: Path, q: str, k: int) -> list[dict]:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(path, chunk, text)")
        sql = (
            "SELECT path, chunk, text, bm25(chunks) AS score "
            "FROM chunks WHERE chunks MATCH ? ORDER BY score LIMIT ?"
        )
        rows = conn.execute(sql, (fts_query(q), k)).fetchall()
    finally:
        conn.close()
    hits = []
    for path, chunk, text, score in rows:
        hits.append(
            {
                "path": path,
                "chunk": int(chunk),
                "score": float(score) if score is not None else 0.0,
                "text": text,
                "untrusted": True,
            }
        )
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="corpus/index.sqlite")
    parser.add_argument("--q", required=True, help="Query string")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args(argv)
    db_path = Path(args.db)
    if not db_path.is_file():
        print(
            f"query_corpus: FAIL_CLOSED index missing: {db_path}. "
            "Index the operator corpus or say there is no retrieved answer.",
            file=sys.stderr,
        )
        return 2
    try:
        hits = query(db_path, args.q, max(1, args.k))
    except sqlite3.Error as exc:
        print(f"query_corpus: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"hits": hits}, ensure_ascii=False, indent=2))
    if not hits:
        print("query_corpus: zero hits — do not fill from memory", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
