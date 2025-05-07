from events.base import EventType, Event
from events.observer import EventManager


class NotificationSystem:
    def __init__(self, event_manager: EventManager):
        event_manager.subscribe(EventType.LEVEL_UP, self.handle_level_up)
        event_manager.subscribe(EventType.EXPERIENCE_GAIN, self.handle_xp_gain)
        event_manager.subscribe(EventType.COMBAT_RESULT, self.report_of_the_battle)

    def handle_level_up(self, event: Event):
        hero = event.source
        print(f"{hero.name} has reached level {event.data['new_level']}.")

    def handle_xp_gain(self, event: Event):
        hero = event.source
        source = event.data.get('source')
        if source:
            print(f"{hero.name} has shown {source} the way out. {event.data['amount']} experience point gained")

    def report_of_the_battle(self, event: Event):
        attacker = event.data.get("attacker")
        defender = event.data.get("defender")
        xp_gained = event.data.get("xp_gained")

        print(f"{defender} lost. {attacker} WIN! Gained {xp_gained} exp")