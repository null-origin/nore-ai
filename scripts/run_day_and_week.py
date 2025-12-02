# scripts/run_day_and_week.py
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nore_ai.engine.pipeline import run_day_pipeline
from nore_ai.models.event import Event
from nore_ai.models.fieldstate import FieldState
from nore_ai.models.weekly import WeeklyRegister


def parse_date(s: str) -> date:
    year, month, day = map(int, s.split("-"))
    return date(year, month, day)


def read_events_for_day(day: date) -> List[Event]:
    events_path = ROOT / "data" / "events" / f"{day.isoformat()}.jsonl"
    schema_path = ROOT / "schemas" / "event.schema.json"

    config: Dict[str, Any] = {
        "events_path": str(events_path),
        "event_schema": str(schema_path),
        "validate": True,
    }

    events, errors = run_day_pipeline(config)

    print("[nore-ai] run-day completed")
    print(f"  valid events     : {len(events)}")
    print(f"  validation errors: {len(errors)}")
    if errors:
        print("  first few errors:")
        for err in errors[:5]:
            print(f"    - {err}")

    return events


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=False)
    path.write_text(text, encoding="utf-8")


def load_fieldstate(day: date) -> Optional[FieldState]:
    path = ROOT / "data" / "registers" / f"fieldstate-{day.isoformat()}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    return FieldState.from_dict(raw)


def load_weekly_register(week_id: str) -> Optional[WeeklyRegister]:
    path = ROOT / "data" / "registers" / f"{week_id}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    return WeeklyRegister.from_dict(raw)


def compute_week_bounds(day: date) -> tuple[date, date, str]:
    # Monday as start of ISO week
    monday = day - timedelta(days=day.weekday())
    sunday = monday + timedelta(days=6)
    iso_year, iso_week, _ = monday.isocalendar()
    week_id = f"weekly-{iso_year}-W{iso_week:02d}"
    return monday, sunday, week_id


def rebuild_weekly_register(week_start: date, week_end: date, week_id: str) -> WeeklyRegister:
    # Collect all FieldStates in that week
    fieldstates: List[FieldState] = []
    cur = week_start
    while cur <= week_end:
        fs = load_fieldstate(cur)
        if fs is not None:
            fieldstates.append(fs)
        cur += timedelta(days=1)

    weekly = WeeklyRegister.from_fieldstates(
        week_id=week_id,
        week_start=week_start,
        week_end=week_end,
        fieldstates=fieldstates,
    )
    return weekly

def main(date_str: str) -> None:
    day = parse_date(date_str)

    # 1) Ingest + validate events
    events = read_events_for_day(day)

    # 2) Build daily FieldState (if there are in-window events)
    fieldstate = FieldState.from_events(day, events)

    if fieldstate is None:
        print(f"[nore-ai] no in-window events for {day.isoformat()};")
        print("          skipping FieldState write and weekly update.")
        return

    fs_path = ROOT / "data" / "registers" / f"fieldstate-{day.isoformat()}.json"
    write_json(fs_path, fieldstate.to_dict())
    print(f"[nore-ai] wrote FieldState: {fs_path}")

    # 3) Rebuild the entire weekly register that contains this day
    week_start, week_end, week_id = compute_week_bounds(day)
    weekly = rebuild_weekly_register(week_start, week_end, week_id)

    weekly_path = ROOT / "data" / "registers" / f"{week_id}.json"
    write_json(weekly_path, weekly.to_dict())
    print(f"[nore-ai] updated WeeklyRegister: {weekly_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_day_and_week.py YYYY-MM-DD")
        raise SystemExit(1)

    main(sys.argv[1])
