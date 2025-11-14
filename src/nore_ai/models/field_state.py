from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Any
from .event import Event


@dataclass
class FieldState:
    """
    The processed daily state: events + derived signals.
    Downstream dashboards will use this object.
    """
    day: date
    events: List[Event]
    summary: Dict[str, Any] = field(default_factory=dict)
