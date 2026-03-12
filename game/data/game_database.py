"""游戏数据库模块：统一管理并提供配置访问接口。"""

from __future__ import annotations

from game.data.config_loader import ConfigLoader


class GameDatabase:
    """Wrap loaded config dictionaries and expose unified getters."""

    def __init__(self, loader: ConfigLoader) -> None:
        # 中文注释：直接引用 loader 已加载的数据，避免重复读取文件。
        self.units = loader.units
        self.skills = loader.skills
        self.buffs = loader.buffs
        self.equipments = loader.equipments

    def get_unit(self, unit_id: str) -> dict[str, object] | None:
        return self.units.get(unit_id)

    def get_skill(self, skill_id: str) -> dict[str, object] | None:
        return self.skills.get(skill_id)

    def get_buff(self, buff_id: str) -> dict[str, object] | None:
        return self.buffs.get(buff_id)

    def get_equipment(self, equipment_id: str) -> dict[str, object] | None:
        return self.equipments.get(equipment_id)
