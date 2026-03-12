"""成长属性面板：负责属性页的渲染与点击处理。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.ui.scrollable_list import ScrollableList

STAT_LINE_HEIGHT = 36


class ProgressionStatPanel:
    """属性页面板。"""

    def __init__(self, text_font: pygame.font.Font, small_font: pygame.font.Font) -> None:
        self.text_font = text_font
        self.small_font = small_font
        self.scroller = ScrollableList(item_height=STAT_LINE_HEIGHT)

    def render(self, screen: pygame.Surface, rect: pygame.Rect, entries: list[dict[str, object]]) -> None:
        start, end = self.scroller.get_visible_slice(len(entries), rect)
        for draw_index, entry in enumerate(entries[start:end]):
            line_y = rect.y + draw_index * STAT_LINE_HEIGHT
            if entry["kind"] == "spacer":
                continue
            surface = self.text_font.render(str(entry["text"]), True, (230, 236, 245))
            screen.blit(surface, (rect.x + 4, line_y))
            stat_name = entry.get("stat_name")
            if isinstance(stat_name, str):
                self._draw_button(screen, self.get_stat_button_rect(rect, draw_index), "+")
        self.scroller.draw_scrollbar(screen, rect, len(entries))

    def handle_scroll(self, event: pygame.event.Event, rect: pygame.Rect, entries: list[dict[str, object]]) -> None:
        self.scroller.handle_event(event, rect, len(entries))

    def handle_click(self, pos: tuple[int, int], rect: pygame.Rect, entries: list[dict[str, object]]) -> str | None:
        start, end = self.scroller.get_visible_slice(len(entries), rect)
        for draw_index, entry in enumerate(entries[start:end]):
            stat_name = entry.get("stat_name")
            if isinstance(stat_name, str) and self.get_stat_button_rect(rect, draw_index).collidepoint(pos):
                return stat_name
        return None

    def ensure_visible(self, index: int, total: int, rect: pygame.Rect) -> None:
        self.scroller.ensure_visible(index, total, rect)

    def get_stat_button_rect(self, rect: pygame.Rect, draw_index: int) -> pygame.Rect:
        return pygame.Rect(rect.right - 44, rect.y + draw_index * STAT_LINE_HEIGHT + 2, 36, 28)

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str) -> None:
        pygame.draw.rect(screen, (78, 92, 112), rect, border_radius=8)
        pygame.draw.rect(screen, (180, 194, 218), rect, width=1, border_radius=8)
        text_surface = self.small_font.render(label, True, (240, 244, 252))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
