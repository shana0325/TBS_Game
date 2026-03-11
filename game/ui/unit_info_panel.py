"""单位信息面板模块：负责绘制选中单位属性。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.ui.font_manager import get_font

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
        if self._title_font is None:
            self._title_font = get_font(30)
        if self._text_font is None:
            self._text_font = get_font(26)

        self._draw_text(texts.UNIT_INFO_TITLE, self._title_font, self.panel_rect.x + 16, self.panel_rect.y + 12, TITLE_COLOR)

        if unit is None:
            self._draw_text(texts.UNIT_INFO_NONE, self._text_font, self.panel_rect.x + 16, self.panel_rect.y + 54, TEXT_COLOR)
            return

        name = getattr(unit, "name", None) or "Unit"
        status_text = self._build_status_text(unit)
        buff_text = self._build_buff_text(unit)
        lines = [
            f"{name}",
            f"{texts.UNIT_INFO_HP}: {unit.state.hp}/{unit.config.hp}",
            f"{texts.UNIT_INFO_ATK}: {unit.config.atk}",
            f"{texts.UNIT_INFO_DEF}: {unit.config.defense}",
            f"{texts.UNIT_INFO_MOVE}: {unit.config.move}",
            f"{texts.UNIT_INFO_RANGE}: {unit.config.range_min}-{unit.config.range_max}",
            f"{texts.UNIT_INFO_STATUS}: {status_text}",
            f"{texts.UNIT_INFO_BUFFS}: {buff_text}",
        ]

        base_x = self.panel_rect.x + 16
        base_y = self.panel_rect.y + 50
        for idx, line in enumerate(lines):
            self._draw_text(line, self._text_font, base_x, base_y + idx * 26, TEXT_COLOR)

    def _build_status_text(self, unit: object) -> str:
        """构建单位当前状态文本。"""
        statuses: list[str] = []
        if getattr(unit.state, "acted", False):
            statuses.append(texts.get_status_text("acted"))
        if getattr(unit, "is_stunned", lambda: False)():
            statuses.append(texts.get_status_text("stun"))
        if getattr(unit, "is_silenced", lambda: False)():
            statuses.append(texts.get_status_text("silence"))
        if not statuses:
            statuses.append(texts.get_status_text("normal"))
        return " / ".join(statuses)

    def _build_buff_text(self, unit: object) -> str:
        """构建单位当前 Buff 摘要。"""
        buffs = getattr(unit, "buffs", [])
        if not buffs:
            return texts.PROGRESSION_NO_DESCRIPTION
        return " / ".join(texts.get_buff_name(getattr(buff, "name", "")) for buff in buffs[:2])

    def _draw_text(self, text: str, font: pygame.font.Font, x: int, y: int, color: tuple[int, int, int]) -> None:
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

