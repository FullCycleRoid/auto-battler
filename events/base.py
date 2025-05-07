from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Type, List


class EventType(Enum):
    LEVEL_UP = "LEVEL_UP"
    EXPERIENCE_GAIN = "EXPERIENCE_GAIN"
    SOCIAL_INTERACTION = "SOCIAL_INTERACTION"
    COMBAT_RESULT = "COMBAT_RESULT"


@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: Any = None  # Объект-источник события (Hero, Pet и т.д.)