"""战斗判定模块：负责攻击距离与攻击范围判断，以及战斗事件分发。"""

from __future__ import annotations

from game.entity.unit import Unit


class CombatSystem:
    """Centralized combat range checks and event dispatch for battle interactions."""

    def __init__(self, grid: object) -> None:
        self.grid = grid

    def is_in_attack_range(self, attacker: Unit, defender: Unit) -> bool:
        """Check whether attacker can attack defender at current positions."""
        return self.is_position_in_attack_range(attacker, defender.state.pos)

    def is_position_in_attack_range(self, attacker: Unit, target_pos: tuple[int, int]) -> bool:
        # 中文注释：跨战场时忽略 Y 轴，按“逻辑列差”计算攻击距离。
        attacker_side = self.grid.get_side_for_position(*attacker.state.pos)
        target_side = self.grid.get_side_for_position(*target_pos)

        if attacker_side is not None and target_side is not None and attacker_side != target_side:
            x_distance = self._cross_grid_distance(attacker.state.pos[0], target_pos[0])
            return attacker.config.range_min <= x_distance <= attacker.config.range_max

        ax, ay = attacker.state.pos
        tx, ty = target_pos
        distance = abs(ax - tx) + abs(ay - ty)
        return attacker.config.range_min <= distance <= attacker.config.range_max

    def dispatch_event(self, event_type: str, context: dict[str, object]) -> None:
        """Dispatch combat events to all buff listeners."""
        game = context.get("game")
        if game is None:
            attacker = context.get("attacker")
            game = getattr(attacker, "battle_context", None)
        if game is None:
            return

        units = getattr(game, "units", [])
        for unit in units:
            if not isinstance(unit, Unit):
                continue
            for buff in list(unit.buffs):
                buff.on_event(event_type, owner=unit, context=context, game=game)

    def _cross_grid_distance(self, attacker_x: int, target_x: int) -> int:
        # 中文注释：将两侧战场压缩为逻辑列（0..7）后计算列差。
        return abs(self._to_logical_x(attacker_x) - self._to_logical_x(target_x))

    def _to_logical_x(self, x: int) -> int:
        # 中文注释：敌方战场 X 需减去 gap 偏移，映射到连续逻辑列。
        if x >= self.grid.enemy_offset_x:
            return x - self.grid.gap_width
        return x
