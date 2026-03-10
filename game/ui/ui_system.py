"""UI 系统模块：负责 UI Panel、HUD 和 ActionMenu 的渲染。"""

from __future__ import annotations

from typing import Callable

import pygame

from game.entity.unit import Unit
from game.ui.action_menu import ActionMenu
from game.ui.hud import render_hud
from game.ui.unit_info_panel import UnitInfoPanel


class UISystem:
    """Render all UI-layer elements for the battle scene."""

    def __init__(
        self,
        screen: pygame.Surface,
        ui_panel_rect: pygame.Rect,
        unit_info_rect: pygame.Rect,
        action_panel_rect: pygame.Rect,
        action_menu: ActionMenu,
        selected_unit_provider: Callable[[], Unit | None],
        panel_bg_color: tuple[int, int, int] = (232, 236, 242),
        panel_border_color: tuple[int, int, int] = (160, 170, 185),
    ) -> None:
        self.screen = screen
        self.ui_panel_rect = ui_panel_rect
        self.unit_info_rect = unit_info_rect
        self.action_panel_rect = action_panel_rect
        self.action_menu = action_menu
        self.selected_unit_provider = selected_unit_provider
        self.panel_bg_color = panel_bg_color
        self.panel_border_color = panel_border_color
        self.unit_info_panel = UnitInfoPanel(screen, unit_info_rect)

    def render(self, units: list[object], current_camp: str) -> None:
        """绘制 UI Panel、HUD、Unit Info 与 ActionMenu。"""
        # 中文注释：底部总面板 + 左右分栏，保证 UI 不覆盖战场。
        pygame.draw.rect(self.screen, self.panel_bg_color, self.ui_panel_rect)
        pygame.draw.rect(self.screen, self.panel_border_color, self.ui_panel_rect, width=2)
        pygame.draw.rect(self.screen, self.panel_border_color, self.unit_info_rect, width=1)
        pygame.draw.rect(self.screen, self.panel_border_color, self.action_panel_rect, width=1)

        selected_unit = self.selected_unit_provider()
        self.unit_info_panel.render(selected_unit)

        # 中文注释：保留 HUD 接口兼容性；主要信息已由 Unit Info Panel 展示。
        # render_hud(self.screen, units, current_camp, self.action_panel_rect)
        self.action_menu.draw(self.screen)
