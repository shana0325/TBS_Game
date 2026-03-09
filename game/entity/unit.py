"""Unit model definitions for turn-based battle logic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UnitConfig:
    """Static unit template data."""

    hp: int
    atk: int
    defense: int
    move: int
    range_min: int
    range_max: int


@dataclass(slots=True)
class UnitState:
    """Runtime unit state inside battle."""

    pos: tuple[int, int]
    hp: int
    acted: bool
    alive: bool
    team_id: int


class Unit:
    """Composable unit object with config and mutable state."""

    def __init__(self, config: UnitConfig, state: UnitState) -> None:
        self.config = config
        self.state = state

    def move_to(self, x: int, y: int) -> None:
        """Update the unit's position."""
        self.state.pos = (x, y)

    def take_damage(self, amount: int) -> None:
        """Apply incoming damage and update alive flag."""
        damage = max(0, amount)
        self.state.hp = max(0, self.state.hp - damage)
        self.state.alive = self.state.hp > 0

    def attack(self, target: Unit) -> None:
        """Placeholder for attack behavior."""
        pass
