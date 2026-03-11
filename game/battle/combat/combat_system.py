"""战斗判定模块：负责攻击距离、攻击范围与战斗事件分发。"""

from __future__ import annotations

from game.battle.combat.damage_calculator import calculate_damage
from game.battle.events.battle_event import BattleEvent
from game.battle.events.event_system import EventSystem
from game.battle.events.event_types import ON_ATTACK, ON_HIT, ON_KILL
from game.entity.unit import Unit


class CombatSystem:
    """Centralized combat range checks and event dispatch for battle interactions."""

    def __init__(self, grid: object, event_system: EventSystem | None = None) -> None:
        self.grid = grid
        self.event_system = event_system

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

    def resolve_attack(self, attacker: Unit, defender: Unit, *, counter: bool = False) -> int:
        """Resolve one normal attack and dispatch all related combat events."""
        damage = calculate_damage(attacker, defender, terrain_bonus=0)

        event_data = {
            "damage": damage,
            "game": attacker.battle_context,
            "is_counter": counter,
        }
        self.dispatch(BattleEvent(event_type=ON_ATTACK, source=attacker, target=defender, data=event_data))

        actual_damage = defender.take_damage(damage)
        hit_event = BattleEvent(
            event_type=ON_HIT,
            source=attacker,
            target=defender,
            data={
                "damage": actual_damage,
                "game": attacker.battle_context,
                "is_counter": counter,
            },
        )
        self.dispatch(hit_event)

        if defender.is_dead():
            kill_event = BattleEvent(
                event_type=ON_KILL,
                source=attacker,
                target=defender,
                data={
                    "damage": actual_damage,
                    "game": attacker.battle_context,
                    "is_counter": counter,
                },
            )
            self.dispatch(kill_event)

        return actual_damage

    def dispatch(self, event: BattleEvent) -> None:
        """Dispatch one battle event via EventSystem."""
        if self.event_system is None:
            return
        self.event_system.dispatch(event)

    def dispatch_event(self, event_type: str, context: dict[str, object]) -> None:
        """Compatibility wrapper to dispatch typed events from existing callsites."""
        source = context.get("attacker")
        target = context.get("target")
        data = dict(context)
        data.pop("attacker", None)
        data.pop("target", None)

        self.dispatch(BattleEvent(event_type=event_type, source=source, target=target, data=data))

    def _cross_grid_distance(self, attacker_x: int, target_x: int) -> int:
        # 中文注释：将两侧战场压缩为逻辑列（0..7）后计算列差。
        return abs(self._to_logical_x(attacker_x) - self._to_logical_x(target_x))

    def _to_logical_x(self, x: int) -> int:
        # 中文注释：敌方战场 X 需减去 gap 偏移，映射到连续逻辑列。
        if x >= self.grid.enemy_offset_x:
            return x - self.grid.gap_width
        return x
