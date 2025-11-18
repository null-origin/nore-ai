# tests/test_fieldstate.py
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import unittest
from datetime import date

from nore_ai.models.fieldstate import FieldState


class DummyEvent:
    """
    Minimal event-like object for testing FieldState aggregation.

    We deliberately don't use the real Event dataclass here so the test
    remains stable even if the Event model gains new fields.
    """
    def __init__(
        self,
        id: str,
        timestamp: str,
        source: str,
        channel: str,
        vectors: list[str],
        laws: list[str] | None = None,
    ) -> None:
        self.id = id
        self.timestamp = timestamp
        self.source = source
        self.channel = channel
        self.vectors = vectors
        self.laws = laws or []


class FieldStateTests(unittest.TestCase):
    def test_from_events_basic_aggregation(self) -> None:
        day = date(2025, 11, 17)

        e1 = DummyEvent(
            id="s-2025-11-17-01",
            timestamp="2025-11-17T15:50:00-05:00",
            source="dad",
            channel="travel",
            vectors=["alignment", "dual-arrival", "continuity"],
            laws=["FL-09", "FL-12", "FL-13"],
        )
        e2 = DummyEvent(
            id="s-2025-11-17-02",
            timestamp="2025-11-17T20:10:00-05:00",
            source="cnbc",
            channel="macro-field",
            vectors=["exposure", "withdrawal", "legitimacy"],
            laws=["FL-06", "FL-12", "FL-13"],
        )

        fs = FieldState.from_events(day, [e1, e2])

        self.assertEqual(fs.id, "fieldstate-2025-11-17")
        self.assertEqual(fs.day, day)
        self.assertEqual(fs.event_ids, ["s-2025-11-17-01", "s-2025-11-17-02"])
        self.assertEqual(fs.event_count, 2)

        self.assertEqual(fs.channels, {"travel": 1, "macro-field": 1})
        self.assertEqual(fs.sources, {"dad": 1, "cnbc": 1})

        self.assertEqual(
            fs.vectors,
            {
                "alignment": 1,
                "dual-arrival": 1,
                "continuity": 1,
                "exposure": 1,
                "withdrawal": 1,
                "legitimacy": 1,
            },
        )

        self.assertEqual(
            fs.laws,
            {
                "FL-09": 1,
                "FL-12": 2,
                "FL-13": 2,
                "FL-06": 1,
            },
        )

        self.assertIsNotNone(fs.time_start)
        self.assertIsNotNone(fs.time_end)
        self.assertLess(fs.time_start, fs.time_end)

        self.assertIn("continuity", fs.summary)
        self.assertIn("dominant_themes", fs.summary)
        self.assertIn("notes", fs.summary)
        self.assertEqual(fs.summary["continuity"], "stable")
        self.assertIsInstance(fs.summary["dominant_themes"], list)

    def test_from_events_empty_day(self) -> None:
        day = date(2025, 11, 18)
        fs = FieldState.from_events(day, [])

        self.assertEqual(fs.id, "fieldstate-2025-11-18")
        self.assertEqual(fs.day, day)
        self.assertEqual(fs.event_count, 0)
        self.assertEqual(fs.event_ids, [])
        self.assertEqual(fs.channels, {})
        self.assertEqual(fs.sources, {})
        self.assertEqual(fs.vectors, {})
        self.assertEqual(fs.laws, {})
        self.assertIsNone(fs.time_start)
        self.assertIsNone(fs.time_end)
        self.assertEqual(fs.summary.get("continuity"), "empty")


if __name__ == "__main__":
    unittest.main()
