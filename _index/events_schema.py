"""
Event schema for SISO Library pipeline events.
Defines typed event records written to _index/events.jsonl.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class EventKind(str, Enum):
    RUN_STARTED = "run_started"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"
    ITEM_INGESTED = "item_ingested"
    ITEM_SUPERSEDED = "item_superseded"
    ITEM_ARCHIVED = "item_archived"


VALID_KINDS: set[str] = {e.value for e in EventKind}


@dataclass
class PipelineEvent:
    """Typed record for a single event written to events.jsonl."""

    ts: str  # ISO-8601 UTC timestamp
    agent: str  # agent name, e.g. "youtube", "hackernews"
    kind: str  # one of EventKind values
    page_id: Optional[str] = None  # page identifier when applicable
    meta: dict = field(default_factory=dict)

    def to_json_line(self) -> str:
        """Serialize to a JSON line (no trailing newline)."""
        import json
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_json_line(cls, line: str) -> "PipelineEvent":
        """Parse a PipelineEvent from a JSON line."""
        import json
        data = json.loads(line)
        return cls(**data)

    @classmethod
    def validate_kind(cls, kind: str) -> None:
        """Raise ValueError if kind is not a known EventKind."""
        if kind not in VALID_KINDS:
            raise ValueError(
                f"Invalid kind {kind!r}. Must be one of: {sorted(VALID_KINDS)}"
            )


def make_timestamp() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_event(
    agent: str,
    kind: str,
    page_id: Optional[str] = None,
    meta: Optional[dict] = None,
) -> PipelineEvent:
    """
    Factory: build a PipelineEvent, validating kind and ts automatically.
    """
    PipelineEvent.validate_kind(kind)
    return PipelineEvent(
        ts=make_timestamp(),
        agent=agent,
        kind=kind,
        page_id=page_id,
        meta=meta or {},
    )
