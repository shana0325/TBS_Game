"""国际化模块：集中管理当前语言与语言包访问。"""

from __future__ import annotations

from types import ModuleType

from . import en_us, zh_cn

_LANGUAGE_PACKS: dict[str, ModuleType] = {
    "zh_cn": zh_cn,
    "en_us": en_us,
}
_current_language = "zh_cn"


def get_language() -> str:
    """返回当前语言代码。"""
    return _current_language


def set_language(language_code: str) -> str:
    """设置当前语言；无效值时回退到中文。"""
    global _current_language
    _current_language = language_code if language_code in _LANGUAGE_PACKS else "zh_cn"
    return _current_language


def toggle_language() -> str:
    """在中英文之间切换。"""
    return set_language("en_us" if _current_language == "zh_cn" else "zh_cn")


def get_locale_module() -> ModuleType:
    """返回当前语言包模块。"""
    return _LANGUAGE_PACKS[get_language()]


def available_languages() -> tuple[str, ...]:
    """返回支持的语言列表。"""
    return tuple(_LANGUAGE_PACKS.keys())

