from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List

from .fieldstate import FieldState


@dataclass
class MonthlyRegister:
    """
    Aggregate view over a calendar month.

    Built from one or more FieldState objects.
    """

    id: str
    month_start: date
    month_end: date

    days: List[str] = field(default_factory=list)
    fieldstates: List[str] = field(default_factory=list)

    event_count: int = 0
    channels: Dict[str, int] = field(default_factory=dict)
    vectors: Dict[str, int] = field(default_factory=dict)

    status: str = "partial"  # "partial" | "complete" | "empty"
    summary: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_fieldstates(
        cls,
        month_id: str,
        month_start: date,
        month_end: date,
        fieldstates: List[FieldState],
    ) -> "MonthlyRegister":
        if not fieldstates:
            return cls(
                id=month_id,
                month_start=month_start,
                month_end=month_end,
                days=[],
                fieldstates=[],
                event_count=0,
                channels={},
                vectors={},
                status="empty",
                summary={"notes": "No FieldStates for this month."},
            )

        # Basic aggregation
        days = sorted({fs.day.isoformat() for fs in fieldstates})
        fieldstate_ids = [fs.id for fs in fieldstates]
        event_count = sum(fs.event_count for fs in fieldstates)

        channels: Dict[str, int] = {}
        vectors: Dict[str, int] = {}

        for fs in fieldstates:
            for k, v in fs.channels.items():
                channels[k] = channels.get(k, 0) + v
            for k, v in fs.vectors.items():
                vectors[k] = vectors.get(k, 0) + v

        # Dominant themes from vectors
        dominant_themes: List[str] = []
        if vectors:
            sorted_vecs = sorted(vectors.items(), key=lambda kv: kv[1], reverse=True)
            dominant_themes = [name for name, _ in sorted_vecs[:3]]

        summary: Dict[str, Any] = {
            "notes": "Auto-generated monthly register; aggregates FieldState counts only.",
            "dominant_themes": dominant_themes,
        }

        return cls(
            id=month_id,
            month_start=month_start,
            month_end=month_end,
            days=days,
            fieldstates=fieldstate_ids,
            event_count=event_count,
            channels=channels,
            vectors=vectors,
            status="complete",  # close_month will only be called when you want closure
            summary=summary,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "month_start": self.month_start.isoformat(),
            "month_end": self.month_end.isoformat(),
            "days": self.days,
            "fieldstates": self.fieldstates,
            "event_count": self.event_count,
            "channels": self.channels,
            "vectors": self.vectors,
            "status": self.status,
            "summary": self.summary,
        }
