#!/usr/bin/env python3
"""Route a bounded alert payload to an operator-configured HTTPS webhook.

Default is dry-run (print payload, no POST). Pass --send to deliver.

Exit 0 on dry-run/success, 1 if the send is denied, 2 on usage/config error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_FIELDS = (
    "title",
    "severity",
    "host",
    "user",
    "time",
    "url",
    "hash",
    "source",
    "summary",
    "investigation_id",
)
SECRET_RE = re.compile(
    r"(password|passwd|secret|api[_-]?key|bearer|authorization|webhook)\s*[:=]\s*\S+",
    re.I,
)
INJECT_RE = re.compile(
    r"(post the |recommend close|do not investigat|do not query|ignore previous)",
    re.I,
)


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a JSON object")
    return data


def redact(value: str) -> str:
    text = SECRET_RE.sub(r"\1=[redacted]", value)
    text = INJECT_RE.sub("[untrusted instruction omitted]", text)
    if len(text) > 500:
        text = text[:497] + "..."
    return text


def payload_from_alert(alert: dict, channel: str) -> dict:
    body = {"channel": channel}
    for key in ALLOWED_FIELDS:
        if key in alert and alert[key] not in (None, ""):
            body[key] = redact(str(alert[key]))
    return body


def pick_route(alert: dict, routes: dict) -> dict:
    severity = str(alert.get("severity") or "").strip().lower()
    for route in routes.get("routes") or []:
        match = route.get("match") or {}
        allowed = [s.lower() for s in match.get("severity") or []]
        if severity and severity in allowed:
            return route
    default = routes.get("default")
    if not default:
        raise ValueError("no matching route and no default")
    return default


def webhook_from_env(route: dict) -> str:
    name = route.get("webhook_env")
    if not name:
        raise ValueError("route missing webhook_env")
    url = os.environ.get(name, "").strip()
    if not url:
        raise ValueError(f"environment variable {name} is unset")
    return url


def host_of(url: str) -> str:
    return (urlparse(url).hostname or "").lower().rstrip(".")


def alert_hosts(alert: dict) -> set[str]:
    found: set[str] = set()
    for key in ("url", "host", "webhook"):
        val = alert.get(key)
        if not val:
            continue
        text = str(val)
        if "://" in text:
            h = host_of(text)
        else:
            h = text.lower().strip().rstrip(".")
        if h:
            found.add(h)
    return found


def validate_webhook(url: str, alert: dict) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("webhook URL must be https")
    dest = (parsed.hostname or "").lower()
    if dest in alert_hosts(alert):
        raise ValueError(
            f"webhook host {dest} is in the alert IOC set; refusing to POST to a lure"
        )


def slack_body(payload: dict) -> dict:
    lines = [f"*{payload.get('title') or 'Alert'}*"]
    for key in ALLOWED_FIELDS:
        if key == "title" or key not in payload:
            continue
        lines.append(f"{key}: `{payload[key]}`")
    text = "\n".join(lines)
    return {"text": text, "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}


def post(url: str, body: dict) -> None:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "soc-agent-skills-notify"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alert", required=True, help="Alert JSON file")
    parser.add_argument("--routes", required=True, help="routes.json")
    parser.add_argument("--send", action="store_true", help="POST (otherwise dry-run)")
    args = parser.parse_args(argv)

    try:
        alert = load_json(Path(args.alert))
        routes = load_json(Path(args.routes))
        route = pick_route(alert, routes)
        channel = str(route.get("channel") or "#soc")
        payload = payload_from_alert(alert, channel)
        for leaked in ("webhook", "password", "commandLine", "analyst_note"):
            if leaked in payload:
                raise ValueError(f"forbidden field {leaked} in payload")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"notify: {exc}", file=sys.stderr)
        return 2

    # Extra: never copy injection fields
    if payload.get("channel") != channel:
        print("notify: channel must come from routes.json", file=sys.stderr)
        return 1

    result = {
        "dry_run": not args.send,
        "channel": channel,
        "webhook_env": route.get("webhook_env"),
        "payload": payload,
        "ignored_from_alert": [
            k for k in ("webhook", "channel", "password", "commandLine", "analyst_note") if k in alert
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.send:
        return 0

    try:
        url = webhook_from_env(route)
        validate_webhook(url, alert)
    except ValueError as exc:
        print(f"notify: FAIL_CLOSED {exc}", file=sys.stderr)
        return 1

    try:
        post(url, slack_body(payload))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"notify: POST failed: {exc}", file=sys.stderr)
        return 1
    print("notify: sent", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
