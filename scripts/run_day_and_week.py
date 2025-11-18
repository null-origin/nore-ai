# scripts/run_day_and_week.py
from pathlib import Path
import sys

# Ensure src/ is on sys.path so we can import nore_ai without pip install -e .
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Any, List

from nore_ai.engine.pipeline import run_day_pipeline
from nore_ai.models.fieldstate import FieldState
from nore_ai.models.weekly import WeeklyRegister


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=False)
    path.write_text(text, encoding="utf-8")


def iso_week_id(day: date) -> str:
    year, week, _ = day.isocalendar()
    return f"weekly-{year}-W{week:02d}"


def week_bounds_for(day: date) -> (date, date):
    # Monday = 0, Sunday = 6
    weekday = day.weekday()
    week_start = day - timedelta(days=weekday)
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def main(day_str: str) -> None:
    """
    Usage:
        python scripts/run_day_and_week.py 2025-11-17
    """
    events_path = Path(f"data/events/{day_str}.jsonl")
    config = {
        "events_path": str(events_path),
        "event_schema": "schemas/event.schema.json",
        "validate": True,
    }

    events, errors = run_day_pipeline(config)

    print(f"[nore-ai] run-day completed")
    print(f"  valid events     : {len(events)}")
    print(f"  validation errors: {len(errors)}")

    if errors:
        print("  first few errors:")
        for e in errors[:5]:
            print(f"    - {e}")

    year, month, day = map(int, day_str.split("-"))
    d = date(year, month, day)

    # --- FieldState ---
    fieldstate = FieldState.from_events(d, events)
    fs_path = Path(f"data/registers/fieldstate-{day_str}.json")
    write_json(fs_path, fieldstate.to_dict())
    print(f"[nore-ai] wrote {fs_path}")

    # --- Weekly register ---
    week_id = iso_week_id(d)
    week_start, week_end = week_bounds_for(d)
    weekly_path = Path(f"data/registers/{week_id}.json")

    if weekly_path.exists():
        # Load existing weekly, update with this day's FieldState
        raw = json.loads(weekly_path.read_text(encoding="utf-8"))

        # Days / fieldstates: append if not present
        day_iso = d.isoformat()
        if day_iso not in raw.get("days", []):
            raw.setdefault("days", []).append(day_iso)
        if fieldstate.id not in raw.get("fieldstates", []):
            raw.setdefault("fieldstates", []).append(fieldstate.id)

        # Aggregate counts
        raw["event_count"] = raw.get("event_count", 0) + fieldstate.event_count

        def _merge_counts(target_key: str, source_counts: Dict[str, int]) -> None:
            m = raw.get(target_key, {})
            for k, v in source_counts.items():
                m[k] = m.get(k, 0) + v
            raw[target_key] = m

        _merge_counts("channels", fieldstate.channels)
        _merge_counts("vectors", fieldstate.vectors)
        _merge_counts("laws", fieldstate.laws)

        # Status stays "partial" for now; you can flip to "complete" at week close
        write_json(weekly_path, raw)
        print(f"[nore-ai] updated {weekly_path}")
    else:
        # First day of this weekly register
        weekly = WeeklyRegister.from_fieldstates(
            week_id=week_id,
            week_start=week_start,
            week_end=week_end,
            fieldstates=[fieldstate],
        )
        write_json(weekly_path, weekly.to_dict())
        print(f"[nore-ai] wrote {weekly_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python scripts/run_day_and_week.py YYYY-MM-DD")
        raise SystemExit(1)

    main(sys.argv[1])
