"""屏幕基类模块：定义所有 Screen 的统一接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ScreenBase(ABC):
    """Screen 抽象基类。"""

    def __init__(self, manager: object) -> None:
        self.manager = manager

    @abstractmethod
    def handle_input(self) -> None:
        """处理输入事件。"""

    @abstractmethod
    def update(self) -> None:
        """更新逻辑。"""

    @abstractmethod
    def render(self) -> None:
        """渲染当前画面。"""
