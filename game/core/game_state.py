"""Game state enum for input and turn flow control."""

from enum import Enum, auto


class GameState(Enum):
    """High-level battle interaction states."""

    IDLE = auto()
    UNIT_SELECTED = auto()
    MOVE_MODE = auto()
    ATTACK_MODE = auto()
    ENEMY_TURN = auto()
