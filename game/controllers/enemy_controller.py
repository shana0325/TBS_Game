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
        battle_log: object | None = None,
    ) -> None:
        self.grid = grid
        self.units = units
        self.turn_manager = turn_manager
        self.enemy_team_id = enemy_team_id
        self.battle_log = battle_log

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
        actor_name = getattr(actor, "name", "Enemy")

        action, target = choose_enemy_action(actor, self.grid, self.units)
        if action == "attack" and isinstance(target, Unit):
            damage = calculate_damage(actor, target, terrain_bonus=0)
            target.take_damage(damage)

            defender_name = getattr(target, "name", "Unit")
            self._log(
                f"{actor_name} attacks {defender_name} for {damage} damage",
                category="attack",
                side="enemy",
            )
            if not target.state.alive:
                self._log(f"{defender_name} is defeated", category="defeat", side="player")

        elif action == "move" and target is not None:
            from_pos = actor.state.pos
            actor.move_to(target.x, target.y)
            self._log(
                f"{actor_name} moves {from_pos} -> {(target.x, target.y)}",
                category="move",
                side="enemy",
            )
        else:
            self._log(f"{actor_name} waits", category="wait", side="enemy")

        self.turn_manager.mark_acted(actor)

    def _log(self, message: str, category: str = "info", side: str = "neutral") -> None:
        # 中文注释：控制器不依赖具体日志实现，只调用 add 接口。
        if self.battle_log is None:
            return
        add_fn = getattr(self.battle_log, "add", None)
        if callable(add_fn):
            add_fn(message, category=category, side=side)
