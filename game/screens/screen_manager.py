"""屏幕管理器模块：负责当前 Screen 的切换与驱动。"""

from __future__ import annotations

from game.screens.screen_base import ScreenBase


class ScreenManager:
    """管理当前屏幕并转发主循环调用。"""

    def __init__(self, screen: object) -> None:
        self.screen = screen
        self.current_screen: ScreenBase | None = None
        self.running = True

    def switch_to(self, screen: ScreenBase) -> None:
        # 中文注释：切换当前屏幕，后续主循环调用将转发到新屏幕。
        self.current_screen = screen

    def handle_input(self) -> None:
        if self.current_screen is None:
            return
        self.current_screen.handle_input()

    def update(self) -> None:
        if self.current_screen is None:
            return
        self.current_screen.update()

    def render(self) -> None:
        if self.current_screen is None:
            return
        self.current_screen.render()
