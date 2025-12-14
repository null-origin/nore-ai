# src/nore_ai/models/weekly.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from collections import Counter
from typing import Any, Dict, List

from .fieldstate import FieldState


@dataclass
class WeeklyRegister:
    """
    Week-level aggregation of daily FieldStates.

    Backs data/registers/weekly-YYYY-Www.json.
    """
    id: str
    week_start: date
    week_end: date
    days: List[str]
    fieldstates: List[str]
    event_count: int
    channels: Dict[str, int]
    vectors: Dict[str, int]
    status: str = "partial"
    summary: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_fieldstates(
        cls,
        week_id: str,
        week_start: date,
        week_end: date,
        fieldstates: List[FieldState],
    ) -> "WeeklyRegister":
        if not fieldstates:
            return cls(
                id=week_id,
                week_start=week_start,
                week_end=week_end,
                days=[],
                fieldstates=[],
                event_count=0,
                channels={},
                vectors={},
                status="empty",
                summary={
                    "notes": "No FieldState data for this week.",
                    "dominant_themes": []
                },
            )

        days = [fs.day.isoformat() for fs in fieldstates]
        fs_ids = [fs.id for fs in fieldstates]

        event_count = sum(fs.event_count for fs in fieldstates)

        channels = Counter()
        vectors = Counter()
        for fs in fieldstates:
            channels.update(fs.channels)
            vectors.update(fs.vectors)

        dominant_themes = [v for v, _ in vectors.most_common(3)]

        summary = {
            "notes": "Auto-generated weekly register; aggregates FieldState counts only.",
            "dominant_themes": dominant_themes,
        }

        return cls(
            id=week_id,
            week_start=week_start,
            week_end=week_end,
            days=days,
            fieldstates=fs_ids,
            event_count=event_count,
            channels=dict(channels),
            vectors=dict(vectors),
            status="partial",
            summary=summary,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "week_start": self.week_start.isoformat(),
            "week_end": self.week_end.isoformat(),
            "days": self.days,
            "fieldstates": self.fieldstates,
            "event_count": self.event_count,
            "channels": self.channels,
            "vectors": self.vectors,
            "status": self.status,
            "summary": self.summary,
        }
