"""Damage calculation utilities for battle combat."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entity.unit import Unit


def calculate_damage(attacker: Unit, defender: Unit, terrain_bonus: int, skill_power: float = 1.0) -> int:
    """Calculate final damage without mutating any unit state."""
    attack = attacker.config.atk
    defense = defender.config.defense + terrain_bonus

    base_damage = max(1, attack - defense)
    # 中文注释：技能倍率作用于基础伤害，最小值仍为 1。
    final_damage = int(base_damage * skill_power)
    return max(1, final_damage)
