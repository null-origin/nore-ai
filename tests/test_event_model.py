# tests/test_event_model.py
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the src/ directory is on sys.path when running tests directly
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import unittest
from datetime import datetime

from nore_ai.models.event import Event


class TestEventModel(unittest.TestCase):
    def test_from_dict_and_to_dict_round_trip(self) -> None:
        raw = {
            "id": "s-2025-11-14-01",
            "timestamp": "2025-11-14T10:30:00-05:00",
            "source": "cnbc",
            "channel": "corporate",
            "vectors": ["exposure", "retrieval"],
            "text": "Walmart CEO Doug McMillon to retire...",
            "meta": {
                "tags": [
                    "walmart",
                    "leadership transition",
                    "retail",
                    "ai transformation",
                ],
                "window": False,
                "note": "legacy arc closure; internal-origin successor signals sector-wide leadership recalibration",
            },
        }

        event = Event.from_dict(raw)

        # Core fields
        self.assertEqual(event.id, raw["id"])
        self.assertEqual(event.source, raw["source"])
        self.assertEqual(event.channel, raw["channel"])
        self.assertEqual(event.vectors, raw["vectors"])
        self.assertEqual(event.text, raw["text"])
        self.assertEqual(event.meta["window"], False)

        # Timestamp parsed properly
        self.assertIsInstance(event.timestamp, datetime)
        # make sure offset is preserved
        self.assertIsNotNone(event.timestamp.tzinfo)

        # Round-trip back to dict
        data = event.to_dict()

        # Required keys present
        for key in ["id", "timestamp", "source", "channel", "vectors", "text", "meta"]:
            self.assertIn(key, data)

        self.assertEqual(data["id"], raw["id"])
        self.assertEqual(data["source"], raw["source"])
        self.assertEqual(data["channel"], raw["channel"])
        self.assertEqual(data["vectors"], raw["vectors"])
        self.assertEqual(data["text"], raw["text"])
        self.assertEqual(data["meta"]["window"], False)

        # Timestamp is string-ified ISO
        self.assertIsInstance(data["timestamp"], str)


if __name__ == "__main__":
    unittest.main()
