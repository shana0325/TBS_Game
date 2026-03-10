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
        units: list[Unit],
        turn_manager: object,
        enemy_team_id: int = 2,
    ) -> None:
        self.grid = grid
        self.units = units
        self.turn_manager = turn_manager
        self.enemy_team_id = enemy_team_id

    def update(self) -> None:
        """Run one enemy unit action by AI decision each frame."""
        # 中文注释：敌方回合逐单位行动，每帧处理一个可行动单位。
        active_units = [
            unit
            for unit in self.turn_manager.get_active_units()
            if unit.state.team_id == self.enemy_team_id and unit.state.alive
        ]
        if not active_units:
            return

        actor = active_units[0]

        action, target = choose_enemy_action(actor, self.grid, self.units)
        if action == "attack" and isinstance(target, Unit):
            damage = calculate_damage(actor, target, terrain_bonus=0)
            target.take_damage(damage)
        elif action == "move" and target is not None:
            actor.move_to(target.x, target.y)

        self.turn_manager.mark_acted(actor)
