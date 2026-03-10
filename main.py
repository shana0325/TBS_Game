"""项目入口：初始化 pygame 并驱动 Game 主循环。"""

from __future__ import annotations

import pygame

from game.core.game import Game

FPS = 60


def main() -> None:
    """启动游戏并运行主循环。"""
    pygame.init()

    clock = pygame.time.Clock()
    game = Game()

    while game.running:
        game.handle_events()
        game.update()
        game.render()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
