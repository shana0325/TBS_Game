"""Attack 状态模块：负责玩家攻击输入处理。"""

from __future__ import annotations

import pygame

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
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            # 中文注释：右键可随时取消攻击模式，避免无可攻击目标时卡住。
            if event.button == 3:
                game.game_state = GameState.IDLE
                return IdleState()

            if event.button != 1:
                continue

            # 中文注释：左键点击战场外也取消当前模式。
            if not battlefield_rect.collidepoint(event.pos):
                game.game_state = GameState.IDLE
                return IdleState()

            target_pos = game.screen_to_grid(event.pos)
            if target_pos is None:
                continue

            target_unit = game.get_unit_at(target_pos)
            if target_unit is None or target_unit.state.team_id == actor.state.team_id:
                return self

            if game.combat_system.is_in_attack_range(actor, target_unit):
                damage = game.combat_system.resolve_attack(actor, target_unit)

                # 中文注释：记录玩家攻击事件与可能的击杀结果。
                attacker_name = getattr(actor, "name", "Unit")
                defender_name = getattr(target_unit, "name", "Unit")
                game.battle_log.add(
                    texts.format_battle_attack(attacker_name, defender_name, damage),
                    category="attack",
                    side="player",
                )
                if not target_unit.state.alive:
                    game.battle_log.add(texts.format_battle_defeated(defender_name), category="defeat", side="enemy")

                game.turn_manager.mark_acted(actor)
                game.selected_unit = None
                game.game_state = GameState.IDLE
                return IdleState()

            return self

        return self

