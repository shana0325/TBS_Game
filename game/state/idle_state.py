"""Idle 状态模块：负责单位选中与行动菜单选择。"""

from __future__ import annotations

import pygame

from game.core.game_state import GameState
from game.state.game_state_base import GameStateBase


class IdleState(GameStateBase):
    """Handle unit selection and action menu choices."""

    def handle_input(
        self,
        game: object,
        events: list[pygame.event.Event],
        battlefield_rect: pygame.Rect,
    ) -> GameStateBase:
        from game.state.attack_state import AttackState
        from game.state.move_state import MoveState

        if game.player.state.acted or not game.player.state.alive:
            game.game_state = GameState.IDLE
            return self

        if game.game_state == GameState.IDLE:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not battlefield_rect.collidepoint(event.pos):
                        continue
                    target_x = event.pos[0] // game.tile_size
                    target_y = event.pos[1] // game.tile_size
                    if (target_x, target_y) == game.player.state.pos:
                        game.game_state = GameState.UNIT_SELECTED
                        return self
            return self

        if game.game_state == GameState.UNIT_SELECTED:
            for event in events:
                if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue

                option = game.action_menu.get_option_at_pos(event.pos)
                if option == "Move":
                    game.game_state = GameState.MOVE_MODE
                    return MoveState()
                if option == "Attack":
                    game.game_state = GameState.ATTACK_MODE
                    return AttackState()
                if option == "Wait":
                    game.turn_manager.mark_acted(game.player)
                    game.game_state = GameState.IDLE
                    return self

        return self
