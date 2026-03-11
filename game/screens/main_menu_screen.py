"""主菜单屏幕：进入关卡选择或退出游戏。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.screens.screen_base import ScreenBase
from game.ui.font_manager import get_font
from game.ui.language_shortcut import handle_language_toggle

BUTTON_WIDTH = 280
BUTTON_HEIGHT = 52
BUTTON_GAP = 18
BUTTON_BG = (64, 78, 98)
BUTTON_HOVER_BG = (86, 104, 130)
BUTTON_BORDER = (188, 198, 216)
BUTTON_TEXT = (240, 244, 252)


class MainMenuScreen(ScreenBase):
    """主菜单 Screen。"""

    def __init__(self, manager: object) -> None:
        super().__init__(manager)
        self.title_font = get_font(64)
        self.text_font = get_font(34)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.running = False
                return
            if event.type == pygame.VIDEORESIZE:
                self.manager.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                continue
            if event.type == getattr(pygame, "WINDOWSIZECHANGED", -1):
                self.manager.screen = pygame.display.set_mode((event.x, event.y), pygame.RESIZABLE)
                continue
            if handle_language_toggle(event):
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_rect, quit_rect = self._get_button_rects()
                if start_rect.collidepoint(event.pos):
                    self._start_game()
                    return
                if quit_rect.collidepoint(event.pos):
                    self.manager.running = False
                    return

            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_game()
                return
            if event.key == pygame.K_ESCAPE:
                self.manager.running = False
                return

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        screen.fill((28, 35, 44))

        title_surface = self.title_font.render(texts.MAIN_MENU_TITLE, True, (230, 236, 245))
        screen.blit(title_surface, (80, 90))

        start_rect, quit_rect = self._get_button_rects()
        self._draw_button(screen, start_rect, texts.MAIN_MENU_START)
        self._draw_button(screen, quit_rect, texts.MAIN_MENU_QUIT)

        pygame.display.flip()

    def _start_game(self) -> None:
        """进入关卡选择界面。"""
        from game.screens.level_select_screen import LevelSelectScreen

        self.manager.switch_to(LevelSelectScreen(self.manager))

    def _get_button_rects(self) -> tuple[pygame.Rect, pygame.Rect]:
        """根据当前窗口尺寸计算主菜单按钮区域。"""
        screen = self.manager.screen
        base_x = 80
        base_y = 200
        start_rect = pygame.Rect(base_x, base_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        quit_rect = pygame.Rect(base_x, base_y + BUTTON_HEIGHT + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
        return start_rect, quit_rect

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str) -> None:
        """绘制主菜单按钮并处理悬停高亮。"""
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        bg_color = BUTTON_HOVER_BG if hovered else BUTTON_BG
        pygame.draw.rect(screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_BORDER, rect, width=2, border_radius=10)

        text_surface = self.text_font.render(label, True, BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
