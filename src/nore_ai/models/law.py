from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Law:
    """
    Structural law metadata (FL-XX, OCI-XX, CL-XX).
    These are referenced by events but do not enforce logic yet.
    """
    id: str
    name: str
    description: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
