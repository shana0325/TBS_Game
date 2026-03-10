"""Attack 状态模块：负责玩家攻击输入处理。"""

from __future__ import annotations

import pygame

from game.battle.combat.damage_calculator import calculate_damage
from game.core.game_state import GameState
from game.state.game_state_base import GameStateBase


class AttackState(GameStateBase):
    """Handle attack target click and attack execution."""

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
            if (target_x, target_y) != game.enemy.state.pos:
                return self

            if game.combat_system.is_in_attack_range(game.player, game.enemy):
                damage = calculate_damage(game.player, game.enemy, terrain_bonus=0)
                game.enemy.take_damage(damage)
                game.turn_manager.mark_acted(game.player)
                game.game_state = GameState.IDLE
                return IdleState()

            return self

        return self
