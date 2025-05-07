from dataclasses import dataclass, Field, field
from enum import Enum
from typing import List

from items.base import Item


class WeaponType(Enum):
    HEAVY = "HEAVY"
    BLUNT = "BLUNT"
    THROWN = "THROWN"
    FAST = "FAST"
    LONG = "LONG"


@dataclass
class Weapon(Item):
    name: str
    description: str

    types: List[WeaponType]
    odds: float
    hit_speed: int
    damage: int
    draw_chance: int
    reach: 0
