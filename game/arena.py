from collections import deque
from random import randint

from characters.unit import Hero, Pet
from events.base import Event, EventType
from events.observer import EventManager


class TurnQueue(deque):
    pass


# Определить очередность первохода
# Подразумевается что соперник уже найден
class BruteGame:
    def __init__(self, hero1: Hero, hero2: Hero, event_manager: EventManager):
        self.hero1: Hero = hero1
        self.hero2: Hero = hero2
        self.event_manager = event_manager
        self.turn_queue: TurnQueue  = TurnQueue()
        self.round = 0

    def start(self):
        self.prepare_turn_queue()
        while self.hero1.hp > 0 and self.hero2.hp > 0:
            self.process_round()
            self.round += 1

    def prepare_turn_queue(self):
        participants = []
        participants.extend(self.get_all_participants(self.hero1))
        participants.extend(self.get_all_participants(self.hero2))

        # Сортируем по скорости и случайному значению для ничьей
        participants.sort(
            key=lambda x: (x.speed, randint(1, 100)),
            reverse=True
        )
        self.turn_queue.extend(participants)

    def get_all_participants(self, hero: Hero) -> list:
        return [hero] + hero.pets

    def process_round(self):
        print(f"\n--- Round {self.round} ---")
        for _ in range(len(self.turn_queue)):
            attacker = self.turn_queue.popleft()
            if attacker.hp <= 0:
                continue

            defender = self.hero2 if attacker in self.get_all_participants(self.hero1) else self.hero1
            self.process_attack(attacker, defender)
            self.turn_queue.append(attacker)

            if self.hero1.hp <= 0 or self.hero2.hp <= 0:
                break

    def process_attack(self, attacker, defender):
        # Получаем суммарные характеристики
        a_stats = attacker.total_combat_stats() if isinstance(attacker, Hero) else attacker.combat_stats
        d_stats = defender.total_combat_stats() if isinstance(defender, Hero) else defender.combat_stats

        # Расчет шанса попадания
        hit_chance = a_stats.accuracy - d_stats.evasion + (attacker.agility - defender.agility)
        hit_chance = max(min(hit_chance, 95), 5)  # Ограничиваем диапазон

        if randint(1, 100) > hit_chance:
            print(f"{attacker.__class__.__name__} промахнулся!")
            return

        # Расчет критического удара
        is_critical = randint(1, 100) <= a_stats.critical_chance
        damage = attacker.attack * (2 if is_critical else 1)

        # Расчет защиты
        armor = sum(a.armor for a in defender.armor) if isinstance(defender, Hero) else 0
        damage = max(damage - armor, 1)

        # Применение урона
        defender.hp -= damage
        crit_text = " CRITICAL!" if is_critical else ""
        attacker_name = self._get_unit_name(attacker)
        defender_name = self._get_unit_name(defender)
        print(f"{attacker_name} наносит {damage} урона{crit_text} → {defender_name} HP: {max(defender.hp, 0)}")

        if defender.hp <= 0:
            xp_gain = self._calculate_xp(defender)
            if isinstance(attacker, Pet):
                attacker = attacker.lord

            attacker.add_experience(xp_gain, source=defender_name)
            self.event_manager.publish(Event(
                type=EventType.COMBAT_RESULT,
                data={
                    "attacker": attacker_name,
                    "defender": defender.name,
                    "xp_gained": xp_gain
                }
            ))
            defender.death()

    def _calculate_xp(self, defender):
        return defender.lvl * 10

    def _get_unit_name(self, source: Hero | Pet) -> str:
        return source.name if hasattr(source, "name") else source.__class__.__name__