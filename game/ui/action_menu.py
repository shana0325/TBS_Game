"""行动菜单模块：负责在界面上绘制并检测 Move/Attack/Skill/Wait 菜单点击。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.ui.font_manager import get_font

MENU_BG_COLOR = (250, 250, 250)
MENU_BORDER_COLOR = (80, 80, 80)
MENU_TEXT_COLOR = (20, 20, 20)
MENU_HOVER_COLOR = (225, 235, 255)
MENU_TITLE_COLOR = (40, 40, 40)


class ActionMenu:
    """Simple action menu for selected unit."""

    COMMANDS = ("move", "attack", "skill", "wait")

    def __init__(
        self,
        x: int = 8,
        y: int = 96,
        width: int = 220,
        item_height: int = 42,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.item_height = item_height
        self.visible = False
        self._font: pygame.font.Font | None = None
        self._title_font: pygame.font.Font | None = None

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def set_anchor(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return

        if self._font is None:
            self._font = get_font(28)
        if self._title_font is None:
            self._title_font = get_font(30)

        title_surface = self._title_font.render(texts.ACTION_MENU_TITLE, True, MENU_TITLE_COLOR)
        screen.blit(title_surface, (self.x, self.y - 34))

        mouse_pos = pygame.mouse.get_pos()
        for index, label in enumerate(self._get_labels()):
            rect = self._item_rect(index)
            bg_color = MENU_HOVER_COLOR if rect.collidepoint(mouse_pos) else MENU_BG_COLOR
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, MENU_BORDER_COLOR, rect, width=1)

            text_surface = self._font.render(label, True, MENU_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def get_option_at_pos(self, pos: tuple[int, int]) -> str | None:
        if not self.visible:
            return None

        for index, _label in enumerate(self._get_labels()):
            if self._item_rect(index).collidepoint(pos):
                return self.COMMANDS[index]
        return None

    def _item_rect(self, index: int) -> pygame.Rect:
        return pygame.Rect(self.x, self.y + index * self.item_height, self.width, self.item_height)

    def _get_labels(self) -> list[str]:
        """按当前语言返回行动菜单显示文本。"""
        return list(texts.ACTION_MENU_OPTIONS)
