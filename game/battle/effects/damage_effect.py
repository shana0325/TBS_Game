"""伤害效果模块：执行 damage 类型效果。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entity.unit import Unit


class DamageEffect:
    """伤害效果执行器。"""

    @staticmethod
    def apply(effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        # 中文注释：统一由 CombatSystem 处理普通伤害、事件和触发链。
        power = float(effect_data.get("power", 1.0))
        if power != 1.0:
            from game.battle.combat.damage_calculator import calculate_damage

            return_value = calculate_damage(user, target, terrain_bonus=0, skill_power=power)
            game = user.battle_context
            if game is None or getattr(game, "combat_system", None) is None:
                target.take_damage(return_value)
                return return_value

            game.combat_system.dispatch_event(
                "on_attack",
                {"attacker": user, "target": target, "damage": return_value, "game": game},
            )
            actual_damage = target.take_damage(return_value)
            game.combat_system.dispatch_event(
                "on_hit",
                {"attacker": user, "target": target, "damage": actual_damage, "game": game},
            )
            if target.is_dead():
                game.combat_system.dispatch_event(
                    "on_kill",
                    {"attacker": user, "target": target, "damage": actual_damage, "game": game},
                )
            return actual_damage

        game = user.battle_context
        if game is not None and getattr(game, "combat_system", None) is not None:
            return game.combat_system.resolve_attack(user, target)

        from game.battle.combat.damage_calculator import calculate_damage

        damage = calculate_damage(user, target, terrain_bonus=0, skill_power=power)
        return target.take_damage(damage)
