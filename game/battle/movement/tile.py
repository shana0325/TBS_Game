"""Tile model for grid-based battle maps."""

from dataclasses import dataclass


@dataclass(slots=True)
class Tile:
    """Represents one map tile."""

    x: int
    y: int
    move_cost: int = 1
    defense_bonus: int = 0
    passable: bool = True
