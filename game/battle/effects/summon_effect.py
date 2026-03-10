"""召唤效果模块：根据效果配置在战场上生成单位。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entity.unit import Unit


class SummonEffect:
    """Summon 效果执行器。"""

    @staticmethod
    def apply(effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        # 中文注释：召唤使用施法者阵营；目标参数保留以兼容统一签名。
        _ = target

        game = user.battle_context
        if game is None:
            return 0

        unit_type = str(effect_data.get("unit_type", "")).strip()
        if not unit_type:
            return 0

        summon_pos = SummonEffect._find_summon_position(game=game, user=user)
        if summon_pos is None:
            return 0

        from game.levels.systems.spawn_system import SpawnSystem

        summoned_unit = SpawnSystem.spawn_unit_at(
            grid=game.grid,
            unit_type=unit_type,
            pos=summon_pos,
            team_id=user.state.team_id,
        )

        duration_raw = effect_data.get("duration")
        if duration_raw is not None:
            duration = int(duration_raw)
            if duration > 0:
                summoned_unit.summon_duration = duration

        summoned_unit.set_battle_log(game.battle_log)
        summoned_unit.set_battle_context(game)
        game.units.append(summoned_unit)

        unit_name = getattr(user, "name", "Unit")
        summon_name = getattr(summoned_unit, "name", unit_type)
        side = "player" if user.state.team_id == 1 else "enemy"
        game.battle_log.add(
            f"{unit_name} summons {summon_name} at {summon_pos}",
            category="summon",
            side=side,
        )
        return 0

    @staticmethod
    def _find_summon_position(game: object, user: Unit) -> tuple[int, int] | None:
        # 中文注释：优先在施法者四邻格寻找可通行且未被占用的位置。
        ux, uy = user.state.pos
        center_tile = game.grid.get_tile(ux, uy)
        if center_tile is None:
            return None

        occupied = {unit.state.pos for unit in game.units if unit.state.alive}
        for neighbor in game.grid.get_neighbors(center_tile):
            pos = (neighbor.x, neighbor.y)
            if pos in occupied:
                continue
            return pos

        return None
