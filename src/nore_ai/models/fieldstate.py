# src/nore_ai/models/fieldstate.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from collections import Counter
from typing import Any, Dict, List, Optional

from .event import Event


@dataclass
class FieldState:
    """
    Day-level aggregate of events.
    Backs data/registers/fieldstate-YYYY-MM-DD.json.
    """
    id: str
    day: date
    event_ids: List[str]
    event_count: int
    channels: Dict[str, int]
    sources: Dict[str, int]
    vectors: Dict[str, int]
    laws: Dict[str, int]
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None
    summary: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_events(cls, day: date, events: List[Event]) -> "FieldState":
        """
        Build a FieldState for a given calendar day from a list of events.
        Assumes all events belong to `day`.
        """
        if not events:
            return cls(
                id=f"fieldstate-{day.isoformat()}",
                day=day,
                event_ids=[],
                event_count=0,
                channels={},
                sources={},
                vectors={},
                laws={},
                time_start=None,
                time_end=None,
                summary={
                    "continuity": "empty",
                    "dominant_themes": [],
                    "notes": "No events for this day.",
                },
            )

        @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FieldState":
        """
        Rebuild a FieldState from its JSON representation.

        This is mainly for week/month aggregation where we want to
        recompute higher-level registers from stored daily state.
        """
        day = date.fromisoformat(data["date"])

        time_start_raw = data.get("time_start")
        time_end_raw = data.get("time_end")

        time_start = datetime.fromisoformat(time_start_raw) if time_start_raw else None
        time_end = datetime.fromisoformat(time_end_raw) if time_end_raw else None

        return cls(
            id=data["id"],
            day=day,
            event_ids=data.get("event_ids", []),
            event_count=data.get("event_count", 0),
            channels=data.get("channels", {}),
            sources=data.get("sources", {}),
            vectors=data.get("vectors", {}),
            laws=data.get("laws", {}),
            time_start=time_start,
            time_end=time_end,
            summary=data.get("summary", {}),
        )

        # --- Aggregate counts ---
        event_ids = [e.id for e in events]
        channels = Counter(e.channel for e in events)
        sources = Counter(e.source for e in events)
        vector_counts = Counter(v for e in events for v in e.vectors)
        law_counts = Counter(l for e in events for l in (getattr(e, "laws", []) or []))

        # --- Timestamp normalization and sorting ---
        def _event_ts(e: Event) -> datetime:
            """
            Normalize Event timestamp for sorting.
            Supports:
            - e.ts: datetime
            - e.timestamp: datetime or ISO string
            """
            if hasattr(e, "ts"):
                return getattr(e, "ts")

            ts = getattr(e, "timestamp", None)
            if isinstance(ts, datetime):
                return ts
            if isinstance(ts, str):
                return datetime.fromisoformat(ts)

            raise AttributeError("Event has no usable timestamp (ts/timestamp).")

        sorted_by_time = sorted(events, key=_event_ts)
        time_start = _event_ts(sorted_by_time[0])
        time_end = _event_ts(sorted_by_time[-1])

        # --- Simple FieldState summary ---
        continuity = "stable" if len(events) <= 3 else "active"
        dominant_vectors = [v for v, _ in vector_counts.most_common(3)]

        summary = {
            "continuity": continuity,
            "dominant_themes": dominant_vectors,
            "notes": "Auto-generated FieldState summary; frequency-based only.",
        }

        return cls(
            id=f"fieldstate-{day.isoformat()}",
            day=day,
            event_ids=event_ids,
            event_count=len(events),
            channels=dict(channels),
            sources=dict(sources),
            vectors=dict(vector_counts),
            laws=dict(law_counts),
            time_start=time_start,
            time_end=time_end,
            summary=summary,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to a JSON-serializable dict for writing to data/registers/.
        """
        return {
            "id": self.id,
            "date": self.day.isoformat(),
            "event_ids": self.event_ids,
            "event_count": self.event_count,
            "channels": self.channels,
            "sources": self.sources,
            "vectors": self.vectors,
            "laws": self.laws,
            "time_start": self.time_start.isoformat() if self.time_start else None,
            "time_end": self.time_end.isoformat() if self.time_end else None,
            "summary": self.summary,
        }
