"""复活效果模块：复活死亡单位。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entity.unit import Unit


class ReviveEffect:
    """Revive 效果执行器。"""

    @staticmethod
    def apply(effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        if not target.is_dead():
            return 0

        hp_percent = float(effect_data.get("hp_percent", 0.5))
        hp_percent = max(0.0, min(1.0, hp_percent))

        revive_hp = max(1, int(target.config.hp * hp_percent))
        target.state.hp = revive_hp
        target.state.alive = True
        target.state.acted = True

        game = user.battle_context
        battle_log = None
        if game is not None:
            battle_log = getattr(game, "battle_log", None)
        if battle_log is None:
            battle_log = target.battle_log

        if battle_log is not None:
            actor_name = getattr(user, "name", "Unit")
            target_name = getattr(target, "name", "Unit")
            side = "player" if user.state.team_id == 1 else "enemy"
            battle_log.add(
                f"{actor_name} revives {target_name} with {revive_hp} HP",
                category="revive",
                side=side,
            )
        return 0
