from __future__ import annotations

from pathlib import Path
from typing import List

from ..io.jsonl_io import read_jsonl
from ..models.event import Event


def ingest_events(path: Path) -> List[Event]:
    """
    Load events from a JSONL file into Event objects.
    Each line must match the Event schema (or be caught by validation later).
    """
    events: List[Event] = []
    for raw in read_jsonl(path):
        events.append(Event.from_dict(raw))
    return events
