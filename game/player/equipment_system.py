"""装备系统：处理玩家持久化角色的装备槽位与数值汇总。"""

from __future__ import annotations

from game.data.game_database import GameDatabase
from game.player.player_unit_data import PlayerUnitData


class EquipmentSystem:
    """玩家装备逻辑入口。"""

    VALID_SLOTS = ("weapon", "offhand", "accessory")

    @classmethod
    def equip_item(
        cls,
        unit_data: PlayerUnitData,
        slot: str,
        equipment_id: str,
        game_db: GameDatabase,
    ) -> bool:
        """将装备放入指定槽位。"""
        normalized_slot = cls._normalize_slot(slot)
        normalized_id = equipment_id.strip()
        if normalized_slot is None or not normalized_id:
            return False

        equipment = game_db.get_equipment(normalized_id)
        if equipment is None:
            return False

        if str(equipment.get("slot", "")).strip().lower() != normalized_slot:
            return False

        unit_data.equipment[normalized_slot] = normalized_id
        return True

    @classmethod
    def unequip_item(cls, unit_data: PlayerUnitData, slot: str) -> bool:
        """卸下指定槽位的装备。"""
        normalized_slot = cls._normalize_slot(slot)
        if normalized_slot is None:
            return False

        if unit_data.equipment.get(normalized_slot) is None:
            return False

        unit_data.equipment[normalized_slot] = None
        return True

    @classmethod
    def get_total_modifiers(
        cls,
        unit_data: PlayerUnitData,
        game_db: GameDatabase,
    ) -> dict[str, int]:
        """汇总角色当前装备提供的属性加成。"""
        totals: dict[str, int] = {}
        for equipment_id in cls.get_equipped_item_ids(unit_data):
            equipment = game_db.get_equipment(equipment_id)
            if equipment is None:
                continue

            raw_modifiers = equipment.get("modifiers", {})
            if not isinstance(raw_modifiers, dict):
                continue

            for key, value in raw_modifiers.items():
                stat_name = str(key).strip().lower()
                if not stat_name:
                    continue
                totals[stat_name] = totals.get(stat_name, 0) + int(value)
        return totals

    @classmethod
    def get_granted_skills(
        cls,
        unit_data: PlayerUnitData,
        game_db: GameDatabase,
    ) -> list[str]:
        """收集装备赋予的技能列表。"""
        granted: list[str] = []
        for equipment_id in cls.get_equipped_item_ids(unit_data):
            equipment = game_db.get_equipment(equipment_id)
            if equipment is None:
                continue

            raw_skills = equipment.get("granted_skills", [])
            if not isinstance(raw_skills, list):
                continue

            for raw_skill in raw_skills:
                skill_id = str(raw_skill).strip()
                if skill_id and skill_id not in granted:
                    granted.append(skill_id)
        return granted

    @staticmethod
    def get_equipped_item_ids(unit_data: PlayerUnitData) -> list[str]:
        """返回角色当前已装备物品 id 列表。"""
        result: list[str] = []
        for slot in EquipmentSystem.VALID_SLOTS:
            equipment_id = unit_data.equipment.get(slot)
            if equipment_id:
                result.append(equipment_id)
        return result

    @classmethod
    def _normalize_slot(cls, slot: str) -> str | None:
        normalized = slot.strip().lower()
        if normalized not in cls.VALID_SLOTS:
            return None
        return normalized
