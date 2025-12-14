# src/nore_ai/models/fieldstate.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from .event import Event


@dataclass
class FieldState:
    id: str
    date: date
    event_ids: List[str]
    event_count: int
    channels: Dict[str, int]
    sources: Dict[str, int]
    vectors: Dict[str, int]
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    summary: Dict[str, Any] = field(default_factory=dict)

    @property
    def day(self) -> date:
        """
        Backwards-compat alias for older code that expects `fs.day`.
        Internally we store this as `date`.
        """
        return self.date

    # ---------- NEW METHODS ----------
    def to_dict(self) -> Dict[str, Any]:
        """Serialize FieldState to a JSON-serializable dict."""
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "event_ids": self.event_ids,
            "event_count": self.event_count,
            "channels": self.channels,
            "sources": self.sources,
            "vectors": self.vectors,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "summary": self.summary,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FieldState":
        """Reconstruct FieldState from a dict (as stored on disk)."""
        return cls(
            id=data["id"],
            date=date.fromisoformat(data["date"]),
            event_ids=data.get("event_ids", []),
            event_count=data.get(
                "event_count",
                len(data.get("event_ids", [])),
            ),
            channels=data.get("channels", {}),
            sources=data.get("sources", {}),
            vectors=data.get("vectors", {}),
            time_start=data.get("time_start"),
            time_end=data.get("time_end"),
            summary=data.get("summary", {}),
        )

    @classmethod
    def from_events(cls, day: date, events: List[Event]) -> Optional["FieldState"]:
        """
        Build a FieldState from a list of Event objects.

        - Prefer events with meta.window == True
        - If none are windowed but there are events, fall back to all events
        - If there are no events at all, return None
        """
        if not events:
            return None

        # Support both `ts` and `timestamp` attribute names
        def get_ts(e: Event):
            if hasattr(e, "ts"):
                return e.ts
            if hasattr(e, "timestamp"):
                return e.timestamp
            raise AttributeError("Event has neither 'ts' nor 'timestamp' attribute")

        window_events: List[Event] = []
        for e in events:
            meta = e.meta or {}
            if meta.get("window", False):
                window_events.append(e)

        used_events = window_events if window_events else events

        # sort by timestamp
        used_events = sorted(used_events, key=get_ts)

        event_ids = [e.id for e in used_events]
        event_count = len(used_events)

        channels: Dict[str, int] = {}
        sources: Dict[str, int] = {}
        vectors: Dict[str, int] = {}
        laws: Dict[str, int] = {}

        for e in used_events:
            channels[e.channel] = channels.get(e.channel, 0) + 1
            sources[e.source] = sources.get(e.source, 0) + 1

            for v in e.vectors:
                vectors[v] = vectors.get(v, 0) + 1

            for law in e.laws:
                laws[law] = laws.get(law, 0) + 1

        time_start = get_ts(used_events[0]).isoformat()
        time_end = get_ts(used_events[-1]).isoformat()

        # dominant themes = top 3 vectors by frequency
        sorted_vectors = sorted(vectors.items(), key=lambda kv: kv[1], reverse=True)
        dominant_themes = [name for name, _ in sorted_vectors[:3]]

        summary = {
            "continuity": "active" if event_count > 0 else "none",
            "dominant_themes": dominant_themes,
            "notes": "Auto-generated FieldState summary; frequency-based only.",
        }

        fs_id = f"fieldstate-{day.isoformat()}"

        return cls(
            id=fs_id,
            date=day,
            event_ids=event_ids,
            event_count=event_count,
            channels=channels,
            sources=sources,
            vectors=vectors,
            laws=laws,
            time_start=time_start,
            time_end=time_end,
            summary=summary,
        )
