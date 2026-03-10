"""项目入口：初始化 pygame 并驱动 ScreenManager 主循环。"""

from __future__ import annotations

import pygame

from game.core.game import BOTTOM_PANEL_HEIGHT, BATTLEFIELD_AREA_HEIGHT, WINDOW_WIDTH
from game.screens.main_menu_screen import MainMenuScreen
from game.screens.screen_manager import ScreenManager

FPS = 60
WINDOW_HEIGHT = BATTLEFIELD_AREA_HEIGHT + BOTTOM_PANEL_HEIGHT


def main() -> None:
    """启动游戏并运行 Screen 主循环。"""
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TBS Game")

    clock = pygame.time.Clock()
    manager = ScreenManager(screen)
    manager.switch_to(MainMenuScreen(manager))

    while manager.running:
        manager.handle_input()
        manager.update()
        manager.render()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
