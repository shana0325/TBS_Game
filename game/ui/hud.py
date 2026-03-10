"""HUD rendering helpers for pygame battle view."""

from __future__ import annotations

import pygame

from game.entity.unit import Unit

TEXT_COLOR = (20, 20, 20)
FONT_SIZE = 24
LINE_SPACING = 28


def render_hud(
    screen: pygame.Surface,
    units: list[Unit],
    current_turn: str,
    panel_rect: pygame.Rect | None = None,
) -> None:
    """Render current turn and HP summary text."""
    font = pygame.font.Font(None, FONT_SIZE)

    player_hp = _sum_team_hp(units, team_id=1)
    enemy_hp = _sum_team_hp(units, team_id=2)

    turn_label = "Player" if current_turn.lower() == "player" else "Enemy"
    lines = [
        f"Turn: {turn_label}",
        f"Player HP: {player_hp}",
        f"Enemy HP: {enemy_hp}",
    ]

    if panel_rect is None:
        base_x, base_y = 8, 8
    else:
        # 中文注释：将 HUD 固定绘制在底部 UI Panel 的右侧区域。
        base_x = panel_rect.x + 180
        base_y = panel_rect.y + 20

    for index, text in enumerate(lines):
        surface = font.render(text, True, TEXT_COLOR)
        screen.blit(surface, (base_x, base_y + index * LINE_SPACING))


def _sum_team_hp(units: list[Unit], team_id: int) -> int:
    return sum(unit.state.hp for unit in units if unit.state.alive and unit.state.team_id == team_id)
