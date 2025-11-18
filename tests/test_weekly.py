# tests/test_weekly.py
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import unittest
from datetime import date

from nore_ai.models.weekly import WeeklyRegister


class DummyFieldState:
    """
    Minimal FieldState-like object for testing WeeklyRegister aggregation.

    We keep this tiny on purpose:
    WeeklyRegister only relies on:
      - id
      - day
      - event_count
      - channels
      - vectors
      - laws
    """
    def __init__(
        self,
        id: str,
        day: date,
        event_count: int,
        channels: dict[str, int],
        vectors: dict[str, int],
        laws: dict[str, int],
    ) -> None:
        self.id = id
        self.day = day
        self.event_count = event_count
        self.channels = channels
        self.vectors = vectors
        self.laws = laws


class WeeklyRegisterTests(unittest.TestCase):
    def test_from_fieldstates_basic_aggregation(self) -> None:
        week_start = date(2025, 11, 17)  # Monday
        week_end = date(2025, 11, 23)    # Sunday
        week_id = "weekly-2025-W47"

        fs1 = DummyFieldState(
            id="fieldstate-2025-11-17",
            day=date(2025, 11, 17),
            event_count=2,
            channels={"travel": 1},
            vectors={"alignment": 1, "dual-arrival": 1},
            laws={"FL-09": 1, "FL-12": 1},
        )

        fs2 = DummyFieldState(
            id="fieldstate-2025-11-18",
            day=date(2025, 11, 18),
            event_count=3,
            channels={"macro-field": 2},
            vectors={"exposure": 2, "continuity": 1},
            laws={"FL-06": 1, "FL-12": 2},
        )

        weekly = WeeklyRegister.from_fieldstates(
            week_id=week_id,
            week_start=week_start,
            week_end=week_end,
            fieldstates=[fs1, fs2],
        )

        # Basic identity
        self.assertEqual(weekly.id, week_id)
        self.assertEqual(weekly.week_start, week_start)
        self.assertEqual(weekly.week_end, week_end)

        # Days and fieldstates
        self.assertEqual(
            sorted(weekly.days),
            ["2025-11-17", "2025-11-18"],
        )
        self.assertEqual(
            sorted(weekly.fieldstates),
            ["fieldstate-2025-11-17", "fieldstate-2025-11-18"],
        )

        # Event count is sum of day counts
        self.assertEqual(weekly.event_count, 5)

        # Channels are aggregated
        self.assertEqual(
            weekly.channels,
            {"travel": 1, "macro-field": 2},
        )

        # Vectors are aggregated
        self.assertEqual(
            weekly.vectors,
            {
                "alignment": 1,
                "dual-arrival": 1,
                "exposure": 2,
                "continuity": 1,
            },
        )

        # Laws are aggregated
        self.assertEqual(
            weekly.laws,
            {
                "FL-09": 1,
                "FL-12": 3,  # 1 + 2
                "FL-06": 1,
            },
        )

        # Status + summary
        self.assertEqual(weekly.status, "partial")
        self.assertIn("notes", weekly.summary)
        self.assertIn("dominant_themes", weekly.summary)
        self.assertIsInstance(weekly.summary["dominant_themes"], list)
        # At least the highest-frequency vector should be in dominant_themes
        self.assertIn("exposure", weekly.summary["dominant_themes"])

    def test_from_fieldstates_empty_week(self) -> None:
        week_start = date(2025, 11, 24)
        week_end = date(2025, 11, 30)
        week_id = "weekly-2025-W48"

        weekly = WeeklyRegister.from_fieldstates(
            week_id=week_id,
            week_start=week_start,
            week_end=week_end,
            fieldstates=[],
        )

        self.assertEqual(weekly.id, week_id)
        self.assertEqual(weekly.week_start, week_start)
        self.assertEqual(weekly.week_end, week_end)
        self.assertEqual(weekly.days, [])
        self.assertEqual(weekly.fieldstates, [])
        self.assertEqual(weekly.event_count, 0)
        self.assertEqual(weekly.channels, {})
        self.assertEqual(weekly.vectors, {})
        self.assertEqual(weekly.laws, {})
        self.assertEqual(weekly.status, "empty")
        self.assertEqual(weekly.summary.get("dominant_themes"), [])


if __name__ == "__main__":
    unittest.main()
