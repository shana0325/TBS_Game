"""攻击范围高亮渲染模块：负责绘制单位可攻击格子的红色边框。"""

from __future__ import annotations

import pygame

from game.battle.movement.tile import Tile

ATTACK_HIGHLIGHT_COLOR = (230, 70, 70)
ATTACK_HIGHLIGHT_WIDTH = 2


def draw_attack_highlights(screen: pygame.Surface, tiles: list[Tile], tile_size: int) -> None:
    """绘制攻击范围高亮：将可攻击格子用红色边框标出。"""
    for tile in tiles:
        rect = pygame.Rect(tile.x * tile_size, tile.y * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, ATTACK_HIGHLIGHT_COLOR, rect, width=ATTACK_HIGHLIGHT_WIDTH)
