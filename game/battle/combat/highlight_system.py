"""高亮计算模块：负责移动范围、路径预览、攻击范围的高亮格子计算。"""

from __future__ import annotations

from typing import Callable

import pygame

from game.battle.movement.pathfinder import get_path_to_tile, get_reachable_tiles
from game.battle.movement.tile import Tile
from game.core.game_state import GameState
from game.entity.unit import Unit


class HighlightSystem:
    """Compute tiles used by highlight renderers."""

    def __init__(
        self,
        grid: object,
        selected_unit_provider: Callable[[], Unit | None],
        turn_manager: object,
        combat_system: object,
        tile_size: int,
        player_camp: str = "player",
    ) -> None:
        self.grid = grid
        self.selected_unit_provider = selected_unit_provider
        self.turn_manager = turn_manager
        self.combat_system = combat_system
        self.tile_size = tile_size
        self.player_camp = player_camp

    def get_move_tiles(self, game_state: GameState) -> list[Tile]:
        # 中文注释：仅在玩家回合且有选中单位时显示可移动高亮。
        if self.turn_manager.current_camp != self.player_camp:
            return []
        if game_state not in (GameState.UNIT_SELECTED, GameState.MOVE_MODE):
            return []

        unit = self.selected_unit_provider()
        if unit is None or not unit.state.alive or unit.state.acted:
            return []

        start_tile = self.grid.get_tile(*unit.state.pos)
        if start_tile is None:
            return []

        tiles = get_reachable_tiles(self.grid, start_tile, unit.config.move)
        return [tile for tile in tiles if self.grid.get_side_for_position(tile.x, tile.y) == self.player_camp]

    def get_path_preview(
        self,
        game_state: GameState,
        battlefield_rect: pygame.Rect,
        move_tiles: list[Tile],
        origin: tuple[int, int],
    ) -> list[Tile]:
        # 中文注释：只有鼠标悬停在可达格子上时，才显示路径预览。
        if self.turn_manager.current_camp != self.player_camp:
            return []
        if game_state != GameState.MOVE_MODE:
            return []
        if not move_tiles:
            return []

        unit = self.selected_unit_provider()
        if unit is None:
            return []

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not battlefield_rect.collidepoint((mouse_x, mouse_y)):
            return []

        ox, oy = origin
        local_x = mouse_x - ox
        local_y = mouse_y - oy
        if local_x < 0 or local_y < 0:
            return []

        tile_x = local_x // self.tile_size
        tile_y = local_y // self.tile_size

        target_tile = self.grid.get_tile(tile_x, tile_y)
        if target_tile is None:
            return []

        move_positions = {(tile.x, tile.y) for tile in move_tiles}
        if (target_tile.x, target_tile.y) not in move_positions:
            return []

        start_tile = self.grid.get_tile(*unit.state.pos)
        if start_tile is None:
            return []

        return get_path_to_tile(self.grid, start_tile, target_tile, unit.config.move)

    def get_attack_tiles(self, game_state: GameState) -> list[Tile]:
        # 中文注释：攻击模式下按选中单位射程高亮对方战场可攻击范围。
        if self.turn_manager.current_camp != self.player_camp:
            return []
        if game_state != GameState.ATTACK_MODE:
            return []

        unit = self.selected_unit_provider()
        if unit is None or not unit.state.alive or unit.state.acted:
            return []

        attacker_side = self.grid.get_side_for_position(*unit.state.pos)

        result: list[Tile] = []
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                tile = self.grid.get_tile(x, y)
                if tile is None:
                    continue

                target_side = self.grid.get_side_for_position(x, y)
                # 中文注释：攻击范围高亮只显示在对方战场，不显示己方战场格子。
                if attacker_side is not None and target_side == attacker_side:
                    continue

                if self.combat_system.is_position_in_attack_range(unit, (x, y)):
                    result.append(tile)

        return result
