# Destinations space

This is where alert notifications go.

1. Copy `routes.example.json` to `routes.json` (gitignored).
2. Set the env vars named in that file to Slack Incoming Webhook URLs, or
   any HTTPS webhook (Teams, ntfy, a homegrown listener).
3. Optionally drop alert JSON files in `alerts/` and run:

```bash
python ../scripts/notify.py \
  --alert destinations/alerts/example.json \
  --routes destinations/routes.json
```

Add `--send` only after a dry-run looks right.

Never commit `routes.json` if you have pasted a raw webhook URL into it.
Prefer env var names as in the example.
