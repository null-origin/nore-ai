from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from jsonschema import ValidationError, validate as js_validate

from ..io.jsonl_io import load_schema
from ..models.event import Event


def validate_events(
    events: List[Event],
    event_schema_path: Path,
) -> Tuple[List[Event], List[str]]:
    """
    Validate Event objects against the JSON Schema.

    Returns:
        (valid_events, errors)
        - valid_events: Events that passed validation
        - errors: list of human-readable error strings
    """
    schema = load_schema(event_schema_path)
    valid: List[Event] = []
    errors: List[str] = []

    for e in events:
        data = e.to_dict()
        try:
            js_validate(instance=data, schema=schema)
            valid.append(e)
        except ValidationError as exc:
            errors.append(f"{e.id}: {exc.message}")

    return valid, errors
