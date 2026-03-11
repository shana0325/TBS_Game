"""统一字体模块：集中管理游戏内所有 pygame 字体加载。"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pygame

# 中文注释：默认字体文件统一放在 assets/fonts 下，后续替换字体只需修改这里。
_DEFAULT_FONT_PATH = Path(__file__).resolve().parents[2] / "assets" / "fonts" / "LXGWWenKai-Light.ttf"


def get_font_path() -> str | None:
    """返回当前字体文件路径；缺失时回退到 pygame 默认字体。"""
    if _DEFAULT_FONT_PATH.exists():
        return str(_DEFAULT_FONT_PATH)
    return None


@lru_cache(maxsize=32)
def get_font(size: int) -> pygame.font.Font:
    """按字号获取统一字体实例，并缓存复用。"""
    return pygame.font.Font(get_font_path(), size)


def clear_font_cache() -> None:
    """清理字体缓存；当未来切换字体文件时可调用。"""
    get_font.cache_clear()
