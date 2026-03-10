"""Skill 实体模块：定义技能属性与执行逻辑。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.battle.combat.damage_calculator import calculate_damage

if TYPE_CHECKING:
    from game.entity.unit import Unit


@dataclass(slots=True)
class Skill:
    """最小技能模型。"""

    name: str
    power: float
    min_range: int
    max_range: int

    def execute(self, user: Unit, target: Unit) -> int:
        """执行技能：计算伤害、扣血并返回伤害值。"""
        # 中文注释：当前最小版本仅处理伤害技能，不包含治疗/异常状态。
        damage = calculate_damage(user, target, terrain_bonus=0, skill_power=self.power)
        target.take_damage(damage)
        return damage
