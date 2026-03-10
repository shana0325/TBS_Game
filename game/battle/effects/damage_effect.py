"""伤害效果模块：执行 damage 类型效果。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.battle.combat.damage_calculator import calculate_damage

if TYPE_CHECKING:
    from game.entity.unit import Unit


class DamageEffect:
    """伤害效果执行器。"""

    @staticmethod
    def apply(effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        # 中文注释：damage 支持 power 倍率，默认 1.0。
        power = float(effect_data.get("power", 1.0))
        damage = calculate_damage(user, target, terrain_bonus=0, skill_power=power)

        game = user.battle_context
        if game is not None and getattr(game, "combat_system", None) is not None:
            game.combat_system.dispatch_event(
                "on_attack",
                {"attacker": user, "target": target, "damage": damage, "game": game},
            )

        target.take_damage(damage, attacker=user)
        return damage
