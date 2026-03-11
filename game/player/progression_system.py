"""成长系统模块：处理属性加点与技能学习/装备逻辑。"""

from __future__ import annotations

from game.player.player_unit_data import PlayerUnitData


class ProgressionSystem:
    """玩家角色成长逻辑入口。"""

    @staticmethod
    def add_exp(unit_data: PlayerUnitData, amount: int) -> dict[str, int]:
        """增加经验并在需要时自动升级。"""
        if amount <= 0:
            return {"exp_gained": 0, "levels_gained": 0}

        unit_data.exp += amount
        levels_gained = 0

        # 中文注释：最小版本采用线性升级曲线，后续可替换为表驱动。
        while unit_data.exp >= ProgressionSystem.required_exp_for_level(unit_data.level):
            unit_data.exp -= ProgressionSystem.required_exp_for_level(unit_data.level)
            unit_data.level += 1
            unit_data.stat_points += 2
            unit_data.skill_points += 1
            levels_gained += 1

        return {"exp_gained": amount, "levels_gained": levels_gained}

    @staticmethod
    def required_exp_for_level(level: int) -> int:
        """返回指定等级升到下一等级所需经验。"""
        return max(100, level * 100)

    @staticmethod
    def add_stat_point(unit_data: PlayerUnitData, stat_name: str, amount: int = 1) -> bool:
        """消耗属性点并增加指定属性。"""
        if amount <= 0 or unit_data.stat_points < amount:
            return False

        key = stat_name.strip().lower()
        if not key:
            return False

        unit_data.stat_points -= amount
        unit_data.allocated_stats[key] = unit_data.allocated_stats.get(key, 0) + amount
        return True

    @staticmethod
    def learn_skill(unit_data: PlayerUnitData, skill_id: str, cost: int = 1) -> bool:
        """消耗技能点学习一个新技能。"""
        normalized = skill_id.strip()
        if not normalized or unit_data.skill_points < cost:
            return False
        if normalized in unit_data.learned_skills:
            return False

        unit_data.skill_points -= cost
        unit_data.learned_skills.append(normalized)
        return True

    @staticmethod
    def equip_skill(unit_data: PlayerUnitData, skill_id: str) -> bool:
        """将已学习技能加入当前装备技能列表。"""
        normalized = skill_id.strip()
        if not normalized:
            return False
        if normalized not in unit_data.learned_skills and normalized not in unit_data.extra_skills:
            return False
        if normalized in unit_data.equipped_skills:
            return False

        unit_data.equipped_skills.append(normalized)
        return True
