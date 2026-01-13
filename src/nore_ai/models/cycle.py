# src/nore_ai/models/cycle.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Iterable, Tuple, Optional

from .fieldstate import FieldState


def _merge_counts(dicts: Iterable[Dict[str, int]]) -> Dict[str, int]:
    merged: Dict[str, int] = {}
    for d in dicts:
        for k, v in d.items():
            merged[k] = merged.get(k, 0) + int(v)
    return merged


def _top_n(d: Dict[str, int], n: int) -> Dict[str, int]:
    """Return top-n entries as a dict, ties broken alphabetically by key."""
    items: List[Tuple[str, int]] = sorted(
        d.items(),
        key=lambda kv: (-kv[1], kv[0]),  # count desc, then name asc
    )
    return {k: v for k, v in items[:n]}


@dataclass
class CycleRegister:
    """
    Aggregated structural view over a cycle window.

    This is the canonical Cycle register shape:

    {
      "id": "cycle-8",
      "range_start": "2025-11-30",
      "range_end": "2025-12-14",
      "days": [...],
      "fieldstates": [...],
      "event_count": 0,
      "channels": {...},
      "vectors": {...},
      "status": "complete" | "partial",
      "summary": {
        "dominant_themes": [...],
        "peak_day": "YYYY-MM-DD" | null,
        "peak_vectors": {...},
        "notes": "Auto-generated cycle register; aggregates FieldState counts only. No interpretive content."
      }
    }
    """

    id: str
    range_start: date
    range_end: date
    days: List[date]
    fieldstates: List[str]
    event_count: int
    channels: Dict[str, int]
    vectors: Dict[str, int]
    status: str = "complete"
    summary: Dict[str, Any] = field(default_factory=dict)

    # ---------- construction ----------

    @classmethod
    def from_fieldstates(
        cls,
        cycle_id: str,
        range_start: date,
        range_end: date,
        fieldstates: List[FieldState],
        status: str = "complete",
    ) -> CycleRegister:
        # sort by day to enforce deterministic ordering
        fieldstates_sorted = sorted(fieldstates, key=lambda fs: fs.day)

        days: List[date] = [fs.day for fs in fieldstates_sorted]
        fieldstate_ids: List[str] = [
            f"fieldstate-{fs.day.isoformat()}" for fs in fieldstates_sorted
        ]

        # aggregates
        event_count = sum(fs.event_count for fs in fieldstates_sorted)
        channels = _merge_counts(fs.channels for fs in fieldstates_sorted)
        vectors = _merge_counts(fs.vectors for fs in fieldstates_sorted)

        # per-day event counts for peak_day calculation
        day_event_counts: Dict[date, int] = {
            fs.day: fs.event_count for fs in fieldstates_sorted
        }

        peak_day: Optional[str] = None
        if day_event_counts:
            # max by event count, then earliest date in case of tie
            max_count = max(day_event_counts.values())
            candidates = [d for d, c in day_event_counts.items() if c == max_count]
            peak_day = min(candidates).isoformat()

        # summary.dominant_themes: top 3 vectors
        top_vectors_sorted = sorted(
            vectors.items(),
            key=lambda kv: (-kv[1], kv[0]),
        )
        dominant_themes: List[str] = [k for k, _ in top_vectors_sorted[:3]]

        summary: Dict[str, Any] = {
            "dominant_themes": dominant_themes,
            "peak_day": peak_day,
            "peak_vectors": _top_n(vectors, n=5),
            "notes": (
                "Auto-generated cycle register; aggregates FieldState counts only. "
                "No interpretive content."
            ),
        }

        return cls(
            id=cycle_id,
            range_start=range_start,
            range_end=range_end,
            days=days,
            fieldstates=fieldstate_ids,
            event_count=event_count,
            channels=channels,
            vectors=vectors,
            status=status,
            summary=summary,
        )

    # ---------- (de)serialization ----------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "range_start": self.range_start.isoformat(),
            "range_end": self.range_end.isoformat(),
            "days": [d.isoformat() for d in self.days],
            "fieldstates": self.fieldstates,
            "event_count": self.event_count,
            "channels": dict(self.channels),
            "vectors": dict(self.vectors),
            "status": self.status,
            "summary": dict(self.summary),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CycleRegister:
        rs = date.fromisoformat(data["range_start"])
        re = date.fromisoformat(data["range_end"])
        days = [date.fromisoformat(d) for d in data.get("days", [])]

        return cls(
            id=data["id"],
            range_start=rs,
            range_end=re,
            days=days,
            fieldstates=list(data.get("fieldstates", [])),
            event_count=int(data.get("event_count", 0)),
            channels={k: int(v) for k, v in data.get("channels", {}).items()},
            vectors={k: int(v) for k, v in data.get("vectors", {}).items()},
            status=data.get("status", "complete"),
            summary=dict(data.get("summary", {})),
        )
