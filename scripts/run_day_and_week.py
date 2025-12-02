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


# ---------- MARKDOWN VISUALIZATION HELPER ----------

from typing import Dict, Any, List, Tuple
from pathlib import Path
from nore_ai.models.weekly import WeeklyRegister


def _top_n(d: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def _bar(count: int, max_count: int, width: int = 20) -> str:
    if max_count <= 0:
        return ""
    blocks = max(1 if count > 0 else 0, round(count / max_count * width))
    return "■" * blocks


def write_weekly_markdown(weekly: WeeklyRegister, out_path: Path) -> None:
    """
    Render a weekly snapshot as Markdown.

    Non-interpretive: surfaces counts and basic geometry.
    """
    week_id = weekly.id
    week_start = weekly.week_start.isoformat()
    week_end = weekly.week_end.isoformat()
    event_count = weekly.event_count

    summary: Dict[str, Any] = weekly.summary or {}
    notes = summary.get("notes")

    channels: Dict[str, int] = weekly.channels or {}
    vectors: Dict[str, int] = weekly.vectors or {}
    laws: Dict[str, int] = weekly.laws or {}

    top_channels = _top_n(channels, n=5)
    top_vectors = _top_n(vectors, n=5)
    top_laws = _top_n(laws, n=5)

    # Dominant themes: top 4–5 vectors by count
    dominant_themes: List[str] = [name for name, _ in top_vectors][:5]

    # Vector pie chart
    mermaid_pie_lines: List[str] = []
    if vectors:
        mermaid_pie_lines.append("```mermaid")
        mermaid_pie_lines.append("pie showData")
        for name, count in top_vectors:
            mermaid_pie_lines.append(f'    "{name}" : {count}')
        mermaid_pie_lines.append("```")

    # Optional channel→vector matrix
    channel_vectors: Dict[str, Dict[str, int]] = getattr(weekly, "channel_vectors", {}) or {}
    matrix_lines: List[str] = []
    if channel_vectors and top_channels and top_vectors:
        matrix_lines.append("## Channel–vector matrix (top surface)")
        matrix_lines.append("")
        vector_order = [name for name, _ in top_vectors]

        header = "| channel | " + " | ".join(vector_order) + " |"
        sep = "|" + "--------|" * (len(vector_order) + 1)
        matrix_lines.append(header)
        matrix_lines.append(sep)

        for ch_name, _ in top_channels:
            per_vec = channel_vectors.get(ch_name, {}) or {}
            row_cells: List[str] = [ch_name]
            for vname in vector_order:
                val = per_vec.get(vname, 0)
                row_cells.append(str(val) if val else "")
            matrix_lines.append("| " + " | ".join(row_cells) + " |")

        matrix_lines.append("")

    # Shape of the week
    vector_span = len(vectors)
    channel_span = len(channels)
    law_span = len(laws)
    unique_vectors = sorted([name for name, c in vectors.items() if c == 1])

    shape_lines: List[str] = []
    shape_lines.append("## Shape of the week")
    shape_lines.append("")
    shape_lines.append(f"- **Vector span:** {vector_span}")
    shape_lines.append(f"- **Channel span:** {channel_span}")
    shape_lines.append(f"- **Law span:** {law_span}")
    if dominant_themes:
        shape_lines.append(
            f"- **Dominant vector cluster:** {', '.join(dominant_themes[:4])}"
        )
    if unique_vectors:
        shape_lines.append(
            f"- **Unique vectors (count = 1):** {', '.join(unique_vectors)}"
        )
    shape_lines.append("")

    # Build Markdown
    lines: List[str] = []
    lines.append(f"# Weekly Snapshot {week_id}")
    lines.append("")
    lines.append(f"- **Range:** {week_start} → {week_end}")
    lines.append(f"- **Total events:** {event_count}")
    if dominant_themes:
        lines.append(f"- **Dominant themes:** {', '.join(dominant_themes)}")
    else:
        lines.append("- **Dominant themes:** (none)")
    lines.append("")
    lines.append("---")
    lines.append("")

    if mermaid_pie_lines:
        lines.append("## Vector distribution (top 5)")
        lines.append("")
        lines.extend(mermaid_pie_lines)
        lines.append("")

    # Channel distribution: Markdown table + ASCII bar
    if top_channels:
        lines.append("## Channel distribution (top 5)")
        lines.append("")
        lines.append("| channel | count | bar |")
        lines.append("|---------|-------|-----|")
        max_c = top_channels[0][1]
        for name, count in top_channels:
            lines.append(f"| {name} | {count} | {_bar(count, max_c)} |")
        lines.append("")

    # Law distribution: Markdown table + ASCII bar
    if top_laws:
        lines.append("## Law distribution (top 5)")
        lines.append("")
        lines.append("| law | count | bar |")
        lines.append("|-----|-------|-----|")
        max_l = top_laws[0][1]
        for name, count in top_laws:
            lines.append(f"| {name} | {count} | {_bar(count, max_l)} |")
        lines.append("")

    if matrix_lines:
        lines.append("")
        lines.extend(matrix_lines)

    if notes:
        lines.append("## Notes")
        lines.append("")
        lines.append(notes)
        lines.append("")

    lines.extend(shape_lines)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


# ---------- MAIN PIPELINE ----------

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

    # 4) Write a Markdown snapshot for the same weekly register
    weekly_md_path = ROOT / "data" / "registers" / f"{week_id}.md"
    write_weekly_markdown(weekly, weekly_md_path)
    print(f"[nore-ai] wrote WeeklyRegister markdown: {weekly_md_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_day_and_week.py YYYY-MM-DD")
        raise SystemExit(1)

    main(sys.argv[1])
