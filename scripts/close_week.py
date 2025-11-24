# scripts/close_week.py
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nore_ai.models.fieldstate import FieldState
from nore_ai.models.weekly import WeeklyRegister


def iso_week_id(day: date) -> str:
    year, week, _ = day.isocalendar()
    return f"weekly-{year}-W{week:02d}"


def week_bounds_for(day: date) -> tuple[date, date]:
    # Monday = 0
    weekday = day.weekday()
    start = day - timedelta(days=weekday)
    end = start + timedelta(days=6)
    return start, end


def load_fieldstates_for_week(week_start: date, week_end: date) -> List[FieldState]:
    fieldstates: List[FieldState] = []
    cur = week_start
    while cur <= week_end:
        path = Path(f"data/registers/fieldstate-{cur.isoformat()}.json")
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            fs = FieldState.from_dict(raw)
            fieldstates.append(fs)
        cur += timedelta(days=1)
    return fieldstates


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=False)
    path.write_text(text, encoding="utf-8")


def main(day_str: str) -> None:
    """
    Close a week given any date inside that ISO week.

    Usage:
        python scripts/close_week.py 2025-11-20
    """
    year, month, day = map(int, day_str.split("-"))
    d = date(year, month, day)

    week_start, week_end = week_bounds_for(d)
    week_id = iso_week_id(d)

    fieldstates = load_fieldstates_for_week(week_start, week_end)

    if not fieldstates:
        print(f"[nore-ai] No FieldState files found for week {week_id}. Nothing to close.")
        raise SystemExit(0)

    weekly = WeeklyRegister.from_fieldstates(
        week_id=week_id,
        week_start=week_start,
        week_end=week_end,
        fieldstates=fieldstates,
    )

    # Mark as closed/complete
    weekly.status = "complete"
    # You can add manual notes later if you want
    weekly.summary.setdefault("notes", "Week closed from existing FieldStates.")

    out_path = Path(f"data/registers/{week_id}.json")
    write_json(out_path, weekly.to_dict())

    print(f"[nore-ai] closed week {week_id}")
    print(f"  days included : {[fs.day.isoformat() for fs in fieldstates]}")
    print(f"  event_count   : {weekly.event_count}")
    print(f"  output        : {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/close_week.py YYYY-MM-DD")
        raise SystemExit(1)
    main(sys.argv[1])
