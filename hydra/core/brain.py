from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Awaitable

from .storage import Storage


class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Intelligence:
    head: str
    competitor: str
    discovery: str
    threat_level: ThreatLevel
    confidence: float
    timestamp: datetime
    data: Dict[str, Any] | None = None
    recommended_action: str | None = None

    def to_record(self) -> Dict[str, Any]:
        return {
            "head": self.head,
            "competitor": self.competitor,
            "discovery": self.discovery,
            "threat_level": self.threat_level.value,
            "confidence": float(self.confidence),
            "timestamp": self.timestamp.isoformat(),
            "data": None if self.data is None else str(self.data),
            "recommended_action": self.recommended_action,
        }


class Brain:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.heads: Dict[str, Any] = {}
        self.subscribers: List[Callable[[Intelligence], Awaitable[None]]] = []

    async def init(self) -> None:
        await self.storage.init()

    def attach_head(self, name: str, head: Any) -> None:
        head.brain = self
        self.heads[name] = head

    async def process_intelligence(self, intel: Intelligence) -> None:
        await self.storage.save_intelligence(intel.to_record())
        for subscriber in list(self.subscribers):
            await subscriber(intel)

    def on_intelligence(self, handler: Callable[[Intelligence], Awaitable[None]]) -> None:
        self.subscribers.append(handler)

