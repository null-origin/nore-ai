# run_day.py
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure src/ is on sys.path so we can import nore_ai without installing
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nore_ai.engine.pipeline import run_day_pipeline  # type: ignore[import]


def build_config_from_events(events_path: Path) -> Dict[str, Any]:
    return {
        "events_path": str(events_path),
        "event_schema": "schemas/event.schema.json",
        "validate": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python run_day.py",
        description="Run NORE-AI pipeline for a single day",
    )
    parser.add_argument(
        "-e",
        "--events",
        type=Path,
        required=True,
        help="Path to a JSONL events file (data/events/YYYY-MM-DD.jsonl)",
    )

    args = parser.parse_args()
    config = build_config_from_events(args.events)

    events, errors = run_day_pipeline(config)

    print("[nore-ai] run-day completed")
    print(f"  valid events     : {len(events)}")
    print(f"  validation errors: {len(errors)}")
    if errors:
        print("  first few errors:")
        for err in errors[:5]:
            print(f"    - {err}")


if __name__ == "__main__":
    main()
