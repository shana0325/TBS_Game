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

        actor = game.selected_unit
        if actor is None or actor.state.acted or not actor.state.alive:
            game.selected_unit = None
            game.game_state = GameState.IDLE
            return IdleState()

        for event in events:
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue

            target_pos = game.screen_to_grid(event.pos)
            if target_pos is None:
                continue

            target_unit = game.get_unit_at(target_pos)
            if target_unit is None or target_unit.state.team_id == actor.state.team_id:
                return self

            if game.combat_system.is_in_attack_range(actor, target_unit):
                damage = calculate_damage(actor, target_unit, terrain_bonus=0)
                target_unit.take_damage(damage)
                game.turn_manager.mark_acted(actor)
                game.selected_unit = None
                game.game_state = GameState.IDLE
                return IdleState()

            return self

        return self
