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

        actor = game.selected_unit
        if actor is None or actor.state.acted or not actor.state.alive:
            game.selected_unit = None
            game.game_state = GameState.IDLE
            return IdleState()

        for event in events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            # 中文注释：右键可随时取消移动模式，避免无目标时卡住。
            if event.button == 3:
                game.game_state = GameState.IDLE
                return IdleState()

            if event.button != 1:
                continue

            # 中文注释：左键点击战场外也取消当前模式。
            if not battlefield_rect.collidepoint(event.pos):
                game.game_state = GameState.IDLE
                return IdleState()

            target = game.screen_to_grid(event.pos)
            if target is None:
                continue

            target_x, target_y = target

            start_tile = game.grid.get_tile(*actor.state.pos)
            target_tile = game.grid.get_tile(target_x, target_y)
            if start_tile is None or target_tile is None:
                return self

            # 中文注释：玩家移动只能落在 Player Grid 内，且不能占据已有单位位置。
            if game.grid.get_side_for_position(target_x, target_y) != "player":
                return self
            occupant = game.get_unit_at(target)
            if occupant is not None and occupant is not actor:
                return self

            reachable = get_reachable_tiles(game.grid, start_tile, actor.config.move)
            reachable_positions = {(tile.x, tile.y) for tile in reachable}
            if (target_x, target_y) not in reachable_positions:
                return self

            from_pos = actor.state.pos
            actor.move_to(target_x, target_y)

            # 中文注释：记录玩家移动事件（数据保留，但 UI 层可选择不显示）。
            actor_name = getattr(actor, "name", "Unit")
            game.battle_log.add(
                f"{actor_name} moves {from_pos} -> {(target_x, target_y)}",
                category="move",
                side="player",
            )

            game.turn_manager.mark_acted(actor)
            game.selected_unit = None
            game.game_state = GameState.IDLE
            return IdleState()

        return self
