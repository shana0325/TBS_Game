"""Unit model definitions for turn-based battle logic."""

from __future__ import annotations

from dataclasses import dataclass

from game.core import texts
from game.entity.buff import Buff
from game.entity.skill import Skill


@dataclass(slots=True)
class UnitConfig:
    """Static unit template data."""

    hp: int
    atk: int
    defense: int
    move: int
    range_min: int
    range_max: int

    @property
    def attack_range(self) -> tuple[int, int]:
        # 中文注释：提供统一攻击距离视图，兼容 range_min/range_max 旧字段。
        return self.range_min, self.range_max


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

    def __init__(
        self,
        config: UnitConfig,
        state: UnitState,
        skills: list[Skill] | None = None,
        buffs: list[Buff] | None = None,
    ) -> None:
        self.config = config
        self.state = state
        # 中文注释：skills 保存单位可用技能列表，最小版本不做冷却管理。
        self.skills: list[Skill] = list(skills) if skills is not None else []
        # 中文注释：buffs 保存单位当前挂载的增益/减益状态。
        self.buffs: list[Buff] = list(buffs) if buffs is not None else []

        # 中文注释：逻辑层上下文引用，供 Buff/召唤日志等系统读取。
        self.battle_log: object | None = None
        self.battle_context: object | None = None
        self.summon_duration: int | None = None

    def set_battle_log(self, battle_log: object | None) -> None:
        """Attach battle log reference for logic-layer event logging."""
        self.battle_log = battle_log

    def set_battle_context(self, game: object | None) -> None:
        """Attach game context for combat/trigger/turn systems."""
        self.battle_context = game

    def add_buff(self, buff: Buff) -> None:
        """Add one buff to this unit."""
        self.buffs.append(buff)

    def get_modifier_total(self, stat_name: str) -> int:
        """Return total modifier value from all active buffs for one stat."""
        total = 0
        for buff in self.buffs:
            total += int(buff.modifiers.get(stat_name, 0))
        return total

    def has_counter(self) -> bool:
        """Return True when any active counter buff exists."""
        return any(buff.counter and (buff.duration != 0) for buff in self.buffs)

    def is_stunned(self) -> bool:
        """Return True when any active stun-control buff exists."""
        return any(buff.duration != 0 and buff.control == "stun" for buff in self.buffs)

    def is_silenced(self) -> bool:
        """Return True when any active silence-control buff exists."""
        return any(buff.duration != 0 and buff.control == "silence" for buff in self.buffs)

    def is_dead(self) -> bool:
        """Return True when unit is dead."""
        return not self.state.alive or self.state.hp <= 0

    def move_to(self, x: int, y: int) -> None:
        """Update the unit's position."""
        self.state.pos = (x, y)

    def take_damage(self, amount: int) -> int:
        """Apply incoming damage with shield absorption and return actual HP loss."""
        damage_left = max(0, amount)
        if damage_left <= 0:
            return 0

        # 中文注释：护盾先吸收伤害，剩余值再扣血。
        for buff in self.buffs:
            if damage_left <= 0:
                break

            absorbed = buff.absorb_damage(damage_left)
            if absorbed <= 0:
                continue

            damage_left -= absorbed
            self._log_shield_absorb(buff_name=buff.name, absorbed=absorbed)

        before_hp = self.state.hp
        self.state.hp = max(0, self.state.hp - damage_left)
        self.state.alive = self.state.hp > 0
        return before_hp - self.state.hp

    def _log_shield_absorb(self, buff_name: str, absorbed: int) -> None:
        if self.battle_log is None:
            return

        side = "player" if self.state.team_id == 1 else "enemy"
        unit_name = getattr(self, "name", "Unit")
        self.battle_log.add(
            texts.format_battle_shield_absorb(unit_name, buff_name, absorbed),
            category="shield",
            side=side,
        )

    def attack(self, target: Unit) -> None:
        """Placeholder for attack behavior."""
        pass


