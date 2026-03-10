"""结算屏幕：显示战斗结果并支持返回菜单。"""

from __future__ import annotations

import pygame

from game.screens.screen_base import ScreenBase


class ResultScreen(ScreenBase):
    """战斗结果 Screen。"""

    def __init__(self, manager: object, result_text: str) -> None:
        super().__init__(manager)
        self.result_text = result_text
        self.title_font = pygame.font.Font(None, 60)
        self.text_font = pygame.font.Font(None, 32)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.running = False
                return
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from game.screens.main_menu_screen import MainMenuScreen

                self.manager.switch_to(MainMenuScreen(self.manager))
                return

            if event.key == pygame.K_ESCAPE:
                self.manager.running = False
                return

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        screen.fill((30, 30, 36))

        result_surface = self.title_font.render(self.result_text, True, (238, 232, 210))
        tip_surface = self.text_font.render("Enter: Main Menu   ESC: Quit", True, (190, 205, 230))

        screen.blit(result_surface, (80, 120))
        screen.blit(tip_surface, (80, 220))

        pygame.display.flip()
