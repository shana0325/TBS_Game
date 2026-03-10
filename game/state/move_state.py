"""Move 状态模块：负责玩家移动输入处理。"""

from __future__ import annotations

import pygame

from game.battle.movement.pathfinder import get_reachable_tiles
from game.core.game_state import GameState
from game.state.game_state_base import GameStateBase


class MoveState(GameStateBase):
    """Handle move target picking and movement execution."""

    def handle_input(
        self,
        game: object,
        events: list[pygame.event.Event],
        battlefield_rect: pygame.Rect,
    ) -> GameStateBase:
        from game.state.idle_state import IdleState

        if game.player.state.acted or not game.player.state.alive:
            game.game_state = GameState.IDLE
            return IdleState()

        for event in events:
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            if not battlefield_rect.collidepoint(event.pos):
                continue

            target_x = event.pos[0] // game.tile_size
            target_y = event.pos[1] // game.tile_size

            start_tile = game.grid.get_tile(*game.player.state.pos)
            target_tile = game.grid.get_tile(target_x, target_y)
            if start_tile is None or target_tile is None:
                return self

            # 中文注释：玩家移动只能落在 Player Grid 内。
            if game.grid.get_side_for_position(target_x, target_y) != "player":
                return self
            if (target_x, target_y) == game.enemy.state.pos:
                return self

            reachable = get_reachable_tiles(game.grid, start_tile, game.player.config.move)
            reachable_positions = {(tile.x, tile.y) for tile in reachable}
            if (target_x, target_y) not in reachable_positions:
                return self

            game.player.move_to(target_x, target_y)
            game.turn_manager.mark_acted(game.player)
            game.game_state = GameState.IDLE
            return IdleState()

        return self
