from dataclasses import field, dataclass


@dataclass
class CombatStats:
    critical_chance: int = 0
    evasion: int = 0
    dexterity: int = 0
    accuracy: int = 0
    disarm: int = 0
    combo: int = 0
    block: int = 0
    deflect: int = 0
