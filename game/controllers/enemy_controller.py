"""敌方控制器模块：负责敌方回合 AI 决策与行动执行。"""

from __future__ import annotations

from game.ai.enemy_ai import choose_enemy_action
from game.battle.combat.damage_calculator import calculate_damage
from game.entity.unit import Unit


class EnemyController:
    """Handle enemy-turn AI decision and action execution."""

    def __init__(
        self,
        grid: object,
        enemy: Unit,
        units: list[Unit],
        turn_manager: object,
    ) -> None:
        self.grid = grid
        self.enemy = enemy
        self.units = units
        self.turn_manager = turn_manager

    def update(self) -> None:
        """Run one enemy action by AI decision."""
        if self.enemy.state.acted or not self.enemy.state.alive:
            return

        action, target = choose_enemy_action(self.enemy, self.grid, self.units)
        if action == "attack" and isinstance(target, Unit):
            damage = calculate_damage(self.enemy, target, terrain_bonus=0)
            target.take_damage(damage)
        elif action == "move" and target is not None:
            self.enemy.move_to(target.x, target.y)

        self.turn_manager.mark_acted(self.enemy)
