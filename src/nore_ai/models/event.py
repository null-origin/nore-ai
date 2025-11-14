from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class Event:
    """
    Canonical NORE-AI v1 Event model.

    Matches the current JSONL shape you are actually using.
    """
    id: str
    timestamp: datetime
    source: str
    channel: str
    vectors: List[str]
    text: str
    meta: Dict[str, Any] = field(default_factory=dict)

    # Future extensions (optional at ingest)
    laws: Optional[List[str]] = None
    confidence: Optional[float] = None
    severity: Optional[str] = None
    decision: Optional[str] = None
    status: Optional[str] = None
    runtime: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            source=data["source"],
            channel=data["channel"],
            vectors=list(data.get("vectors", [])),
            text=data["text"],
            meta=data.get("meta", {}) or {},
            laws=data.get("laws"),
            confidence=data.get("confidence"),
            severity=data.get("severity"),
            decision=data.get("decision"),
            status=data.get("status"),
            runtime=data.get("runtime"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "channel": self.channel,
            "vectors": self.vectors,
            "text": self.text,
            "meta": self.meta,
            "laws": self.laws,
            "confidence": self.confidence,
            "severity": self.severity,
            "decision": self.decision,
            "status": self.status,
            "runtime": self.runtime,
        }
