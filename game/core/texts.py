"""统一文案入口：对外保持 texts.* 调用不变，并代理到当前语言包。"""

from __future__ import annotations

from game.core.i18n import available_languages as _available_languages
from game.core.i18n import get_language as _get_language
from game.core.i18n import get_locale_module, set_language as _set_language
from game.core.i18n import toggle_language as _toggle_language


def set_language(language_code: str) -> str:
    """设置当前语言。"""
    return _set_language(language_code)


def toggle_language() -> str:
    """在支持的语言之间切换。"""
    return _toggle_language()


def get_language() -> str:
    """返回当前语言代码。"""
    return _get_language()


def available_languages() -> tuple[str, ...]:
    """返回支持的语言列表。"""
    return _available_languages()


def get_skill_description(skill_id: str) -> str:
    """返回技能说明。"""
    return get_locale_module().get_skill_description(skill_id)


def get_buff_description(buff_id: str) -> str:
    """返回 Buff 说明。"""
    return get_locale_module().get_buff_description(buff_id)


def get_equipment_name(equipment_id: str) -> str:
    """返回装备显示名称。"""
    return get_locale_module().get_equipment_name(equipment_id)


def get_equipment_description(equipment_id: str) -> str:
    """返回装备说明。"""
    return get_locale_module().get_equipment_description(equipment_id)


def get_status_text(status_key: str) -> str:
    """返回状态文案。"""
    return get_locale_module().get_status_text(status_key)


def __getattr__(name: str) -> object:
    """兼容旧调用：按需代理当前语言包中的常量与函数。"""
    return getattr(get_locale_module(), name)
