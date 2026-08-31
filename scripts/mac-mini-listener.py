#!/usr/bin/env python3
"""
mac-mini-listener.py
====================
Reference Flask listener that runs on the Mac Mini under launchd.

Responsibilities:
  1. Verify incoming HMAC-SHA256 signature (header: X-SISO-Signature).
  2. Parse the JSON payload.
  3. Execute the appropriate scraper script.
  4. Append a JSONL event line to $LIBRARY_ROOT/_index/events.jsonl.

Payload shape (matches src/app/api/webhook/mac-mini/route.ts):
  {
    "agent":   "youtube" | "twitter" | "reddit" | "people",
    "triggered_by": "web-ui",
    "ts": 1700000000
  }

Environment variables:
  MAC_MINI_WEBHOOK_SECRET  — shared secret for HMAC verification
  LIBRARY_ROOT            — absolute path to SISO_Knowledge

Usage (development):
  flask --app mac-mini-listener run --port 4200
  # or: python3 mac-mini-listener.py
"""

import os
import json
import hmac
import hashlib
import subprocess
import datetime as dt
from pathlib import Path

from flask import Flask, request, abort

# ── Bootstrap ──────────────────────────────────────────────────────────────────

LIBRARY_ROOT = Path(os.environ.get("LIBRARY_ROOT", "/Users/shaansisodia/SISO_Workspace/SISO_Knowledge"))
SECRET = os.environ.get("MAC_MINI_WEBHOOK_SECRET", "")

EVENTS_FILE = LIBRARY_ROOT / "_index" / "events.jsonl"
EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

SCRAPER_MAP = {
    "youtube": "scrapers/run_youtube.sh",
    "twitter": "scrapers/run_twitter.sh",
    "reddit": "scrapers/run_reddit.sh",
    "people": "scrapers/run_people.sh",
}

app = Flask(__name__)


# ── Helpers ─────────────────────────────────────────────────────────────────────

def verify_signature(payload_bytes: bytes, signature_header: str) -> bool:
    """Return True when the request signature matches the HMAC-SHA256 of the payload."""
    if not SECRET:
        return False
    expected = hmac.new(SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)


def emit_event(agent: str, kind: str, meta: dict | None = None) -> None:
    """Atomically append a JSONL line to events.jsonl."""
    record = {
        "ts": dt.datetime.utcnow().isoformat() + "Z",
        "agent": agent,
        "kind": kind,
        "meta": meta or {},
    }
    with EVENTS_FILE.open("a") as fh:
        fh.write(json.dumps(record) + "\n")


# ── Route ───────────────────────────────────────────────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook() -> tuple:
    # 1. Verify HMAC
    raw_body = request.get_data()
    sig = request.headers.get("X-SISO-Signature", "")
    if not verify_signature(raw_body, sig):
        abort(401, description="Invalid HMAC signature.")

    # 2. Parse payload
    try:
        payload = request.get_json()
    except Exception:
        abort(400, description="Invalid JSON body.")

    agent = payload.get("agent", "")
    triggered_by = payload.get("triggered_by", "unknown")
    ts = payload.get("ts")

    if agent not in SCRAPER_MAP:
        abort(400, description=f"Unknown agent: {agent}")

    # 3. Emit run_started
    emit_event(agent, "run_started", {"triggered_by": triggered_by, "ts": ts})

    # 4. Execute scraper
    scraper_path = LIBRARY_ROOT / SCRAPER_MAP[agent]
    try:
        result = subprocess.run(
            ["bash", str(scraper_path)],
            cwd=str(LIBRARY_ROOT),
            capture_output=True,
            timeout=600,
        )
        stdout = result.stdout.decode(errors="replace").strip()
        stderr = result.stderr.decode(errors="replace").strip()
        emit_event(
            agent,
            "run_completed" if result.returncode == 0 else "run_failed",
            {"returncode": result.returncode, "stdout": stdout, "stderr": stderr},
        )
    except subprocess.TimeoutExpired:
        emit_event(agent, "run_failed", {"error": "timeout after 600s"})
        return {"ok": False, "error": "scraper timed out after 600s"}, 408
    except Exception as exc:
        emit_event(agent, "run_failed", {"error": str(exc)})
        return {"ok": False, "error": str(exc)}, 500

    return {"ok": True, "agent": agent}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4200, debug=False)
