import inspect
from abc import ABC
from typing import List

from core.constants import CombatStats
from events.base import Event, EventType
from events.observer import EventManager
from items.weapons import Weapon
from perks.base import Perk


class Unit(ABC):
    def __init__(
            self,
            lvl: int,
            hp: int,
            attack: int,
            speed: int,
            strange: int,
            agility: int,
    ):
        self.lvl = lvl
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.strange = strange
        self.agility = agility

    def death(self):
        if self.hp <= 0:
            print(f"Hero {self.name} is dead!")
            return True
        return False

    def total_combat_stats(self) -> CombatStats:
        total = CombatStats()
        # Базовые характеристики героя
        for stat in vars(self.combat_stats):
            setattr(total, stat, getattr(self.combat_stats, stat))

        # Характеристики от оружия
        for weapon in self.weapons:
            for stat in vars(weapon.combat_stats):
                new_value = getattr(total, stat) + getattr(weapon.combat_stats, stat)
                setattr(total, stat, new_value)

        # Характеристики от брони
        for armor in self.armor:
            for stat in vars(armor.combat_stats):
                new_value = getattr(total, stat) + getattr(armor.combat_stats, stat)
                setattr(total, stat, new_value)

        # Характеристики от питомцев
        for pet in self.pets:
            for stat in vars(pet.combat_stats):
                new_value = getattr(total, stat) + getattr(pet.combat_stats, stat)
                setattr(total, stat, new_value)

        return total


class PetType:
    DOG = "DOG"
    TIGER = "TIGER"


class Pet(Unit):
    def __init__(self, lvl, hp, attack, speed, strange, agility, combat_stats, pet_type, lord):
        super().__init__(lvl, hp, attack, speed, strange, agility)
        self.combat_stats: CombatStats = combat_stats
        self.type: PetType = pet_type
        self.lord = lord


class Hero(Unit):
    def __init__(self, name: str, lvl, hp, attack, speed, strange, agility, combat_stats, perks, event_manager: EventManager):
        super().__init__(lvl, hp, attack, speed, strange, agility)
        self.name = name
        self.weapons: List[Weapon] = []
        self.armor: List[Weapon] = []
        self.pets: List[Pet] = []
        self.perks: List[Perk] = perks
        self.combat_stats: CombatStats = combat_stats
        self.event_manager = event_manager

        self._experience = 0

    def add_experience(self, amount: int, source: str = None):
        self._experience += amount
        self.event_manager.publish(Event(
            type=EventType.EXPERIENCE_GAIN,
            data={
                "amount": amount,
                "source": source,
                "new_total": self._experience
            },
            source=self
        ))
        self._check_level_up()

    def _check_level_up(self):
        required_exp = self._calculate_required_exp()
        if self._experience >= required_exp:
            self._level += 1
            self.event_manager.publish(Event(
                type=EventType.LEVEL_UP,
                data={
                    "new_level": self._level,
                    "previous_level": self._level - 1
                },
                source=self
            ))

    def _calculate_required_exp(self):
        return self.lvl * 100