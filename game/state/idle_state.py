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
        from game.state.skill_state import SkillState

        if game.game_state == GameState.IDLE:
            for event in events:
                if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue

                target = game.screen_to_grid(event.pos)
                if target is None:
                    continue

                # 中文注释：Idle 下允许选中任意存活单位，用于 Unit Info 查看。
                viewable = game.get_viewable_unit_at(target)
                if viewable is not None:
                    game.selected_unit = viewable
                    game.game_state = GameState.UNIT_SELECTED
                    return self

            return self

        if game.game_state == GameState.UNIT_SELECTED:
            for event in events:
                if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue

                # 中文注释：只有可操作单位（玩家且未行动）才响应行动菜单点击。
                if game.can_command_selected_unit():
                    option = game.action_menu.get_option_at_pos(event.pos)
                    if option == "Move":
                        game.game_state = GameState.MOVE_MODE
                        return MoveState()
                    if option == "Attack":
                        game.game_state = GameState.ATTACK_MODE
                        return AttackState()
                    if option == "Skill":
                        if game.selected_unit is not None and game.selected_unit.skills:
                            game.selected_skill = None
                            game.game_state = GameState.SKILL_MODE
                            return SkillState()
                    if option == "Wait":
                        if game.selected_unit is not None:
                            game.turn_manager.mark_acted(game.selected_unit)
                            unit_name = getattr(game.selected_unit, "name", "Unit")
                            game.battle_log.add(f"{unit_name} waits", category="wait", side="player")
                        game.selected_unit = None
                        game.selected_skill = None
                        game.game_state = GameState.IDLE
                        return self

                # 中文注释：菜单外点击战场时，可切换查看任意存活单位。
                target = game.screen_to_grid(event.pos)
                if target is not None:
                    viewable = game.get_viewable_unit_at(target)
                    if viewable is not None:
                        game.selected_unit = viewable
                        return self

        return self
