from collections import defaultdict
from typing import Dict, List

from events.base import EventType, Event


class EventManager:
    def __init__(self):
        self._subscribers: Dict[EventType, List[callable]] = defaultdict(list)
        self._event_history: List[Event] = []

    def subscribe(self, event_type: EventType, callback: callable):
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: callable):
        self._subscribers[event_type].remove(callback)

    def publish(self, event: Event):
        self._event_history.append(event)
        for callback in self._subscribers.get(event.type, []):
            callback(event)

    def get_history(self, filter_type: EventType = None) -> List[Event]:
        if filter_type:
            return [e for e in self._event_history if e.type == filter_type]
        return self._event_history