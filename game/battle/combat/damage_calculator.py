"""Damage calculation utilities for battle combat."""

from game.entity.unit import Unit


def calculate_damage(attacker: Unit, defender: Unit, terrain_bonus: int) -> int:
    """Calculate final damage without mutating any unit state."""
    attack = attacker.config.atk
    defense = defender.config.defense + terrain_bonus

    damage = attack - defense
    return max(1, damage)
