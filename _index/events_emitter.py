"""
Events emitter for SISO Library pipeline.

Emits structured JSONL events and updates agent status files inside
the _index directory. All I/O uses atomic append / write where
possible to avoid corruption from concurrent pipeline runs.

Usage (from _index/ directory or any pipeline working directory):
    from events_emitter import emit_event, emit_agent_status

    emit_event("youtube", "run_started")
    emit_event("hackernews", "item_ingested", page_id="hn_p_12345", meta={"url": "..."})
    emit_agent_status("youtube", "running")
"""

import json
import os
import fcntl
from pathlib import Path
from typing import Optional

from events_schema import PipelineEvent, make_event, VALID_KINDS

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

# Resolve the _index directory once at import time.
_INDEX_DIR = Path(__file__).parent.resolve()

EVENTS_FILE = _INDEX_DIR / "events.jsonl"
AGENT_STATUS_FILE = _INDEX_DIR / "agent-status.json"

# ---------------------------------------------------------------------------
# EventKind set exposed for callers who want to validate before emitting
# ---------------------------------------------------------------------------
VALID_EVENT_KINDS = VALID_KINDS


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def emit_event(
    agent: str,
    kind: str,
    page_id: Optional[str] = None,
    meta: Optional[dict] = None,
) -> str:
    """
    Append a structured JSON line to _index/events.jsonl.

    Args:
        agent:     Name of the pipeline / agent emitting the event.
                   e.g. "youtube", "hackernews", "arxiv", "reddit",
                        "mastodon", "youtube-music", "publish"
        kind:      Event type. Must be one of the VALID_KINDS values:
                   run_started | run_completed | run_failed |
                   item_ingested | item_superseded | item_archived
        page_id:   Optional page identifier (used for item_* events).
        meta:      Optional arbitrary key/value bag.

    Returns:
        The JSON string written to the file (without trailing newline).

    Raises:
        ValueError: if kind is not a recognised EventKind value.
        OSError:   on file I/O errors.

    The write is performed with O_APPEND so concurrent emitters
    (multiple scraper processes) cannot overwrite each other.
    """
    event = make_event(agent=agent, kind=kind, page_id=page_id, meta=meta)
    line = event.to_json_line()

    with open(EVENTS_FILE, "a", encoding="utf-8") as fh:
        # O_APPEND is set by mode "a", but we also take an flock to be
        # extra safe against partial writes on NFS.
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        fh.write(line + "\n")
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

    return line


# ---------------------------------------------------------------------------

def emit_agent_status(agent: str, state: str) -> None:
    """
    Update (or create) an entry for :agent: in agent-status.json.

    The update is atomic: the file is read, the in-memory dict is patched,
    and the entire dict is re-serialized back in a single write (with
    locking) to avoid partial-state corruption.

    Args:
        agent:  Agent name (e.g. "youtube").
        state:  New state string.  Common values:
                idle | running | error | paused | disabled

    Raises:
        OSError / json.JSONDecodeError: on file read/write errors.
    """
    with open(AGENT_STATUS_FILE, "r+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            fh.seek(0)
            content = fh.read()
            status = json.loads(content) if content.strip() else {}
        except json.JSONDecodeError:
            status = {}

        status[agent] = {
            "state": state,
        }

        # Truncate before writing to avoid stale content on shorter replacement.
        fh.seek(0)
        fh.truncate()
        fh.write(json.dumps(status, indent=2) + "\n")
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
