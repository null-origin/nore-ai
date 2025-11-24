from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List

from .fieldstate import FieldState


@dataclass
class CycleRegister:
    """
    Aggregate view over an arbitrary structural cycle window.

    This is structurally identical to Weekly / Monthly registers, but the
    start/end range is explicitly defined (not calendar-bound).
    """

    id: str
    range_start: date
    range_end: date

    days: List[str] = field(default_factory=list)
    fieldstates: List[str] = field(default_factory=list)

    event_count: int = 0
    channels: Dict[str, int] = field(default_factory=dict)
    vectors: Dict[str, int] = field(default_factory=dict)
    laws: Dict[str, int] = field(default_factory=dict)

    status: str = "partial"  # "partial" | "complete" | "empty"
    summary: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_fieldstates(
        cls,
        cycle_id: str,
        range_start: date,
        range_end: date,
        fieldstates: List[FieldState],
    ) -> "CycleRegister":
        """
        Build a CycleRegister from a list of FieldStates.

        The caller is responsible for filtering fieldstates to only those
        within [range_start, range_end].
        """
        if not fieldstates:
            return cls(
                id=cycle_id,
                range_start=range_start,
                range_end=range_end,
                days=[],
                fieldstates=[],
                event_count=0,
                channels={},
                vectors={},
                laws={},
                status="empty",
                summary={"notes": "No FieldStates for this cycle window."},
            )

        # Unique, sorted list of days covered by the cycle
        days = sorted({fs.day.isoformat() for fs in fieldstates})

        # IDs of included FieldStates
        fieldstate_ids = [fs.id for fs in fieldstates]

        # Total event count across the cycle
        event_count = sum(fs.event_count for fs in fieldstates)

        channels: Dict[str, int] = {}
        vectors: Dict[str, int] = {}
        laws: Dict[str, int] = {}

        for fs in fieldstates:
            for k, v in fs.channels.items():
                channels[k] = channels.get(k, 0) + v
            for k, v in fs.vectors.items():
                vectors[k] = vectors.get(k, 0) + v
            for k, v in fs.laws.items():
                laws[k] = laws.get(k, 0) + v

        # Dominant themes based on vector frequencies
        dominant_themes: List[str] = []
        if vectors:
            sorted_vecs = sorted(vectors.items(), key=lambda kv: kv[1], reverse=True)
            dominant_themes = [name for name, _ in sorted_vecs[:3]]

        summary: Dict[str, Any] = {
            "notes": "Auto-generated Cycle Register; aggregates FieldState counts only.",
            "dominant_themes": dominant_themes,
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
            laws=laws,
            status="complete",  # close_cycle will only be called when you want closure
            summary=summary,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "range_start": self.range_start.isoformat(),
            "range_end": self.range_end.isoformat(),
            "days": self.days,
            "fieldstates": self.fieldstates,
            "event_count": self.event_count,
            "channels": self.channels,
            "vectors": self.vectors,
            "laws": self.laws,
            "status": self.status,
            "summary": self.summary,
        }
