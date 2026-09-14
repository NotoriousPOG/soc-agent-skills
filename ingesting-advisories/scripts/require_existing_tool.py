#!/usr/bin/env python3
"""Fail if a plan names a tool that is not in this runtime's inventory.

Exit codes:
  0  every --named tool is in the inventory (case-insensitive)
  1  at least one named tool is missing (fail closed: ask for a paste)
  2  usage / IO error

Inventory JSON is a list of tool names, or an object with a "tools" list.

Example:
  python require_existing_tool.py --inventory tools.json --named WebFetch WebSearch
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_inventory(path: str) -> set[str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        names = data.get("tools") or data.get("names") or []
    elif isinstance(data, list):
        names = data
    else:
        raise ValueError("inventory must be a list or an object with tools[]")
    return {str(n).strip().lower() for n in names if str(n).strip()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, help="JSON tool inventory")
    parser.add_argument("--named", nargs="+", required=True, help="Tools the plan wants to call")
    args = parser.parse_args(argv)

    try:
        inventory = load_inventory(args.inventory)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"require_existing_tool: cannot read inventory: {exc}", file=sys.stderr)
        return 2

    missing = [name for name in args.named if name.strip().lower() not in inventory]
    if missing:
        print(
            "FAIL_CLOSED: tool(s) not in this runtime: "
            + ", ".join(missing)
            + ". Do not name them. If the input is a URL, stop and ask the user "
            "to paste the advisory text. Do not construct a fetch.",
            file=sys.stderr,
        )
        return 1

    print("ALLOW named tools: " + ", ".join(args.named))
    return 0


if __name__ == "__main__":
    sys.exit(main())
