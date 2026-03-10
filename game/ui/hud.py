"""HUD rendering helpers for pygame battle view."""

from __future__ import annotations

import pygame


def render_hud(
    screen: pygame.Surface,
    units: list[object],
    current_turn: str,
    panel_rect: pygame.Rect | None = None,
) -> None:
    """HUD 文本已下线；保留接口以兼容现有调用。"""
    # 中文注释：当前 UI 信息由 Unit Info Panel 提供，此处不再绘制回合/HP 文本。
    return
