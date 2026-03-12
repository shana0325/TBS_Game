"""Pygame map rendering helpers."""

from __future__ import annotations

from pathlib import Path

import pygame

from game.entity.unit import Unit

TILE_SIZE = 40

GRID_LINE_COLOR = (200, 200, 200)
PLAYER_GRID_BORDER_COLOR = (70, 120, 255)
ENEMY_GRID_BORDER_COLOR = (230, 80, 80)
GAP_BG_COLOR = (238, 242, 248)
PLAYER_COLOR = (60, 120, 255)
ENEMY_COLOR = (220, 70, 70)
SPRITE_PADDING = 4

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_UNIT_ASSET_DIR = _PROJECT_ROOT / "assets" / "units"
_SPRITE_CACHE: dict[tuple[str, int], pygame.Surface] = {}


def render_map(
    screen: pygame.Surface,
    grid: object,
    units: list[Unit],
    battlefield_rect: pygame.Rect,
    origin: tuple[int, int],
    tile_size: int = TILE_SIZE,
) -> None:
    """Render battlefield background, separated grids, and unit blocks."""
    _draw_battlefield_zones(screen, grid, battlefield_rect, origin, tile_size)
    _draw_grid(screen, grid, origin, tile_size)
    _draw_units(screen, grid, units, origin, tile_size)


def _draw_battlefield_zones(
    screen: pygame.Surface,
    grid: object,
    battlefield_rect: pygame.Rect,
    origin: tuple[int, int],
    tile_size: int,
) -> None:
    ox, oy = origin

    # 中文注释：战场上方区域先铺底，之后突出两侧阵地和中间 gap。
    pygame.draw.rect(screen, (248, 250, 253), battlefield_rect)

    player_rect = pygame.Rect(
        ox + grid.player_offset_x * tile_size,
        oy,
        grid.side_width * tile_size,
        grid.height * tile_size,
    )
    enemy_rect = pygame.Rect(
        ox + grid.enemy_offset_x * tile_size,
        oy,
        grid.side_width * tile_size,
        grid.height * tile_size,
    )
    gap_rect = pygame.Rect(
        ox + grid.side_width * tile_size,
        oy,
        grid.gap_width * tile_size,
        grid.height * tile_size,
    )

    pygame.draw.rect(screen, GAP_BG_COLOR, gap_rect)
    pygame.draw.rect(screen, PLAYER_GRID_BORDER_COLOR, player_rect, width=3)
    pygame.draw.rect(screen, ENEMY_GRID_BORDER_COLOR, enemy_rect, width=3)


def _draw_grid(screen: pygame.Surface, grid: object, origin: tuple[int, int], tile_size: int) -> None:
    ox, oy = origin
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get_tile(x, y) is None:
                continue
            rect = pygame.Rect(ox + x * tile_size, oy + y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, GRID_LINE_COLOR, rect, width=1)


def _draw_units(
    screen: pygame.Surface,
    grid: object,
    units: list[Unit],
    origin: tuple[int, int],
    tile_size: int,
) -> None:
    ox, oy = origin
    for unit in units:
        if not unit.state.alive:
            continue

        x, y = unit.state.pos
        if grid.get_tile(x, y) is None:
            continue

        rect = pygame.Rect(ox + x * tile_size, oy + y * tile_size, tile_size, tile_size)
        sprite = _get_unit_sprite(unit, tile_size)
        if sprite is not None:
            screen.blit(sprite, rect.move(SPRITE_PADDING, SPRITE_PADDING))
            continue

        # 中文注释：贴图缺失时回退到原有色块逻辑，避免资源缺失导致单位不显示。
        color = PLAYER_COLOR if unit.state.team_id == 1 else ENEMY_COLOR
        pygame.draw.rect(screen, color, rect)


def _get_unit_sprite(unit: Unit, tile_size: int) -> pygame.Surface | None:
    unit_name = str(getattr(unit, "name", "")).strip().lower()
    if not unit_name:
        return None

    cache_key = (unit_name, tile_size)
    cached = _SPRITE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    sprite_path = _UNIT_ASSET_DIR / f"{unit_name}.png"
    if not sprite_path.exists():
        return None

    source = pygame.image.load(str(sprite_path)).convert_alpha()
    target_size = max(8, tile_size - SPRITE_PADDING * 2)
    scaled = pygame.transform.scale(source, (target_size, target_size))
    _SPRITE_CACHE[cache_key] = scaled
    return scaled
