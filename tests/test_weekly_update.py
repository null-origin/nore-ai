from __future__ import annotations

import unittest
from datetime import date

from nore_ai.models.weekly import WeeklyRegister


class DummyFieldState:
    """
    Minimal FieldState-like object reused from weekly tests.
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


class WeeklyUpdateTests(unittest.TestCase):
    def test_weekly_update_recomputes_dominant_themes(self) -> None:
        week_start = date(2025, 11, 17)
        week_end = date(2025, 11, 23)
        week_id = "weekly-2025-W47"

        # Day 1: like your 11-17 day — alignment/dual-arrival/continuity.
        fs1 = DummyFieldState(
            id="fieldstate-2025-11-17",
            day=date(2025, 11, 17),
            event_count=2,
            channels={"travel": 1},
            vectors={"alignment": 1, "dual-arrival": 1, "continuity": 1},
            laws={"FL-09": 1, "FL-12": 2, "FL-13": 2, "FL-06": 1},
        )

        weekly = WeeklyRegister.from_fieldstates(
            week_id=week_id,
            week_start=week_start,
            week_end=week_end,
            fieldstates=[fs1],
        )

        # Initial dominant themes come from fs1 only.
        initial_themes = weekly.summary.get("dominant_themes", [])
        self.assertIn("alignment", initial_themes)
        self.assertIn("continuity", initial_themes)

        # Simulate writing to JSON, then reading back as dict.
        raw = weekly.to_dict()

        # Day 2: like your 11-18 day — strong exposure/continuity/signal.
        fs2 = DummyFieldState(
            id="fieldstate-2025-11-18",
            day=date(2025, 11, 18),
            event_count=6,
            channels={"macro-field": 2},
            vectors={"collapse": 3, "exposure": 5, "continuity": 5, "signal": 4},
            laws={"FL-06": 6, "FL-12": 6, "FL-13": 6, "FL-09": 3},
        )

        # --- simulate scripts/run_day_and_week.py update branch ---

        # Append day / fieldstate if not present
        day_iso = fs2.day.isoformat()
        if day_iso not in raw.get("days", []):
            raw.setdefault("days", []).append(day_iso)
        if fs2.id not in raw.get("fieldstates", []):
            raw.setdefault("fieldstates", []).append(fs2.id)

        # Update event_count
        raw["event_count"] = raw.get("event_count", 0) + fs2.event_count

        # Merge counts like _merge_counts in the script
        def _merge_counts(target_key: str, source_counts: dict[str, int]) -> None:
            m = raw.get(target_key, {})
            for k, v in source_counts.items():
                m[k] = m.get(k, 0) + v
            raw[target_key] = m

        _merge_counts("channels", fs2.channels)
        _merge_counts("vectors", fs2.vectors)
        _merge_counts("laws", fs2.laws)

        # Recompute dominant themes from updated vectors
        vectors = raw.get("vectors", {})
        if isinstance(vectors, dict) and vectors:
            sorted_vecs = sorted(vectors.items(), key=lambda kv: kv[1], reverse=True)
            dominant = [name for name, _ in sorted_vecs[:3]]
            raw.setdefault("summary", {})
            raw["summary"]["dominant_themes"] = dominant

        # --- assertions on updated weekly state ---

        # Event count should be 2 + 6 = 8
        self.assertEqual(raw["event_count"], 8)

        # Vectors aggregated: continuity and exposure should now dominate
        self.assertGreaterEqual(raw["vectors"]["continuity"], 6)
        self.assertGreaterEqual(raw["vectors"]["exposure"], 5)

        # Dominant themes should now reflect the updated mix
        updated_themes = raw["summary"]["dominant_themes"]
        self.assertIn("continuity", updated_themes)
        self.assertIn("exposure", updated_themes)

        # The set of themes should have changed relative to the initial state
        self.assertNotEqual(set(initial_themes), set(updated_themes))


if __name__ == "__main__":
    unittest.main()
