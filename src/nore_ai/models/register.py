from dataclasses import dataclass, field
from typing import List
from .event import Event


@dataclass
class Register:
    """
    A named collection of events — e.g.
    'Macro Signals', 'Daily', 'Cycle 8 Ignition', etc.
    """
    id: str
    name: str
    events: List[Event] = field(default_factory=list)

    def add(self, event: Event) -> None:
        self.events.append(event)
