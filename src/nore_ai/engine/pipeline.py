from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from .ingest import ingest_events
from .validate import validate_events
from ..models.event import Event


def run_day_pipeline(config: Dict[str, Any]) -> Tuple[List[Event], List[str]]:
    """
    Run the core NORE-AI pipeline for a single day.

    Expected config keys:
        - "events_path": str | path-like
        - "event_schema": str | path-like
        - "validate": bool (optional, default: True)

    Returns:
        (events, validation_errors)
        - events: list of Event objects (validated if enabled)
        - validation_errors: list of validation error messages
    """
    events_path = Path(config["events_path"])
    event_schema_path = Path(config["event_schema"])
    do_validate = bool(config.get("validate", True))

    # 1) Ingest
    events = ingest_events(events_path)

    # 2) Validate (optional)
    validation_errors: List[str] = []
    if do_validate:
        events, validation_errors = validate_events(events, event_schema_path)

    # --- future steps ---
    # 3) Cluster
    # clusters = cluster_events(events, config.get("cluster", {}))
    #
    # 4) Prioritize
    # prioritized = prioritize_events(clusters, config.get("priority", {}))
    #
    # 5) Build dashboard / summary
    # build_dashboard(prioritized, config.get("dashboard", {}))

    return events, validation_errors
