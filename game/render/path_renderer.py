"""路径预览渲染模块：负责绘制单位移动路径可视化。"""

from __future__ import annotations

import pygame

from game.battle.movement.tile import Tile

PATH_COLOR = (70, 140, 255)
PATH_WIDTH = 3
NODE_RADIUS = 5


def draw_path_preview(
    screen: pygame.Surface,
    path: list[Tile],
    tile_size: int,
    origin: tuple[int, int] = (0, 0),
) -> None:
    """绘制路径预览：使用线段连接路径节点，并在节点绘制圆点。"""
    if not path:
        return

    ox, oy = origin
    centers = [
        (ox + tile.x * tile_size + tile_size // 2, oy + tile.y * tile_size + tile_size // 2)
        for tile in path
    ]

    if len(centers) >= 2:
        pygame.draw.lines(screen, PATH_COLOR, False, centers, PATH_WIDTH)

    for center in centers:
        pygame.draw.circle(screen, PATH_COLOR, center, NODE_RADIUS)
