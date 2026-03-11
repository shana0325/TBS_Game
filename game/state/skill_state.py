"""Skill 状态模块：负责技能选择与释放流程。"""

from __future__ import annotations

import pygame

from game.core import texts

from game.core.game_state import GameState
from game.state.game_state_base import GameStateBase


class SkillState(GameStateBase):
    """Handle skill pick and target selection."""

    def handle_input(
        self,
        game: object,
        events: list[pygame.event.Event],
        battlefield_rect: pygame.Rect,
    ) -> GameStateBase:
        from game.state.idle_state import IdleState

        actor = game.selected_unit
        if actor is None or actor.state.acted or not actor.state.alive:
            game.selected_skill = None
            game.selected_unit = None
            game.game_state = GameState.IDLE
            return IdleState()

        for event in events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            # 中文注释：右键可随时取消技能模式。
            if event.button == 3:
                game.selected_skill = None
                game.game_state = GameState.IDLE
                return IdleState()

            if event.button != 1:
                continue

            # 中文注释：第一步在技能菜单中选择要释放的技能。
            chosen_skill = game.skill_menu.get_skill_at_pos(event.pos)
            if chosen_skill is not None:
                game.selected_skill = chosen_skill
                continue

            # 中文注释：未选技能前点击战场不生效。
            if game.selected_skill is None:
                continue

            target_pos = game.screen_to_grid(event.pos)
            if target_pos is None:
                continue

            target_unit = game.get_unit_at(target_pos)
            if target_unit is None or target_unit.state.team_id == actor.state.team_id:
                continue

            if not self._is_in_skill_range(game, actor.state.pos, target_pos, game.selected_skill.min_range, game.selected_skill.max_range):
                continue

            damage = game.selected_skill.execute(actor, target_unit)
            actor_name = getattr(actor, "name", "Unit")
            skill_name = game.selected_skill.name
            defender_name = getattr(target_unit, "name", "Unit")
            game.battle_log.add(
                texts.format_skill_use(actor_name, skill_name, defender_name, damage),
                category="attack",
                side="player",
            )
            if not target_unit.state.alive:
                game.battle_log.add(texts.format_battle_defeated(defender_name), category="defeat", side="enemy")

            game.turn_manager.mark_acted(actor)
            game.selected_skill = None
            game.selected_unit = None
            game.game_state = GameState.IDLE
            return IdleState()

        return self

    def _is_in_skill_range(
        self,
        game: object,
        user_pos: tuple[int, int],
        target_pos: tuple[int, int],
        min_range: int,
        max_range: int,
    ) -> bool:
        # 中文注释：与 CombatSystem 一致：跨战场忽略 Y 轴，按逻辑列差计算。
        grid = game.grid
        user_side = grid.get_side_for_position(*user_pos)
        target_side = grid.get_side_for_position(*target_pos)

        if user_side is not None and target_side is not None and user_side != target_side:
            user_x = self._to_logical_x(grid, user_pos[0])
            target_x = self._to_logical_x(grid, target_pos[0])
            distance = abs(user_x - target_x)
            return min_range <= distance <= max_range

        distance = abs(user_pos[0] - target_pos[0]) + abs(user_pos[1] - target_pos[1])
        return min_range <= distance <= max_range

    def _to_logical_x(self, grid: object, x: int) -> int:
        if x >= grid.enemy_offset_x:
            return x - grid.gap_width
        return x



