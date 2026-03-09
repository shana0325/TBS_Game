"""Pygame map rendering helpers."""

from __future__ import annotations

import pygame

from game.battle.movement.grid import Grid
from game.entity.unit import Unit

TILE_SIZE = 40

GRID_LINE_COLOR = (200, 200, 200)
PLAYER_COLOR = (60, 120, 255)
ENEMY_COLOR = (220, 70, 70)


def render_map(screen: pygame.Surface, grid: Grid, units: list[Unit]) -> None:
    """Render the tile grid and unit blocks."""
    _draw_grid(screen, grid)
    _draw_units(screen, grid, units)


def _draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    for y in range(grid.height):
        for x in range(grid.width):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRID_LINE_COLOR, rect, width=1)


def _draw_units(screen: pygame.Surface, grid: Grid, units: list[Unit]) -> None:
    for unit in units:
        if not unit.state.alive:
            continue

        x, y = unit.state.pos
        if x < 0 or y < 0 or x >= grid.width or y >= grid.height:
            continue

        color = PLAYER_COLOR if unit.state.team_id == 1 else ENEMY_COLOR
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect)
