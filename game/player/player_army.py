"""玩家军队模块：管理玩家全局拥有单位并提供部署名单。"""

from __future__ import annotations

import json
from pathlib import Path

from game.data.config_loader import ConfigLoader
from game.data.game_database import GameDatabase
from game.player.equipment_system import EquipmentSystem
from game.player.player_unit_data import PlayerUnitData
from game.player.progression_system import ProgressionSystem


class PlayerArmy:
    """玩家单位仓库：从全局 roster 文件加载可部署单位。"""

    _config_loader = ConfigLoader()
    _game_db = GameDatabase(_config_loader)

    def __init__(self, roster_path: Path | None = None) -> None:
        # 中文注释：默认读取项目根目录 data/player/player_roster.json。
        root = Path(__file__).resolve().parents[2]
        self._roster_path = roster_path or (root / "data" / "player" / "player_roster.json")
        self._units: list[PlayerUnitData] = self._load_roster()

    def _load_roster(self) -> list[PlayerUnitData]:
        if not self._roster_path.exists():
            raise FileNotFoundError(f"Player roster file not found: {self._roster_path}")

        with self._roster_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        # 中文注释：支持未来扩展字段，当前仅要求 units 为列表。
        units = data.get("units", []) if isinstance(data, dict) else []
        if not isinstance(units, list):
            raise ValueError("player_roster.json must contain a list field named 'units'")

        normalized: list[PlayerUnitData] = []
        for entry in units:
            if not isinstance(entry, dict):
                continue
            if "type" not in entry:
                continue

            normalized.append(
                PlayerUnitData(
                    unit_id=str(entry.get("id", entry.get("type", ""))),
                    unit_type=str(entry.get("type", "")),
                    level=int(entry.get("level", 1)),
                    exp=int(entry.get("exp", 0)),
                    stat_points=int(entry.get("stat_points", 0)),
                    skill_points=int(entry.get("skill_points", 0)),
                    equipment=self._normalize_equipment_map(entry.get("equipment", {})),
                    allocated_stats=self._normalize_stat_map(entry.get("allocated_stats", {})),
                    learned_skills=self._normalize_string_list(entry.get("learned_skills", [])),
                    equipped_skills=self._normalize_string_list(entry.get("equipped_skills", [])),
                    extra_skills=self._normalize_string_list(entry.get("extra_skills", [])),
                )
            )
        return normalized

    def save(self) -> None:
        """将当前玩家 roster 写回 JSON。"""
        payload = {"units": [unit.to_dict() for unit in self._units]}
        with self._roster_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=True, indent=2)
            f.write("\n")

    def get_deployable_units(self) -> list[dict[str, object]]:
        """返回可部署单位列表（拷贝），供部署界面读取。"""
        return [unit.to_dict() for unit in self._units]

    def get_units(self) -> list[PlayerUnitData]:
        """返回完整玩家角色数据。"""
        return [
            PlayerUnitData(
                unit_id=unit.unit_id,
                unit_type=unit.unit_type,
                level=unit.level,
                exp=unit.exp,
                stat_points=unit.stat_points,
                skill_points=unit.skill_points,
                equipment=dict(unit.equipment),
                allocated_stats=dict(unit.allocated_stats),
                learned_skills=list(unit.learned_skills),
                equipped_skills=list(unit.equipped_skills),
                extra_skills=list(unit.extra_skills),
            )
            for unit in self._units
        ]

    def find_unit(self, unit_id: str) -> PlayerUnitData | None:
        """按 id 查找玩家角色数据。"""
        for unit in self._units:
            if unit.unit_id == unit_id:
                return unit
        return None

    def grant_exp(self, unit_id: str, amount: int) -> dict[str, int]:
        """给指定角色增加经验并自动保存。"""
        unit = self.find_unit(unit_id)
        if unit is None:
            return {"exp_gained": 0, "levels_gained": 0}

        result = ProgressionSystem.add_exp(unit, amount)
        self.save()
        return result

    def spend_stat_point(self, unit_id: str, stat_name: str, amount: int = 1) -> bool:
        """对指定角色执行属性加点并保存。"""
        unit = self.find_unit(unit_id)
        if unit is None:
            return False

        changed = ProgressionSystem.add_stat_point(unit, stat_name, amount)
        if changed:
            self.save()
        return changed

    def learn_skill(self, unit_id: str, skill_id: str, cost: int = 1) -> bool:
        """对指定角色学习新技能并保存。"""
        unit = self.find_unit(unit_id)
        if unit is None:
            return False

        changed = ProgressionSystem.learn_skill(unit, skill_id, cost)
        if changed:
            self.save()
        return changed

    def equip_skill(self, unit_id: str, skill_id: str) -> bool:
        """对指定角色装备技能并保存。"""
        unit = self.find_unit(unit_id)
        if unit is None:
            return False

        changed = ProgressionSystem.equip_skill(unit, skill_id)
        if changed:
            self.save()
        return changed

    def equip_item(self, unit_id: str, slot: str, equipment_id: str) -> bool:
        """对指定角色装备物品并保存。"""
        unit = self.find_unit(unit_id)
        if unit is None:
            return False

        changed = EquipmentSystem.equip_item(unit, slot, equipment_id, self._game_db)
        if changed:
            self.save()
        return changed

    def unequip_item(self, unit_id: str, slot: str) -> bool:
        """对指定角色卸下装备并保存。"""
        unit = self.find_unit(unit_id)
        if unit is None:
            return False

        changed = EquipmentSystem.unequip_item(unit, slot)
        if changed:
            self.save()
        return changed

    @staticmethod
    def _normalize_string_list(raw_values: object) -> list[str]:
        if not isinstance(raw_values, list):
            return []
        return [str(item).strip() for item in raw_values if str(item).strip()]

    @staticmethod
    def _normalize_stat_map(raw_stats: object) -> dict[str, int]:
        if not isinstance(raw_stats, dict):
            return {}

        normalized: dict[str, int] = {}
        for key, value in raw_stats.items():
            stat_name = str(key).strip().lower()
            if not stat_name:
                continue
            normalized[stat_name] = int(value)
        return normalized

    @staticmethod
    def _normalize_equipment_map(raw_equipment: object) -> dict[str, str | None]:
        # 中文注释：兼容旧存档中的数组格式，自动映射到标准装备槽位。
        empty_equipment = {"weapon": None, "offhand": None, "accessory": None}

        if isinstance(raw_equipment, list):
            for index, equipment_id in enumerate(raw_equipment[:3]):
                normalized_id = str(equipment_id).strip()
                if not normalized_id:
                    continue
                empty_equipment[EquipmentSystem.VALID_SLOTS[index]] = normalized_id
            return empty_equipment

        if not isinstance(raw_equipment, dict):
            return empty_equipment

        for slot in EquipmentSystem.VALID_SLOTS:
            raw_value = raw_equipment.get(slot)
            normalized_id = str(raw_value).strip() if raw_value is not None else ""
            empty_equipment[slot] = normalized_id or None
        return empty_equipment
