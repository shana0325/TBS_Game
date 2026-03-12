"""关卡选择屏幕：选择场景并进入部署阶段。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.screens.screen_base import ScreenBase
from game.ui.font_manager import get_font
from game.ui.language_shortcut import handle_language_toggle

BUTTON_WIDTH = 320
BUTTON_HEIGHT = 50
BUTTON_GAP = 16
BUTTON_BG = (62, 76, 94)
BUTTON_HOVER_BG = (86, 103, 128)
BUTTON_BORDER = (184, 196, 214)
BUTTON_TEXT = (240, 244, 252)
INFO_BG = (44, 56, 72)
INFO_BORDER = (118, 146, 182)


class LevelSelectScreen(ScreenBase):
    """关卡选择 Screen。"""

    def __init__(self, manager: object) -> None:
        super().__init__(manager)
        self.title_font = get_font(56)
        self.text_font = get_font(32)
        self.info_font = get_font(28)
        self.selected_level = "level_1"
        self.selected_scenario = "scenario_1"

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
                deployment_rect, progression_rect, back_rect = self._get_button_rects()
                if deployment_rect.collidepoint(event.pos):
                    self._open_deployment()
                    return
                if progression_rect.collidepoint(event.pos):
                    self._open_progression()
                    return
                if back_rect.collidepoint(event.pos):
                    self._back_to_main_menu()
                    return

            if event.type != pygame.KEYDOWN:
                continue

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._open_deployment()
                return

            if event.key == pygame.K_p:
                self._open_progression()
                return

            if event.key == pygame.K_ESCAPE:
                self._back_to_main_menu()
                return

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        screen.fill((24, 30, 38))

        title_surface = self.title_font.render(texts.LEVEL_SELECT_TITLE, True, (230, 236, 245))
        screen.blit(title_surface, (80, 80))

        self._draw_scenario_info(screen)
        deployment_rect, progression_rect, back_rect = self._get_button_rects()
        self._draw_button(screen, deployment_rect, texts.LEVEL_SELECT_DEPLOYMENT, (170, 230, 180))
        self._draw_button(screen, progression_rect, texts.LEVEL_SELECT_PROGRESSION, (230, 210, 160))
        self._draw_button(screen, back_rect, texts.LEVEL_SELECT_BACK, (220, 180, 180))

        pygame.display.flip()

    def _open_deployment(self) -> None:
        """进入部署界面。"""
        from game.screens.deployment_screen import DeploymentScreen

        self.manager.switch_to(
            DeploymentScreen(
                manager=self.manager,
                level_name=self.selected_level,
                scenario_name=self.selected_scenario,
            )
        )

    def _open_progression(self) -> None:
        """进入成长界面。"""
        from game.screens.progression_character_select_screen import ProgressionCharacterSelectScreen

        self.manager.switch_to(ProgressionCharacterSelectScreen(self.manager, return_screen=self))

    def _back_to_main_menu(self) -> None:
        """返回主菜单。"""
        from game.screens.main_menu_screen import MainMenuScreen

        self.manager.switch_to(MainMenuScreen(self.manager))

    def _draw_scenario_info(self, screen: pygame.Surface) -> None:
        """绘制当前场景信息卡片。"""
        info_rect = pygame.Rect(80, 165, 360, 56)
        pygame.draw.rect(screen, INFO_BG, info_rect, border_radius=10)
        pygame.draw.rect(screen, INFO_BORDER, info_rect, width=2, border_radius=10)
        info_surface = self.info_font.render(texts.LEVEL_SELECT_SCENARIO, True, (190, 220, 255))
        info_rect_text = info_surface.get_rect(center=info_rect.center)
        screen.blit(info_surface, info_rect_text)

    def _get_button_rects(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        """根据当前窗口尺寸计算关卡选择按钮区域。"""
        base_x = 80
        base_y = 245
        deployment_rect = pygame.Rect(base_x, base_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        progression_rect = pygame.Rect(base_x, base_y + BUTTON_HEIGHT + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
        back_rect = pygame.Rect(base_x, base_y + (BUTTON_HEIGHT + BUTTON_GAP) * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        return deployment_rect, progression_rect, back_rect

    def _draw_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        label: str,
        text_color: tuple[int, int, int],
    ) -> None:
        """绘制关卡选择按钮。"""
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        bg_color = BUTTON_HOVER_BG if hovered else BUTTON_BG
        pygame.draw.rect(screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(screen, BUTTON_BORDER, rect, width=2, border_radius=10)

        text_surface = self.text_font.render(label, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
