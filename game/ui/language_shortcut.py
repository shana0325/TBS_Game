"""语言切换快捷键模块：统一处理运行中的语言切换。"""

from __future__ import annotations

import pygame

from game.core import texts


def handle_language_toggle(event: pygame.event.Event) -> bool:
    """处理 F2 语言切换；返回 True 表示事件已消费。"""
    if event.type != pygame.KEYDOWN or event.key != pygame.K_F2:
        return False

    texts.toggle_language()
    pygame.display.set_caption(texts.WINDOW_TITLE)
    return True
