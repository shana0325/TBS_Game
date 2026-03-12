"""成长页签栏：负责属性/技能/装备三个子页签的渲染与点击。"""

from __future__ import annotations

import pygame

from game.core import texts


class ProgressionTabs:
    """成长子页签组件。"""

    TABS = ("stats", "skills", "equipment")

    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def get_tab_labels(self) -> dict[str, str]:
        return {
            "stats": texts.PROGRESSION_TAB_STATS,
            "skills": texts.PROGRESSION_TAB_SKILLS,
            "equipment": texts.PROGRESSION_TAB_EQUIPMENT,
        }

    def get_tab_rects(self, rect: pygame.Rect) -> dict[str, pygame.Rect]:
        labels = self.get_tab_labels()
        width = (rect.width - 24) // 3
        result: dict[str, pygame.Rect] = {}
        x = rect.x + 8
        for tab_id in self.TABS:
            result[tab_id] = pygame.Rect(x, rect.y + 8, width, 40)
            x += width + 8
        return result

    def render(self, screen: pygame.Surface, rect: pygame.Rect, current_tab: str) -> None:
        labels = self.get_tab_labels()
        for tab_id, tab_rect in self.get_tab_rects(rect).items():
            selected = tab_id == current_tab
            bg = (88, 104, 132) if selected else (58, 66, 80)
            border = (188, 206, 228) if selected else (126, 142, 166)
            pygame.draw.rect(screen, bg, tab_rect, border_radius=8)
            pygame.draw.rect(screen, border, tab_rect, width=1, border_radius=8)
            text_surface = self.font.render(labels[tab_id], True, (236, 240, 248))
            text_rect = text_surface.get_rect(center=tab_rect.center)
            screen.blit(text_surface, text_rect)

    def get_clicked_tab(self, pos: tuple[int, int], rect: pygame.Rect) -> str | None:
        for tab_id, tab_rect in self.get_tab_rects(rect).items():
            if tab_rect.collidepoint(pos):
                return tab_id
        return None
