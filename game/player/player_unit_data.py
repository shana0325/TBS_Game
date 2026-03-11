"""玩家角色数据模型：保存玩家持有单位的成长与技能状态。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PlayerUnitData:
    """玩家持有单位的持久化数据。"""

    unit_id: str
    unit_type: str
    level: int = 1
    exp: int = 0
    stat_points: int = 0
    skill_points: int = 0
    equipment: list[str] = field(default_factory=list)
    allocated_stats: dict[str, int] = field(default_factory=dict)
    learned_skills: list[str] = field(default_factory=list)
    equipped_skills: list[str] = field(default_factory=list)
    extra_skills: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """转换为部署与生成流程使用的字典。"""
        return {
            "id": self.unit_id,
            "type": self.unit_type,
            "level": self.level,
            "exp": self.exp,
            "stat_points": self.stat_points,
            "skill_points": self.skill_points,
            "equipment": list(self.equipment),
            "allocated_stats": dict(self.allocated_stats),
            "learned_skills": list(self.learned_skills),
            "equipped_skills": list(self.equipped_skills),
            "extra_skills": list(self.extra_skills),
        }
