"""关卡选择屏幕：选择场景并进入部署阶段。"""

from __future__ import annotations

import pygame

from game.screens.screen_base import ScreenBase


class LevelSelectScreen(ScreenBase):
    """关卡选择 Screen。"""

    def __init__(self, manager: object) -> None:
        super().__init__(manager)
        self.title_font = pygame.font.Font(None, 56)
        self.text_font = pygame.font.Font(None, 32)
        # 中文注释：当前仅提供一个场景入口，后续可扩展为列表。
        self.selected_level = "level_1"
        self.selected_scenario = "scenario_1"

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.running = False
                return
            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from game.screens.deployment_screen import DeploymentScreen

                self.manager.switch_to(
                    DeploymentScreen(
                        manager=self.manager,
                        level_name=self.selected_level,
                        scenario_name=self.selected_scenario,
                    )
                )
                return

            if event.key == pygame.K_ESCAPE:
                from game.screens.main_menu_screen import MainMenuScreen

                self.manager.switch_to(MainMenuScreen(self.manager))
                return

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        screen.fill((24, 30, 38))

        title_surface = self.title_font.render("Level Select", True, (230, 236, 245))
        info_surface = self.text_font.render("Scenario 1 (level_1)", True, (190, 220, 255))
        start_surface = self.text_font.render("Enter: Deployment", True, (170, 230, 180))
        back_surface = self.text_font.render("ESC: Back", True, (220, 180, 180))

        screen.blit(title_surface, (80, 80))
        screen.blit(info_surface, (80, 170))
        screen.blit(start_surface, (80, 220))
        screen.blit(back_surface, (80, 260))

        pygame.display.flip()
