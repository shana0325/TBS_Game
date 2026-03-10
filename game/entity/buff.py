"""Buff 实体模块：定义持续效果、控制效果、光环与触发逻辑。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entity.unit import Unit


@dataclass(slots=True)
class Buff:
    """可扩展 Buff 模型。"""

    name: str
    duration: int
    modifiers: dict[str, int]
    tick_damage: int = 0
    tick_heal: int = 0
    tick_phase: str | None = None
    control: str | None = None
    shield: int = 0
    counter: bool = False
    aura_range: int = 0
    trigger: str | None = None
    heal_percent: float = 0.0
    is_aura_instance: bool = False

    def on_turn_start(self, unit: Unit, game: object | None) -> None:
        """回合开始触发：支持 turn_start 的 DOT/HOT。"""
        if self.tick_phase == "turn_start":
            self._apply_tick(unit=unit, game=game)

    def on_turn_end(self, unit: Unit, game: object | None) -> None:
        """回合结束触发：支持 turn_end 的 DOT/HOT，并减少持续回合。"""
        if self.tick_phase == "turn_end":
            self._apply_tick(unit=unit, game=game)

        # 中文注释：duration=-1 表示永久 Buff，不递减。
        if self.duration > 0:
            self.duration -= 1

    def on_event(self, event_type: str, owner: Unit, context: dict[str, object], game: object | None) -> None:
        """事件触发：按 trigger 配置执行逻辑（如 lifesteal）。"""
        if self.trigger != event_type:
            return

        # 中文注释：攻击相关触发仅对事件攻击者自身生效。
        if event_type in ("on_attack", "on_hit", "on_kill") and context.get("attacker") is not owner:
            return

        # 中文注释：当前最小触发实现：heal_percent，用于 on_hit/on_kill 等吸血类效果。
        if self.heal_percent <= 0 or not owner.state.alive:
            return

        damage = int(context.get("damage", 0))
        if damage <= 0:
            return

        heal_value = max(0, int(damage * self.heal_percent))
        if heal_value <= 0:
            return

        before_hp = owner.state.hp
        owner.state.hp = min(owner.config.hp, owner.state.hp + heal_value)
        actual_heal = owner.state.hp - before_hp
        if actual_heal <= 0:
            return

        self._log(
            unit=owner,
            game=game,
            message=f"{getattr(owner, 'name', 'Unit')} heals {actual_heal} from trigger {self.name}",
            category="trigger",
        )

    def absorb_damage(self, incoming_damage: int) -> int:
        """使用护盾吸收伤害，返回本次吸收值。"""
        if incoming_damage <= 0 or self.shield <= 0:
            return 0

        absorbed = min(self.shield, incoming_damage)
        self.shield -= absorbed
        return absorbed

    def create_aura_instance(self) -> Buff:
        """基于 aura 源 Buff 生成临时实例，供范围内单位生效。"""
        return Buff(
            name=f"{self.name}_aura",
            duration=1,
            modifiers=dict(self.modifiers),
            is_aura_instance=True,
        )

    def _apply_tick(self, unit: Unit, game: object | None) -> None:
        # 中文注释：先处理持续伤害，再处理持续治疗；两者可并存。
        if self.tick_damage > 0 and unit.state.alive:
            before_hp = unit.state.hp
            unit.take_damage(self.tick_damage)
            actual_damage = before_hp - unit.state.hp
            if actual_damage > 0:
                self._log(
                    unit=unit,
                    game=game,
                    message=f"{getattr(unit, 'name', 'Unit')} suffers {actual_damage} damage from {self.name}",
                    category="buff_tick",
                )

        if self.tick_heal > 0 and unit.state.alive:
            before_hp = unit.state.hp
            max_hp = unit.config.hp
            unit.state.hp = min(max_hp, unit.state.hp + self.tick_heal)
            actual_heal = unit.state.hp - before_hp
            if actual_heal > 0:
                self._log(
                    unit=unit,
                    game=game,
                    message=f"{getattr(unit, 'name', 'Unit')} recovers {actual_heal} HP from {self.name}",
                    category="buff_tick",
                )

    def _log(self, unit: Unit, game: object | None, message: str, category: str) -> None:
        battle_log = None
        if game is not None:
            battle_log = getattr(game, "battle_log", None)
        if battle_log is None:
            battle_log = getattr(unit, "battle_log", None)
        if battle_log is None:
            return

        side = "player" if unit.state.team_id == 1 else "enemy"
        battle_log.add(message, category=category, side=side)
