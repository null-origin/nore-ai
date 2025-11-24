# scripts/print_monthly_summary.py
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def load_month(month_id: str) -> Dict[str, Any]:
    path = ROOT / "data" / "registers" / f"{month_id}.json"
    if not path.exists():
        print(f"[nore-ai] monthly register not found: {path}")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def _top_n_counts(d: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    return sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:n]


def print_monthly_summary(month: Dict[str, Any]) -> None:
    mid = month.get("id")
    ms = month.get("month_start")
    me = month.get("month_end")
    status = month.get("status")
    event_count = month.get("event_count", 0)

    print(f"[nore-ai] Monthly summary: {mid}")
    print(f"  range      : {ms} → {me}")
    print(f"  status     : {status}")
    print(f"  events     : {event_count}")

    days = month.get("days", [])
    print(f"  days       : {len(days)} day(s)")

    # Dominant themes from summary
    summary = month.get("summary", {})
    dominant = summary.get("dominant_themes") or []
    if dominant:
        print(f"  themes     : {', '.join(dominant)}")
    else:
        print("  themes     : (none)")

    # Top channels
    channels = month.get("channels", {})
    if channels:
        print("\n  top channels:")
        for name, count in _top_n_counts(channels, n=5):
            print(f"    - {name}: {count}")

    # Top vectors
    vectors = month.get("vectors", {})
    if vectors:
        print("\n  top vectors:")
        for name, count in _top_n_counts(vectors, n=5):
            print(f"    - {name}: {count}")

    # Top laws
    laws = month.get("laws", {})
    if laws:
        print("\n  top laws:")
        for name, count in _top_n_counts(laws, n=5):
            print(f"    - {name}: {count}")

    # Optional notes
    notes = summary.get("notes")
    if notes:
        print("\n  notes:")
        print(f"    {notes}")


def main(month_id: str) -> None:
    month = load_month(month_id)
    print_monthly_summary(month)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/print_monthly_summary.py <month_id>")
        print("Example: python scripts/print_monthly_summary.py monthly-2025-11")
        raise SystemExit(1)

    _, mid = sys.argv
    main(mid)
