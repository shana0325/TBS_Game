"""Rendering helpers for movement range highlights."""

from __future__ import annotations

import pygame

from game.battle.movement.tile import Tile

HIGHLIGHT_COLOR = (60, 120, 255)
HIGHLIGHT_WIDTH = 2


def draw_move_highlights(
    screen: pygame.Surface,
    tiles: list[Tile],
    tile_size: int,
    origin: tuple[int, int] = (0, 0),
) -> None:
    """Draw blue outline highlights for reachable tiles."""
    ox, oy = origin
    for tile in tiles:
        rect = pygame.Rect(ox + tile.x * tile_size, oy + tile.y * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, width=HIGHLIGHT_WIDTH)
