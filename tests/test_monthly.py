# tests/test_monthly.py
from __future__ import annotations

import unittest
from datetime import date

from nore_ai.models.fieldstate import FieldState
from nore_ai.models.monthly import MonthlyRegister


class TestMonthlyRegister(unittest.TestCase):
    def test_monthly_register_from_fieldstates(self):
        # Two mock FieldStates for Nov 2025
        fs1 = FieldState(
            id="fieldstate-2025-11-17",
            day=date(2025, 11, 17),
            event_ids=["e1", "e2"],
            event_count=2,
            channels={"macro-field": 1, "governance": 1},
            sources={"cnbc": 2},
            vectors={"exposure": 1, "continuity": 1},
            laws={"FL-06": 1, "FL-12": 1},
            time_start="2025-11-17T10:00:00-05:00",
            time_end="2025-11-17T20:00:00-05:00",
            summary={"dummy": True},
        )

        fs2 = FieldState(
            id="fieldstate-2025-11-18",
            day=date(2025, 11, 18),
            event_ids=["e3"],
            event_count=1,
            channels={"macro-field": 1},
            sources={"cnbc": 1},
            vectors={"exposure": 1},
            laws={"FL-06": 1},
            time_start="2025-11-18T09:00:00-05:00",
            time_end="2025-11-18T21:00:00-05:00",
            summary={"dummy": True},
        )

        month_start = date(2025, 11, 1)
        month_end = date(2025, 11, 30)

        monthly = MonthlyRegister.from_fieldstates(
            month_id="monthly-2025-11",
            month_start=month_start,
            month_end=month_end,
            fieldstates=[fs1, fs2],
        )

        # ID and bounds
        self.assertEqual(monthly.id, "monthly-2025-11")
        self.assertEqual(monthly.month_start, month_start)
        self.assertEqual(monthly.month_end, month_end)

        # Days
        self.assertEqual(
            monthly.days,
            ["2025-11-17", "2025-11-18"],
        )

        # FieldState references
        self.assertEqual(
            monthly.fieldstates,
            ["fieldstate-2025-11-17", "fieldstate-2025-11-18"],
        )

        # Event count
        self.assertEqual(monthly.event_count, 3)

        # Aggregated channels
        self.assertEqual(
            monthly.channels,
            {"macro-field": 2, "governance": 1},
        )

        # Aggregated vectors
        self.assertEqual(
            monthly.vectors,
            {"exposure": 2, "continuity": 1},
        )

        # Aggregated laws
        self.assertEqual(
            monthly.laws,
            {"FL-06": 2, "FL-12": 1},
        )

        # Status and summary
        self.assertEqual(monthly.status, "complete")
        self.assertIn("dominant_themes", monthly.summary)
        self.assertEqual(monthly.summary["dominant_themes"][0], "exposure")


if __name__ == "__main__":
    unittest.main()
