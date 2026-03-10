"""治疗效果模块：执行 heal 类型效果。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entity.unit import Unit


class HealEffect:
    """治疗效果执行器。"""

    @staticmethod
    def apply(effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        # 中文注释：最小实现优先使用 amount，未配置时可用 power*atk 兜底。
        amount_raw = effect_data.get("amount")
        if amount_raw is None:
            power = float(effect_data.get("power", 0.0))
            amount = int(max(0, user.config.atk * power))
        else:
            amount = int(amount_raw)

        heal_value = max(0, amount)
        if heal_value <= 0:
            return 0

        before_hp = target.state.hp
        max_hp = target.config.hp
        target.state.hp = min(max_hp, target.state.hp + heal_value)

        # 中文注释：治疗后单位应保持存活标记。
        if target.state.hp > 0:
            target.state.alive = True

        return target.state.hp - before_hp
