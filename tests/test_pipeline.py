# tests/test_pipeline.py
from __future__ import annotations

import unittest
from pathlib import Path

from nore_ai.engine.pipeline import run_day_pipeline


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        # repo root = parent of this file's directory
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_run_day_pipeline_on_example_file(self) -> None:
        events_path = self.repo_root / "data" / "examples" / "events" / "2025-11-14.jsonl"
        schema_path = self.repo_root / "schemas" / "event.schema.json"

        self.assertTrue(events_path.exists(), f"Missing events file: {events_path}")
        self.assertTrue(schema_path.exists(), f"Missing schema file: {schema_path}")

        config = {
            "events_path": str(events_path),
            "event_schema": str(schema_path),
            "validate": True,
        }

        events, errors = run_day_pipeline(config)

        # At least one event should be valid
        self.assertGreaterEqual(len(events), 1)
        # And there should be no validation errors
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
