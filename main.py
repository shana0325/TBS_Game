"""项目入口：初始化 pygame 并驱动 ScreenManager 主循环。"""

from __future__ import annotations

import os

import pygame

from game.core import texts
from game.core.game import WINDOW_HEIGHT, WINDOW_WIDTH
from game.screens.main_menu_screen import MainMenuScreen
from game.screens.screen_manager import ScreenManager

FPS = 60


def main() -> None:
    """启动游戏并运行 Screen 主循环。"""
    texts.set_language(os.getenv("TBS_LANG", "zh_cn"))
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(texts.WINDOW_TITLE)

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
