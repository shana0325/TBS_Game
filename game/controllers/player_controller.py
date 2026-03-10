"""玩家控制器模块：负责玩家回合输入、移动和攻击行为处理。"""

from __future__ import annotations

import pygame

from game.battle.combat.damage_calculator import calculate_damage
from game.battle.movement.pathfinder import get_reachable_tiles
from game.core.game_state import GameState
from game.entity.unit import Unit
from game.ui.action_menu import ActionMenu


class PlayerController:
    """Handle player-turn input, move and attack logic."""

    def __init__(
        self,
        grid: object,
        combat_system: object,
        player: Unit,
        enemy: Unit,
        turn_manager: object,
        action_menu: ActionMenu,
        tile_size: int,
    ) -> None:
        self.grid = grid
        self.combat_system = combat_system
        self.player = player
        self.enemy = enemy
        self.turn_manager = turn_manager
        self.action_menu = action_menu
        self.tile_size = tile_size

    def update(
        self,
        events: list[pygame.event.Event],
        game_state: GameState,
        battlefield_rect: pygame.Rect,
    ) -> GameState:
        """Process player input and return the next game state."""
        if self.player.state.acted or not self.player.state.alive:
            return GameState.IDLE

        if game_state == GameState.IDLE:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not battlefield_rect.collidepoint(event.pos):
                        continue
                    target_x = event.pos[0] // self.tile_size
                    target_y = event.pos[1] // self.tile_size
                    if (target_x, target_y) == self.player.state.pos:
                        return GameState.UNIT_SELECTED
            return game_state

        if game_state == GameState.UNIT_SELECTED:
            for event in events:
                if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue

                option = self.action_menu.get_option_at_pos(event.pos)
                if option == "Move":
                    return GameState.MOVE_MODE
                if option == "Attack":
                    return GameState.ATTACK_MODE
                if option == "Wait":
                    self.turn_manager.mark_acted(self.player)
                    return GameState.IDLE

            return game_state

        if game_state == GameState.MOVE_MODE:
            for event in events:
                if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue
                if not battlefield_rect.collidepoint(event.pos):
                    continue

                target_x = event.pos[0] // self.tile_size
                target_y = event.pos[1] // self.tile_size

                start_tile = self.grid.get_tile(*self.player.state.pos)
                target_tile = self.grid.get_tile(target_x, target_y)
                if start_tile is None or target_tile is None:
                    return GameState.MOVE_MODE

                # 中文注释：玩家移动只能落在 Player Grid 内。
                if self.grid.get_side_for_position(target_x, target_y) != "player":
                    return GameState.MOVE_MODE
                if (target_x, target_y) == self.enemy.state.pos:
                    return GameState.MOVE_MODE

                reachable = get_reachable_tiles(self.grid, start_tile, self.player.config.move)
                reachable_positions = {(tile.x, tile.y) for tile in reachable}
                if (target_x, target_y) not in reachable_positions:
                    return GameState.MOVE_MODE

                self.player.move_to(target_x, target_y)
                self.turn_manager.mark_acted(self.player)
                return GameState.IDLE

            return game_state

        if game_state == GameState.ATTACK_MODE:
            for event in events:
                if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                    continue
                if not battlefield_rect.collidepoint(event.pos):
                    continue

                target_x = event.pos[0] // self.tile_size
                target_y = event.pos[1] // self.tile_size
                if (target_x, target_y) != self.enemy.state.pos:
                    return GameState.ATTACK_MODE

                if self.combat_system.is_in_attack_range(self.player, self.enemy):
                    damage = calculate_damage(self.player, self.enemy, terrain_bonus=0)
                    self.enemy.take_damage(damage)
                    self.turn_manager.mark_acted(self.player)
                    return GameState.IDLE

                return GameState.ATTACK_MODE

            return game_state

        return game_state
