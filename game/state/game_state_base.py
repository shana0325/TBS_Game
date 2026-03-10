"""状态基类模块：定义玩家状态处理接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class GameStateBase(ABC):
    """Base class for player turn states."""

    @abstractmethod
    def handle_input(
        self,
        game: object,
        events: list[pygame.event.Event],
        battlefield_rect: pygame.Rect,
    ) -> "GameStateBase":
        """Handle one frame input and return next state object."""
        raise NotImplementedError
