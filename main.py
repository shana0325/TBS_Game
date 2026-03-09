"""Pygame entry point to validate core TBS systems integration."""

from __future__ import annotations

import pygame

from game.ai.enemy_ai import choose_enemy_action
from game.battle.combat.damage_calculator import calculate_damage
from game.battle.movement.grid import Grid
from game.battle.movement.pathfinder import get_reachable_tiles
from game.battle.turn.turn_manager import ENEMY, PLAYER, TurnManager
from game.entity.unit import Unit, UnitConfig, UnitState
from game.render.map_renderer import TILE_SIZE, render_map
from game.ui.hud import render_hud

BACKGROUND_COLOR = (245, 245, 245)
FPS = 60


def main() -> None:
    pygame.init()

    grid = Grid(10, 10)
    screen = pygame.display.set_mode((grid.width * TILE_SIZE, grid.height * TILE_SIZE))
    pygame.display.set_caption("TBS Game - Pygame Integration")
    clock = pygame.time.Clock()

    player = Unit(
        UnitConfig(hp=20, atk=6, defense=2, move=3, range_min=1, range_max=1),
        UnitState(pos=(0, 0), hp=20, acted=False, alive=True, team_id=1),
    )
    enemy = Unit(
        UnitConfig(hp=18, atk=5, defense=1, move=3, range_min=1, range_max=1),
        UnitState(pos=(9, 9), hp=18, acted=False, alive=True, team_id=2),
    )

    units = [player, enemy]
    turn_manager = TurnManager(units=units, player_team_id=1, enemy_team_id=2)

    running = True
    while running and player.state.alive and enemy.state.alive:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if not running:
            break

        if turn_manager.current_camp == PLAYER:
            handle_player_turn(events, grid, player, enemy, turn_manager)
        elif turn_manager.current_camp == ENEMY:
            handle_enemy_turn(grid, enemy, units, player, turn_manager)

        if turn_manager.is_turn_finished():
            turn_manager.next_turn()

        screen.fill(BACKGROUND_COLOR)
        render_map(screen, grid, units)
        render_hud(screen, units, turn_manager.current_camp)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def handle_player_turn(
    events: list[pygame.event.Event],
    grid: Grid,
    player: Unit,
    enemy: Unit,
    turn_manager: TurnManager,
) -> None:
    if player.state.acted or not player.state.alive:
        return

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if is_in_attack_range(player, enemy):
                damage = calculate_damage(player, enemy, terrain_bonus=0)
                enemy.take_damage(damage)
                turn_manager.mark_acted(player)
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            target_x = event.pos[0] // TILE_SIZE
            target_y = event.pos[1] // TILE_SIZE

            start_tile = grid.get_tile(*player.state.pos)
            target_tile = grid.get_tile(target_x, target_y)
            if start_tile is None or target_tile is None:
                return
            if (target_x, target_y) == enemy.state.pos:
                return

            reachable = get_reachable_tiles(grid, start_tile, player.config.move)
            reachable_positions = {(tile.x, tile.y) for tile in reachable}
            if (target_x, target_y) not in reachable_positions:
                return

            player.move_to(target_x, target_y)
            turn_manager.mark_acted(player)
            return


def handle_enemy_turn(
    grid: Grid,
    enemy: Unit,
    units: list[Unit],
    player: Unit,
    turn_manager: TurnManager,
) -> None:
    if enemy.state.acted or not enemy.state.alive:
        return

    action, target = choose_enemy_action(enemy, grid, units)
    if action == "attack" and isinstance(target, Unit):
        damage = calculate_damage(enemy, target, terrain_bonus=0)
        target.take_damage(damage)
    elif action == "move" and target is not None:
        enemy.move_to(target.x, target.y)

    turn_manager.mark_acted(enemy)


def is_in_attack_range(attacker: Unit, defender: Unit) -> bool:
    ax, ay = attacker.state.pos
    dx, dy = defender.state.pos
    distance = abs(ax - dx) + abs(ay - dy)
    return attacker.config.range_min <= distance <= attacker.config.range_max


if __name__ == "__main__":
    main()
