"""Buff 实体模块：定义持续效果、控制效果、光环与触发逻辑。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.battle.events.event_types import ON_ATTACK, ON_HIT, ON_KILL
from game.core import texts

if TYPE_CHECKING:
    from game.battle.events.battle_event import BattleEvent
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

    def on_trigger(self, unit: Unit, event: BattleEvent, game: object | None) -> None:
        """事件触发：按 trigger 配置执行逻辑（如 counter/lifesteal）。"""
        if self.trigger != event.event_type:
            return

        if self.counter:
            self._handle_counter_trigger(unit, event, game)
            return

        # 中文注释：攻击相关触发默认只对事件攻击者自身生效。
        if event.event_type in (ON_ATTACK, ON_HIT, ON_KILL) and event.source is not unit:
            return

        # 中文注释：当前最小触发实现：heal_percent，用于 on_hit/on_kill 等吸血类效果。
        if self.heal_percent <= 0 or not unit.state.alive:
            return

        damage = int(event.data.get("damage", 0))
        if damage <= 0:
            return

        heal_value = max(0, int(damage * self.heal_percent))
        if heal_value <= 0:
            return

        before_hp = unit.state.hp
        unit.state.hp = min(unit.config.hp, unit.state.hp + heal_value)
        actual_heal = unit.state.hp - before_hp
        if actual_heal <= 0:
            return

        self._log(
            unit=unit,
            game=game,
            message=texts.format_battle_trigger_heal(getattr(unit, 'name', 'Unit'), actual_heal, self.name),
            category="trigger",
        )

    def on_event(self, event_type: str, owner: Unit, context: dict[str, object], game: object | None) -> None:
        """Backward-compatible wrapper for old event dispatch calls."""
        from game.battle.events.battle_event import BattleEvent

        source = context.get("attacker")
        target = context.get("target")
        data = dict(context)
        data.pop("attacker", None)
        data.pop("target", None)
        self.on_trigger(owner, BattleEvent(event_type=event_type, source=source, target=target, data=data), game)

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

    def _handle_counter_trigger(self, unit: Unit, event: BattleEvent, game: object | None) -> None:
        # 中文注释：Counter 只在单位作为受击目标时触发，且反击不再连锁触发反击。
        if not unit.state.alive:
            return
        if event.event_type != ON_HIT:
            return
        if event.target is not unit:
            return
        if bool(event.data.get("is_counter", False)):
            return

        attacker = event.source
        if attacker is None or getattr(attacker, "state", None) is None:
            return
        if not attacker.state.alive:
            return

        if game is None:
            game = unit.battle_context
        if game is None:
            return

        combat_system = getattr(game, "combat_system", None)
        if combat_system is None:
            return
        if not combat_system.is_in_attack_range(unit, attacker):
            return

        counter_damage = combat_system.resolve_attack(unit, attacker, counter=True)
        self._log(
            unit=unit,
            game=game,
            message=texts.format_battle_counter(getattr(unit, 'name', 'Unit'), getattr(attacker, 'name', 'Unit'), counter_damage),
            category="attack",
        )

    def _apply_tick(self, unit: Unit, game: object | None) -> None:
        # 中文注释：先处理持续伤害，再处理持续治疗；两者可并存。
        if self.tick_damage > 0 and unit.state.alive:
            before_hp = unit.state.hp
            actual_damage = unit.take_damage(self.tick_damage)
            if actual_damage > 0:
                self._log(
                    unit=unit,
                    game=game,
                    message=texts.format_battle_tick_damage(getattr(unit, 'name', 'Unit'), actual_damage, self.name),
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
                    message=texts.format_battle_tick_heal(getattr(unit, 'name', 'Unit'), actual_heal, self.name),
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


