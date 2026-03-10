"""Basic enemy decision logic for turn-based battles."""

from __future__ import annotations

from game.battle.combat.damage_calculator import calculate_damage
from game.battle.movement.pathfinder import get_reachable_tiles
from game.battle.movement.tile import Tile
from game.entity.unit import Unit


def choose_enemy_action(unit: Unit, grid: object, units: list[Unit]) -> tuple[str, Unit | Tile | None]:
    """Return one action decision: attack, move, or wait."""
    if not unit.state.alive:
        return ("wait", None)

    player_units = [
        target
        for target in units
        if target.state.alive and target.state.team_id != unit.state.team_id
    ]
    if not player_units:
        return ("wait", None)

    attackable_targets = [
        target for target in player_units if _is_in_attack_range(unit, target, grid)
    ]
    if attackable_targets:
        killable_targets = [
            target
            for target in attackable_targets
            if calculate_damage(unit, target, terrain_bonus=0) >= target.state.hp
        ]
        candidates = killable_targets if killable_targets else attackable_targets
        best_target = min(
            candidates,
            key=lambda target: (
                target.state.hp,
                _distance(unit.state.pos, target.state.pos),
                target.state.pos[1],
                target.state.pos[0],
            ),
        )
        return ("attack", best_target)

    start_tile = grid.get_tile(*unit.state.pos)
    if start_tile is None or not start_tile.passable:
        return ("wait", None)

    reachable_tiles = get_reachable_tiles(grid, start_tile, unit.config.move)
    occupied_positions = {
        other.state.pos for other in units if other.state.alive and other is not unit
    }
    movable_tiles = [
        tile
        for tile in reachable_tiles
        if (tile.x, tile.y) != unit.state.pos and (tile.x, tile.y) not in occupied_positions
    ]
    if not movable_tiles:
        return ("wait", None)

    current_distance = min(_distance(unit.state.pos, target.state.pos) for target in player_units)
    better_tiles = [
        tile
        for tile in movable_tiles
        if min(_distance((tile.x, tile.y), target.state.pos) for target in player_units)
        < current_distance
    ]
    if not better_tiles:
        return ("wait", None)

    best_tile = min(
        better_tiles,
        key=lambda tile: (
            min(_distance((tile.x, tile.y), target.state.pos) for target in player_units),
            tile.y,
            tile.x,
        ),
    )
    return ("move", best_tile)


def _is_in_attack_range(attacker: Unit, defender: Unit, grid: object) -> bool:
    # 中文注释：跨战场时忽略 Y 轴，按“逻辑列差”计算攻击距离。
    if hasattr(grid, "get_side_for_position") and hasattr(grid, "enemy_offset_x") and hasattr(grid, "gap_width"):
        attacker_side = grid.get_side_for_position(*attacker.state.pos)
        defender_side = grid.get_side_for_position(*defender.state.pos)
        if attacker_side is not None and defender_side is not None and attacker_side != defender_side:
            x_distance = _cross_grid_distance(attacker.state.pos[0], defender.state.pos[0], grid)
            return attacker.config.range_min <= x_distance <= attacker.config.range_max

    distance = _distance(attacker.state.pos, defender.state.pos)
    return attacker.config.range_min <= distance <= attacker.config.range_max


def _cross_grid_distance(attacker_x: int, defender_x: int, grid: object) -> int:
    # 中文注释：将两侧战场压缩为逻辑列（0..7）后计算列差。
    return abs(_to_logical_x(attacker_x, grid) - _to_logical_x(defender_x, grid))


def _to_logical_x(x: int, grid: object) -> int:
    # 中文注释：敌方战场 X 需减去 gap 偏移，映射到连续逻辑列。
    if x >= grid.enemy_offset_x:
        return x - grid.gap_width
    return x


def _distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


