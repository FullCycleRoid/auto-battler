from dataclasses import dataclass
from random import randint
from typing import List

from core.constants import CombatStats
from items.stones import Stone


@dataclass
class Item:
    combat_stats: CombatStats

    sharpening_multiplier: int
    sharpening_count: int

    stones: List[Stone]

    def sharpening(self):
        result = randint(self.sharpening_multiplier * self.durability * self.sharpening_count)
        if result > 1 or result < 0:
            print(" Armor is break")
            return False

        self.sharpening_multiplier += 1
        return True
