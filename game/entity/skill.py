"""Skill 实体模块：定义技能属性与执行逻辑。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from game.battle.effects.effect_system import EffectSystem

if TYPE_CHECKING:
    from game.entity.unit import Unit


@dataclass(slots=True)
class Skill:
    """技能模型：通过 effects 驱动具体效果执行。"""

    name: str
    power: float
    min_range: int
    max_range: int
    effects: list[dict[str, object]] = field(default_factory=list)

    def execute(self, user: Unit, target: Unit) -> int:
        """执行技能：遍历效果列表并交给 EffectSystem 处理。"""
        # 中文注释：兼容旧技能数据（仅 power，无 effects）时自动转为 damage 效果。
        effect_list = self.effects
        if not effect_list:
            effect_list = [{"type": "damage", "power": self.power}]

        total_value = 0
        for effect_data in effect_list:
            total_value += EffectSystem.apply(effect_data, user, target)
        return total_value
