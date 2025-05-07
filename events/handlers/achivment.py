from events.base import EventType, Event
from events.observer import EventManager


class AchievementSystem:
    def __init__(self, event_manager: EventManager):
        event_manager.subscribe(EventType.LEVEL_UP, self.check_level_achievements)
        # event_manager.subscribe(EventType.SOCIAL_INTERACTION, self.check_social_achievements)

    def check_level_achievements(self, event: Event):
        if event.data['new_level'] >= 10:
            print(f"Achievement Unlocked: Veteran Warrior!")
    #
    # def check_social_achievements(self, event: Event):
    #     if event.data['type'] == 'LIKE' and event.data['receiver'] == event.source.name:
    #         print(f"Achievement Unlocked: Popular Hero!")
