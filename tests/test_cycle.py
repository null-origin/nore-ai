# tests/test_cycle.py
from __future__ import annotations

import unittest
from datetime import date

from nore_ai.models.fieldstate import FieldState
from nore_ai.models.cycle import CycleRegister


class TestCycleRegister(unittest.TestCase):
    def test_cycle_register_from_fieldstates(self):
        # Two mock FieldStates inside the cycle window
        fs1 = FieldState(
            id="fieldstate-2025-11-30",
            day=date(2025, 11, 30),
            event_ids=["e1", "e2"],
            event_count=2,
            channels={"macro-field": 1, "governance": 1},
            sources={"cnbc": 2},
            vectors={"exposure": 1, "continuity": 1},
            laws={"FL-06": 1, "FL-12": 1},
            time_start="2025-11-30T10:00:00-05:00",
            time_end="2025-11-30T20:00:00-05:00",
            summary={"dummy": True},
        )

        fs2 = FieldState(
            id="fieldstate-2025-12-01",
            day=date(2025, 12, 1),
            event_ids=["e3"],
            event_count=1,
            channels={"macro-field": 1},
            sources={"cnbc": 1},
            vectors={"exposure": 1},
            laws={"FL-06": 1},
            time_start="2025-12-01T09:00:00-05:00",
            time_end="2025-12-01T21:00:00-05:00",
            summary={"dummy": True},
        )

        range_start = date(2025, 11, 30)
        range_end = date(2025, 12, 1)

        cycle = CycleRegister.from_fieldstates(
            cycle_id="cycle-8",
            range_start=range_start,
            range_end=range_end,
            fieldstates=[fs1, fs2],
        )

        # ID and bounds
        self.assertEqual(cycle.id, "cycle-8")
        self.assertEqual(cycle.range_start, range_start)
        self.assertEqual(cycle.range_end, range_end)

        # Days (sorted)
        self.assertEqual(
            cycle.days,
            ["2025-11-30", "2025-12-01"],
        )

        # FieldState references
        self.assertEqual(
            cycle.fieldstates,
            ["fieldstate-2025-11-30", "fieldstate-2025-12-01"],
        )

        # Event count
        self.assertEqual(cycle.event_count, 3)

        # Aggregated channels
        self.assertEqual(
            cycle.channels,
            {"macro-field": 2, "governance": 1},
        )

        # Aggregated vectors
        self.assertEqual(
            cycle.vectors,
            {"exposure": 2, "continuity": 1},
        )

        # Aggregated laws
        self.assertEqual(
            cycle.laws,
            {"FL-06": 2, "FL-12": 1},
        )

        # Status and summary
        self.assertEqual(cycle.status, "complete")
        self.assertIn("dominant_themes", cycle.summary)
        self.assertEqual(cycle.summary["dominant_themes"][0], "exposure")

    def test_cycle_register_empty(self):
        # Empty cycle should be marked as "empty"
        range_start = date(2025, 11, 30)
        range_end = date(2025, 12, 1)

        cycle = CycleRegister.from_fieldstates(
            cycle_id="cycle-empty",
            range_start=range_start,
            range_end=range_end,
            fieldstates=[],
        )

        self.assertEqual(cycle.id, "cycle-empty")
        self.assertEqual(cycle.status, "empty")
        self.assertEqual(cycle.event_count, 0)
        self.assertEqual(cycle.days, [])
        self.assertEqual(cycle.fieldstates, [])
        self.assertEqual(cycle.channels, {})
        self.assertEqual(cycle.vectors, {})
        self.assertEqual(cycle.laws, {})
        self.assertIn("notes", cycle.summary)


if __name__ == "__main__":
    unittest.main()
