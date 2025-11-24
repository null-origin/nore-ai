# scripts/close_month.py
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nore_ai.models.fieldstate import FieldState
from nore_ai.models.monthly import MonthlyRegister


def month_bounds_for(d: date) -> tuple[date, date]:
    month_start = date(d.year, d.month, 1)
    if d.month == 12:
        next_month = date(d.year + 1, 1, 1)
    else:
        next_month = date(d.year, d.month + 1, 1)
    month_end = next_month - timedelta(days=1)
    return month_start, month_end


def load_fieldstates_for_month(month_start: date, month_end: date) -> List[FieldState]:
    fieldstates: List[FieldState] = []
    cur = month_start
    while cur <= month_end:
        path = ROOT / "data" / "registers" / f"fieldstate-{cur.isoformat()}.json"
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
    Close a calendar month given any date inside that month.

    Usage:
        python scripts/close_month.py 2025-11-30
    """
    year, month, day = map(int, day_str.split("-"))
    d = date(year, month, day)

    month_start, month_end = month_bounds_for(d)
    month_id = f"monthly-{month_start.year}-{month_start.month:02d}"

    fieldstates = load_fieldstates_for_month(month_start, month_end)

    if not fieldstates:
        print(f"[nore-ai] No FieldState files found for {month_id}. Nothing to close.")
        raise SystemExit(0)

    monthly = MonthlyRegister.from_fieldstates(
        month_id=month_id,
        month_start=month_start,
        month_end=month_end,
        fieldstates=fieldstates,
    )

    # You can tweak notes later if you want a human summary
    monthly.summary.setdefault("notes", "Month closed from existing FieldStates.")

    out_path = ROOT / "data" / "registers" / f"{month_id}.json"
    write_json(out_path, monthly.to_dict())

    print(f"[nore-ai] closed {month_id}")
    print(f"  days included : {[fs.day.isoformat() for fs in fieldstates]}")
    print(f"  event_count   : {monthly.event_count}")
    print(f"  output        : {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/close_month.py YYYY-MM-DD")
        raise SystemExit(1)
    main(sys.argv[1])
