"""配置加载模块：负责从外部 JSON 读取单位/技能/Buff/装备 配置。"""

from __future__ import annotations

import json
from pathlib import Path


class ConfigLoader:
    """Loads static JSON configs for units, skills, buffs, and equipments."""

    def __init__(self) -> None:
        # 中文注释：数据目录位于项目根目录 data/。
        self._project_root = Path(__file__).resolve().parents[2]
        self._data_root = self._project_root / "data"

        self._unit_path = self._data_root / "unit" / "units.json"
        self._skill_path = self._data_root / "skill" / "skills.json"
        self._buff_path = self._data_root / "buff" / "buffs.json"
        self._equipment_path = self._data_root / "equipment" / "equipments.json"

        # 中文注释：初始化时直接加载，供运行时快速读取。
        self.units: dict[str, dict[str, object]] = self.load_units()
        self.skills: dict[str, dict[str, object]] = self.load_skills()
        self.buffs: dict[str, dict[str, object]] = self.load_buffs()
        self.equipments: dict[str, dict[str, object]] = self.load_equipments()

    def load(self, path: Path) -> dict[str, dict[str, object]]:
        """Load one JSON file and return dictionary content."""
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(f"Config file must contain a JSON object: {path}")
        return data

    def load_units(self) -> dict[str, dict[str, object]]:
        """Load unit template config from data/unit/units.json."""
        return self.load(self._unit_path)

    def load_skills(self) -> dict[str, dict[str, object]]:
        """Load skill template config from data/skill/skills.json."""
        return self.load(self._skill_path)

    def load_buffs(self) -> dict[str, dict[str, object]]:
        """Load buff template config from data/buff/buffs.json."""
        return self.load(self._buff_path)

    def load_equipments(self) -> dict[str, dict[str, object]]:
        """Load equipment template config from data/equipment/equipments.json."""
        return self.load(self._equipment_path)
