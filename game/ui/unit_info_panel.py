"""单位信息面板模块：负责绘制选中单位属性。"""

from __future__ import annotations

import pygame

TITLE_COLOR = (35, 35, 35)
TEXT_COLOR = (30, 30, 30)


class UnitInfoPanel:
    """Render selected unit details in the bottom-left panel."""

    def __init__(self, screen: pygame.Surface, panel_rect: pygame.Rect) -> None:
        self.screen = screen
        self.panel_rect = panel_rect
        self._title_font: pygame.font.Font | None = None
        self._text_font: pygame.font.Font | None = None

    def render(self, unit: object | None) -> None:
        """Render selected unit stats, or placeholder when none selected."""
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, 30)
        if self._text_font is None:
            self._text_font = pygame.font.Font(None, 26)

        self._draw_text("Unit Info", self._title_font, self.panel_rect.x + 16, self.panel_rect.y + 12, TITLE_COLOR)

        if unit is None:
            self._draw_text("No unit selected", self._text_font, self.panel_rect.x + 16, self.panel_rect.y + 54, TEXT_COLOR)
            return

        name = getattr(unit, "name", None) or "Unit"
        lines = [
            f"{name}",
            f"HP: {unit.state.hp}/{unit.config.hp}",
            f"ATK: {unit.config.atk}",
            f"DEF: {unit.config.defense}",
            f"Move: {unit.config.move}",
            f"Range: {unit.config.range_min}-{unit.config.range_max}",
        ]

        base_x = self.panel_rect.x + 16
        base_y = self.panel_rect.y + 50
        for idx, line in enumerate(lines):
            self._draw_text(line, self._text_font, base_x, base_y + idx * 26, TEXT_COLOR)

    def _draw_text(self, text: str, font: pygame.font.Font, x: int, y: int, color: tuple[int, int, int]) -> None:
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
