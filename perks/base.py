from enum import Enum

from core.constants import CombatStats


class ActionType(Enum):
    DOUBLE_ATTACK = "DOUBLE_ATTACK"



class Perk:
    name: str
    description: str

    action: ActionType
    odds: float

    combat_stats: CombatStats