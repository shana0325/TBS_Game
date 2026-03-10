"""增益效果模块：执行 buff 类型效果。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.data.config_loader import ConfigLoader
from game.data.game_database import GameDatabase
from game.entity.buff import Buff

if TYPE_CHECKING:
    from game.entity.unit import Unit


class BuffEffect:
    """Buff 效果执行器。"""

    # 中文注释：Buff 模板数据通过 GameDatabase 统一访问。
    _config_loader = ConfigLoader()
    _game_db = GameDatabase(_config_loader)

    @classmethod
    def apply(cls, effect_data: dict[str, object], user: Unit, target: Unit) -> int:
        # 中文注释：优先按 buff id/name 读取模板，再用 effect_data 字段覆盖。
        _ = user
        template = cls._resolve_template(effect_data)

        buff_name = str(effect_data.get("name", template.get("name", effect_data.get("buff", "Buff"))))
        duration = int(effect_data.get("duration", template.get("duration", 1)))

        raw_modifiers = effect_data.get("modifiers", template.get("modifiers", {}))
        modifiers: dict[str, int] = {}
        if isinstance(raw_modifiers, dict):
            for key, value in raw_modifiers.items():
                modifiers[str(key)] = int(value)

        tick_damage = int(effect_data.get("tick_damage", template.get("tick_damage", 0)))
        tick_heal = int(effect_data.get("tick_heal", template.get("tick_heal", 0)))
        tick_phase = effect_data.get("tick_phase", template.get("tick_phase"))
        control = effect_data.get("control", template.get("control"))
        shield = int(effect_data.get("shield", template.get("shield", 0)))
        counter = bool(effect_data.get("counter", template.get("counter", False)))
        aura_range = int(effect_data.get("aura_range", template.get("aura_range", 0)))
        trigger = effect_data.get("trigger", template.get("trigger"))
        heal_percent = float(effect_data.get("heal_percent", template.get("heal_percent", 0.0)))

        buff = Buff(
            name=buff_name,
            duration=duration,
            modifiers=modifiers,
            tick_damage=max(0, tick_damage),
            tick_heal=max(0, tick_heal),
            tick_phase=str(tick_phase) if tick_phase is not None else None,
            control=str(control) if control is not None else None,
            shield=max(0, shield),
            counter=counter,
            aura_range=max(0, aura_range),
            trigger=str(trigger) if trigger is not None else None,
            heal_percent=max(0.0, heal_percent),
        )
        target.add_buff(buff)

        # 中文注释：Buff 类型效果当前不直接返回数值变化。
        return 0

    @classmethod
    def _resolve_template(cls, effect_data: dict[str, object]) -> dict[str, object]:
        buff_id = effect_data.get("buff")
        if buff_id is None:
            buff_id = effect_data.get("name")
        if buff_id is None:
            return {}

        buff_cfg = cls._game_db.get_buff(str(buff_id))
        if buff_cfg is None:
            return {}
        return buff_cfg
