"""UI 系统模块：负责 UI Panel、ActionMenu、单位信息和战斗日志渲染。"""

from __future__ import annotations

from typing import Callable

import pygame

from game.entity.unit import Unit
from game.ui.action_menu import ActionMenu
from game.ui.battle_log import BattleLog
from game.ui.battle_log_panel import BattleLogPanel
from game.ui.unit_info_panel import UnitInfoPanel


class UISystem:
    """Render all UI-layer elements for the battle scene."""

    def __init__(
        self,
        screen: pygame.Surface,
        ui_panel_rect: pygame.Rect,
        unit_info_rect: pygame.Rect,
        action_panel_rect: pygame.Rect,
        log_panel_rect: pygame.Rect,
        action_menu: ActionMenu,
        selected_unit_provider: Callable[[], Unit | None],
        battle_log: BattleLog,
        panel_bg_color: tuple[int, int, int] = (232, 236, 242),
        panel_border_color: tuple[int, int, int] = (160, 170, 185),
    ) -> None:
        self.screen = screen
        self.ui_panel_rect = ui_panel_rect
        self.unit_info_rect = unit_info_rect
        self.action_panel_rect = action_panel_rect
        self.log_panel_rect = log_panel_rect
        self.action_menu = action_menu
        self.selected_unit_provider = selected_unit_provider
        self.battle_log = battle_log
        self.panel_bg_color = panel_bg_color
        self.panel_border_color = panel_border_color

        self.unit_info_panel = UnitInfoPanel(screen, unit_info_rect)
        self.battle_log_panel = BattleLogPanel(
            screen=self.screen,
            battle_log=self.battle_log,
        )

    def update_layout(
        self,
        screen: pygame.Surface,
        ui_panel_rect: pygame.Rect,
        unit_info_rect: pygame.Rect,
        action_panel_rect: pygame.Rect,
        log_panel_rect: pygame.Rect,
    ) -> None:
        # 中文注释：窗口大小变化后更新 UI 各分区矩形与引用。
        self.screen = screen
        self.ui_panel_rect = ui_panel_rect
        self.unit_info_rect = unit_info_rect
        self.action_panel_rect = action_panel_rect
        self.log_panel_rect = log_panel_rect

        self.unit_info_panel.screen = screen
        self.unit_info_panel.panel_rect = unit_info_rect
        self.battle_log_panel.screen = screen

    def render(self, units: list[object], current_camp: str) -> None:
        """绘制区域2/3/4：UnitInfo、ActionMenu、BattleLog。"""
        # 中文注释：区域2+3（底部）背景与边框。
        pygame.draw.rect(self.screen, self.panel_bg_color, self.ui_panel_rect)
        pygame.draw.rect(self.screen, self.panel_border_color, self.ui_panel_rect, width=2)
        pygame.draw.rect(self.screen, self.panel_border_color, self.unit_info_rect, width=1)
        pygame.draw.rect(self.screen, self.panel_border_color, self.action_panel_rect, width=1)

        # 中文注释：区域4（最右侧日志列）独立渲染，不再占用区域3空间。
        pygame.draw.rect(self.screen, (222, 229, 238), self.log_panel_rect)
        pygame.draw.rect(self.screen, self.panel_border_color, self.log_panel_rect, width=2)

        selected_unit = self.selected_unit_provider()
        self.unit_info_panel.render(selected_unit)
        self.action_menu.draw(self.screen)

        log_content_rect = self.log_panel_rect.inflate(-12, -12)
        self.battle_log_panel.render(log_content_rect)
