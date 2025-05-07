from dataclasses import dataclass
from enum import Enum
from typing import List

from items.base import Item



class DefenceClass(Enum):
    HEAVY = "HEAVY"
    LIGHT = "LIGHT"
    MIDDLE = "MIDDLE"

@dataclass
class Armor(Item):
    name: str
    description: str

    defence_class: List[DefenceClass]
    durability: float
    armor: int
