"""通用滚动列表组件：统一处理列表滚动状态、可视范围和滚动条绘制。"""

from __future__ import annotations

import pygame


class ScrollableList:
    """管理可滚动列表的状态与滚动条绘制。"""

    def __init__(
        self,
        item_height: int,
        wheel_step: int = 1,
        anchor: str = "top",
        track_color: tuple[int, int, int] = (82, 92, 108),
        thumb_color: tuple[int, int, int] = (180, 190, 210),
        scrollbar_width: int = 8,
        scrollbar_gap: int = 6,
    ) -> None:
        self.item_height = max(1, item_height)
        self.wheel_step = max(1, wheel_step)
        self.anchor = anchor
        self.track_color = track_color
        self.thumb_color = thumb_color
        self.scrollbar_width = max(4, scrollbar_width)
        self.scrollbar_gap = max(2, scrollbar_gap)
        self.scroll_index = 0

    def get_visible_count(self, view_rect: pygame.Rect) -> int:
        """根据显示区域高度计算当前可见条目数。"""
        return max(1, view_rect.height // self.item_height)

    def clamp(self, total_items: int, view_rect: pygame.Rect) -> None:
        """将滚动偏移限制在合法范围内。"""
        visible_count = self.get_visible_count(view_rect)
        max_scroll = max(0, total_items - visible_count)
        self.scroll_index = max(0, min(self.scroll_index, max_scroll))

    def handle_event(self, event: pygame.event.Event, hover_rect: pygame.Rect, total_items: int) -> None:
        """处理滚轮输入，仅在鼠标位于目标区域时生效。"""
        mouse_pos = pygame.mouse.get_pos()
        if not hover_rect.collidepoint(mouse_pos):
            return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_by(-event.y * self.wheel_step, total_items, hover_rect)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_by(-self.wheel_step, total_items, hover_rect)
            elif event.button == 5:
                self.scroll_by(self.wheel_step, total_items, hover_rect)

    def scroll_by(self, delta: int, total_items: int, view_rect: pygame.Rect) -> None:
        """按指定步长滚动，并自动夹紧范围。"""
        if delta == 0:
            return
        self.scroll_index += delta
        self.clamp(total_items, view_rect)

    def ensure_visible(self, index: int, total_items: int, view_rect: pygame.Rect) -> None:
        """确保指定条目位于当前可视窗口内。"""
        if total_items <= 0:
            self.scroll_index = 0
            return

        index = max(0, min(index, total_items - 1))
        visible_count = self.get_visible_count(view_rect)

        if self.anchor == "top":
            if index < self.scroll_index:
                self.scroll_index = index
            elif index >= self.scroll_index + visible_count:
                self.scroll_index = index - visible_count + 1
        else:
            start_index = self.get_start_index(total_items, view_rect)
            end_index = start_index + visible_count - 1
            if index < start_index:
                self.scroll_index = max(0, total_items - visible_count - index)
            elif index > end_index:
                self.scroll_index = max(0, total_items - visible_count - (index - visible_count + 1))

        self.clamp(total_items, view_rect)

    def get_start_index(self, total_items: int, view_rect: pygame.Rect) -> int:
        """返回当前可视区间起始下标。"""
        visible_count = self.get_visible_count(view_rect)
        self.clamp(total_items, view_rect)

        if self.anchor == "bottom":
            return max(0, total_items - visible_count - self.scroll_index)
        return self.scroll_index

    def get_visible_slice(self, total_items: int, view_rect: pygame.Rect) -> tuple[int, int]:
        """返回当前需要绘制的切片范围。"""
        start = self.get_start_index(total_items, view_rect)
        end = min(total_items, start + self.get_visible_count(view_rect))
        return start, end

    def draw_scrollbar(self, screen: pygame.Surface, view_rect: pygame.Rect, total_items: int) -> None:
        """当内容超出时绘制统一风格的滚动条。"""
        visible_count = self.get_visible_count(view_rect)
        if total_items <= visible_count:
            return

        track_rect = pygame.Rect(
            view_rect.right + self.scrollbar_gap,
            view_rect.y,
            self.scrollbar_width,
            view_rect.height,
        )
        pygame.draw.rect(screen, self.track_color, track_rect, border_radius=self.scrollbar_width // 2)

        thumb_height = max(24, int(track_rect.height * (visible_count / total_items)))
        max_start = max(1, total_items - visible_count)
        start_index = self.get_start_index(total_items, view_rect)
        thumb_y = track_rect.y + int((track_rect.height - thumb_height) * (start_index / max_start))
        thumb_rect = pygame.Rect(track_rect.x, thumb_y, track_rect.width, thumb_height)
        pygame.draw.rect(screen, self.thumb_color, thumb_rect, border_radius=self.scrollbar_width // 2)
