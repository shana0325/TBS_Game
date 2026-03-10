"""效果系统：根据 effect.type 分发到对应效果执行器。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.battle.effects.buff_effect import BuffEffect
from game.battle.effects.damage_effect import DamageEffect
from game.battle.effects.heal_effect import HealEffect
from game.battle.effects.revive_effect import ReviveEffect
from game.battle.effects.summon_effect import SummonEffect

if TYPE_CHECKING:
    from game.entity.unit import Unit


class EffectSystem:
    """技能效果执行分发器。"""

    @staticmethod
    def apply(effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        # 中文注释：支持 damage/heal/buff/summon/revive 五类效果。
        effect_type = str(effect_data.get("type", "")).lower()

        if effect_type == "damage":
            return DamageEffect.apply(effect_data, user, target)
        if effect_type == "heal":
            return HealEffect.apply(effect_data, user, target)
        if effect_type == "buff":
            return BuffEffect.apply(effect_data, user, target)
        if effect_type == "summon":
            return SummonEffect.apply(effect_data, user, target)
        if effect_type == "revive":
            return ReviveEffect.apply(effect_data, user, target)

        # 中文注释：未知效果类型先忽略，避免中断当前技能流程。
        return 0
