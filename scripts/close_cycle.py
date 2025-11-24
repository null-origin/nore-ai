# scripts/close_cycle.py
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nore_ai.models.fieldstate import FieldState
from nore_ai.models.cycle import CycleRegister


def parse_date(s: str) -> date:
    year, month, day = map(int, s.split("-"))
    return date(year, month, day)


def load_fieldstates_for_range(start: date, end: date) -> List[FieldState]:
    fieldstates: List[FieldState] = []
    cur = start
    while cur <= end:
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


def main(cycle_id: str, start_str: str, end_str: str) -> None:
    """
    Close a structural cycle over an arbitrary date range.

    Usage:
        python scripts/close_cycle.py cycle-8 2025-11-30 2025-12-14
    """
    range_start = parse_date(start_str)
    range_end = parse_date(end_str)

    if range_end < range_start:
        print(f"[nore-ai] invalid range: {range_start} → {range_end}")
        raise SystemExit(1)

    fieldstates = load_fieldstates_for_range(range_start, range_end)

    if not fieldstates:
        print(f"[nore-ai] no FieldStates found between {range_start} and {range_end}.")
        print("          writing empty CycleRegister.")
    else:
        print(f"[nore-ai] building CycleRegister {cycle_id}")
        print(f"  days covered : {[fs.day.isoformat() for fs in fieldstates]}")

    cycle = CycleRegister.from_fieldstates(
        cycle_id=cycle_id,
        range_start=range_start,
        range_end=range_end,
        fieldstates=fieldstates,
    )

    out_path = ROOT / "data" / "registers" / f"{cycle_id}.json"
    write_json(out_path, cycle.to_dict())

    print(f"[nore-ai] closed cycle {cycle_id}")
    print(f"  event_count : {cycle.event_count}")
    print(f"  status      : {cycle.status}")
    print(f"  output      : {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scripts/close_cycle.py <cycle_id> YYYY-MM-DD YYYY-MM-DD")
        print("Example: python scripts/close_cycle.py cycle-8 2025-11-30 2025-12-14")
        raise SystemExit(1)

    _, cycle_id_arg, start_arg, end_arg = sys.argv
    main(cycle_id_arg, start_arg, end_arg)
