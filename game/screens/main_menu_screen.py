"""主菜单屏幕：进入关卡选择或退出游戏。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.screens.screen_base import ScreenBase
from game.ui.font_manager import get_font
from game.ui.language_shortcut import handle_language_toggle


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
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from game.screens.level_select_screen import LevelSelectScreen

                self.manager.switch_to(LevelSelectScreen(self.manager))
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
        start_surface = self.text_font.render(texts.MAIN_MENU_START, True, (180, 210, 255))
        quit_surface = self.text_font.render(texts.MAIN_MENU_QUIT, True, (220, 180, 180))

        screen.blit(title_surface, (80, 90))
        screen.blit(start_surface, (80, 190))
        screen.blit(quit_surface, (80, 235))

        pygame.display.flip()


