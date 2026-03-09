"""HUD rendering helpers for pygame battle view."""

from __future__ import annotations

import pygame

from game.entity.unit import Unit

TEXT_COLOR = (20, 20, 20)
FONT_SIZE = 24
HUD_X = 8
HUD_Y = 8
LINE_SPACING = 28


def render_hud(screen: pygame.Surface, units: list[Unit], current_turn: str) -> None:
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

    for index, text in enumerate(lines):
        surface = font.render(text, True, TEXT_COLOR)
        screen.blit(surface, (HUD_X, HUD_Y + index * LINE_SPACING))


def _sum_team_hp(units: list[Unit], team_id: int) -> int:
    return sum(unit.state.hp for unit in units if unit.state.alive and unit.state.team_id == team_id)
