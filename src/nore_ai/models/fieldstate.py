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
    laws: Dict[str, int]
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    summary: Dict[str, Any] = field(default_factory=dict)

    # ... other methods (to_dict, from_dict, etc.) ...

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

        window_events: List[Event] = []
        for e in events:
            meta = e.meta or {}
            if meta.get("window", False):
                window_events.append(e)

        used_events = window_events if window_events else events

        # sort by timestamp
        used_events = sorted(used_events, key=lambda e: e.ts)

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

        time_start = used_events[0].ts.isoformat()
        time_end = used_events[-1].ts.isoformat()

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
