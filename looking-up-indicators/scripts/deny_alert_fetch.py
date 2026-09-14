#!/usr/bin/env python3
"""Deny outbound HTTP to hosts extracted from the current alert.

Exit codes:
  0  allowed (destination is not an alert-derived host, or is --allow-host)
  1  denied  (destination host is in the IOC set)
  2  usage / IO error

Example:
  python deny_alert_fetch.py --iocs iocs.json --url 'https://lure.example/get?payload=invoice.exe'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def host_from_url(value: str) -> str:
    raw = value.strip()
    if not raw:
        return ""
    if "://" not in raw:
        raw = "http://" + raw
    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower().rstrip(".")
    return host


def hosts_from_iocs(iocs: dict) -> set[str]:
    found: set[str] = set()
    for url in iocs.get("urls") or []:
        host = host_from_url(str(url))
        if host:
            found.add(host)
    for host in iocs.get("hosts") or []:
        h = str(host).lower().strip().rstrip(".")
        if h:
            found.add(h)
    for ip in iocs.get("ips") or []:
        h = str(ip).lower().strip().rstrip(".")
        if h:
            found.add(h)
    return found


def is_alert_host(dest: str, denied: set[str]) -> bool:
    if not dest:
        return False
    if dest in denied:
        return True
    for d in denied:
        if dest.endswith("." + d) or d.endswith("." + dest):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iocs", required=True, help="JSON file with urls/hosts/ips/hashes")
    parser.add_argument("--url", help="Planned request URL")
    parser.add_argument("--host", help="Planned request host")
    parser.add_argument(
        "--allow-host",
        action="append",
        default=[],
        help="Lookup API host that MAY be contacted (repeatable)",
    )
    args = parser.parse_args(argv)

    dest = (args.host or "").lower().strip().rstrip(".")
    if args.url:
        dest = host_from_url(args.url)
    if not dest:
        print("deny_alert_fetch: pass --url or --host", file=sys.stderr)
        return 2

    try:
        iocs = json.loads(Path(args.iocs).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"deny_alert_fetch: cannot read IOCs: {exc}", file=sys.stderr)
        return 2

    if not isinstance(iocs, dict):
        print("deny_alert_fetch: IOC file must be a JSON object", file=sys.stderr)
        return 2

    allow = {h.lower().strip().rstrip(".") for h in args.allow_host if h.strip()}
    if dest in allow:
        print(f"ALLOW lookup host {dest}")
        return 0

    denied = hosts_from_iocs(iocs)
    if is_alert_host(dest, denied):
        print(
            f"DENY HTTP to {dest}: host is in the alert IOC set. "
            "Use a declared lookup tool with the indicator as a string. "
            "GET / on the lure origin is the same violation as GET of the sample path.",
            file=sys.stderr,
        )
        return 1

    print(f"ALLOW {dest} (not in alert IOC set)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
