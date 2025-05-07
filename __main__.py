from characters.unit import PetType, Pet, Hero
from core.constants import CombatStats
from events.handlers.achivment import AchievementSystem
from events.handlers.notification import NotificationSystem
from events.handlers.social import SocialSystem
from events.observer import EventManager
from game.arena import BruteGame

if __name__ == "__main__":
    event_manager = EventManager()
    notification_system = NotificationSystem(event_manager)
    social_system = SocialSystem(event_manager)
    achievement_system = AchievementSystem(event_manager)

    # Создаем характеристики
    stats1 = CombatStats(
        critical_chance=15,
        evasion=10,
        accuracy=80
    )

    stats2 = CombatStats(
        critical_chance=10,
        evasion=20,
        accuracy=70
    )

    # Создаем героев
    hero1 = Hero(
        lvl=1, hp=100, attack=20, speed=10,
        strange=10, agility=10, combat_stats=stats1, perks=[], event_manager=event_manager, name="MYKA13"
    )

    hero2 = Hero(
        lvl=1, hp=120, attack=15, speed=8,
        strange=8, agility=12, combat_stats=stats2, perks=[], event_manager=event_manager, name="Qerqi"
    )

    # Пример социального взаимодействия
    social_system.send_like(hero2, hero1)
    social_system.invite_friend(hero1, hero2)

    # Добавляем питомца
    pet_stats = CombatStats(critical_chance=5, evasion=15)
    hero1.pets.append(Pet(
        lvl=1, hp=30, attack=10, speed=12,
        strange=5, agility=15, combat_stats=pet_stats,
        pet_type=PetType.DOG, lord=hero1
    ))

    # Запускаем бой
    game = BruteGame(hero1, hero2, event_manager)
    game.start()