from characters.unit import Hero
from events.base import Event, EventType
from events.observer import EventManager


class SocialSystem:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def send_like(self, sender: Hero, receiver: Hero):
        self.event_manager.publish(Event(
            type=EventType.SOCIAL_INTERACTION,
            data={
                "type": "LIKE",
                "sender": sender.name,
                "receiver": receiver.name
            }
        ))
        receiver.add_experience(1, source=sender.name)

    def invite_friend(self, inviter: Hero, friend: Hero):
        self.event_manager.publish(Event(
            type=EventType.SOCIAL_INTERACTION,
            data={
                "type": "INVITE",
                "inviter": inviter.name,
                "friend": friend.name
            }
        ))
        inviter.add_experience(2, source="Invitation")