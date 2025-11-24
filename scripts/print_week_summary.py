# scripts/print_week_summary.py
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Dict, Any, List, Tuple
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]


def _top_k(d: Dict[str, int], k: int = 5) -> List[Tuple[str, int]]:
    return sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:k]


def main(week_id: str) -> None:
    """
    Print a human-friendly summary of a weekly register.
    
    Usage:
        python scripts/print_week_summary.py weekly-2025-W47
    """
    path = ROOT / "data" / "registers" / f"{week_id}.json"
    if not path.exists():
        print(f"[nore-ai] weekly register not found: {path}")
        raise SystemExit(1)

    raw = json.loads(path.read_text(encoding="utf-8"))

    print(f"\n=== WEEKLY SUMMARY: {week_id} ===")
    print(f"Week: {raw['week_start']} → {raw['week_end']}")
    print(f"Days captured: {len(raw.get('days', []))}  ({', '.join(raw.get('days', []))})")
    print(f"Total events: {raw.get('event_count', 0)}")
    print(f"Status: {raw.get('status', 'unknown')}")

    print("\n--- Top Channels ---")
    for name, count in _top_k(raw.get("channels", {})):
        print(f"{name:20} {count:3}")

    print("\n--- Top Vectors ---")
    for name, count in _top_k(raw.get("vectors", {})):
        print(f"{name:20} {count:3}")

    print("\n--- Top Laws ---")
    for name, count in _top_k(raw.get("laws", {})):
        print(f"{name:10} {count:3}")

    print("\n--- Dominant Themes ---")
    for t in raw.get("summary", {}).get("dominant_themes", []):
        print(f"- {t}")

    print("\n--- Notes ---")
    print(raw.get("summary", {}).get("notes", "(none)"))

    print("\n===============================\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/print_week_summary.py weekly-YYYY-Www")
        raise SystemExit(1)

    main(sys.argv[1])
