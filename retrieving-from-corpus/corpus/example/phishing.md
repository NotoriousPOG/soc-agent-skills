# Phishing download runbook

When a host is alerted for downloading a suspicious executable from email:

- Isolate or restrict the host if execution is unconfirmed.
- Treat the URL and hash as indicators (strings). Do not fetch the lure
  from the analyst workstation or the agent runtime.
- Confirm on-disk file size and a hash of the local copy if one exists.
- Check email gateway for the same subject/hash to other mailboxes.
- Look for follow-on execution, LOLBins, and outbound C2 after the download.
