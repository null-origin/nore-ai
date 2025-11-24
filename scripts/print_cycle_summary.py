# scripts/print_cycle_summary.py
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def load_cycle(cycle_id: str) -> Dict[str, Any]:
    path = ROOT / "data" / "registers" / f"{cycle_id}.json"
    if not path.exists():
        print(f"[nore-ai] cycle register not found: {path}")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def _top_n_counts(d: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    return sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:n]


def print_cycle_summary(cycle: Dict[str, Any]) -> None:
    cid = cycle.get("id")
    rs = cycle.get("range_start")
    re = cycle.get("range_end")
    status = cycle.get("status")
    event_count = cycle.get("event_count", 0)

    print(f"[nore-ai] Cycle summary: {cid}")
    print(f"  range      : {rs} → {re}")
    print(f"  status     : {status}")
    print(f"  events     : {event_count}")

    days = cycle.get("days", [])
    print(f"  days       : {len(days)} day(s)")

    # Dominant themes from summary
    summary = cycle.get("summary", {})
    dominant = summary.get("dominant_themes") or []
    if dominant:
        print(f"  themes     : {', '.join(dominant)}")
    else:
        print("  themes     : (none)")

    # Top channels
    channels = cycle.get("channels", {})
    if channels:
        print("\n  top channels:")
        for name, count in _top_n_counts(channels, n=5):
            print(f"    - {name}: {count}")

    # Top vectors
    vectors = cycle.get("vectors", {})
    if vectors:
        print("\n  top vectors:")
        for name, count in _top_n_counts(vectors, n=5):
            print(f"    - {name}: {count}")

    # Top laws
    laws = cycle.get("laws", {})
    if laws:
        print("\n  top laws:")
        for name, count in _top_n_counts(laws, n=5):
            print(f"    - {name}: {count}")

    # Optional freeform notes
    notes = summary.get("notes")
    if notes:
        print("\n  notes:")
        print(f"    {notes}")


def main(cycle_id: str) -> None:
    cycle = load_cycle(cycle_id)
    print_cycle_summary(cycle)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/print_cycle_summary.py <cycle_id>")
        print("Example: python scripts/print_cycle_summary.py cycle-8")
        raise SystemExit(1)

    _, cid = sys.argv
    main(cid)
