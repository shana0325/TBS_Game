"""装备实体：描述装备模板的基础信息。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Equipment:
    """战斗外装备数据对象。"""

    equipment_id: str
    name: str
    slot: str
    modifiers: dict[str, int] = field(default_factory=dict)
    granted_skills: list[str] = field(default_factory=list)
