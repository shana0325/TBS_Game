"""UI 系统模块：负责 UI Panel、HUD 和 ActionMenu 的渲染。"""

from __future__ import annotations

import pygame

from game.ui.action_menu import ActionMenu
from game.ui.hud import render_hud


class UISystem:
    """Render all UI-layer elements for the battle scene."""

    def __init__(
        self,
        screen: pygame.Surface,
        ui_panel_rect: pygame.Rect,
        action_menu: ActionMenu,
        panel_bg_color: tuple[int, int, int] = (232, 236, 242),
        panel_border_color: tuple[int, int, int] = (160, 170, 185),
    ) -> None:
        self.screen = screen
        self.ui_panel_rect = ui_panel_rect
        self.action_menu = action_menu
        self.panel_bg_color = panel_bg_color
        self.panel_border_color = panel_border_color

    def render(self, units: list[object], current_camp: str) -> None:
        """绘制 UI Panel、HUD 和 ActionMenu。"""
        # 中文注释：先绘制面板底色与边框，再绘制 HUD 和行动菜单。
        pygame.draw.rect(self.screen, self.panel_bg_color, self.ui_panel_rect)
        pygame.draw.rect(self.screen, self.panel_border_color, self.ui_panel_rect, width=2)

        render_hud(self.screen, units, current_camp, self.ui_panel_rect)
        self.action_menu.draw(self.screen)
