"""玩家军队模块：管理玩家全局拥有单位并提供部署名单。"""

from __future__ import annotations

import json
from pathlib import Path


class PlayerArmy:
    """玩家单位仓库：从全局 roster 文件加载可部署单位。"""

    def __init__(self, roster_path: Path | None = None) -> None:
        # 中文注释：默认读取项目根目录 data/player/player_roster.json。
        root = Path(__file__).resolve().parents[2]
        self._roster_path = roster_path or (root / "data" / "player" / "player_roster.json")
        self._units: list[dict[str, object]] = self._load_roster()

    def _load_roster(self) -> list[dict[str, object]]:
        if not self._roster_path.exists():
            raise FileNotFoundError(f"Player roster file not found: {self._roster_path}")

        with self._roster_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        # 中文注释：支持未来扩展字段，当前仅要求 units 为列表。
        units = data.get("units", []) if isinstance(data, dict) else []
        if not isinstance(units, list):
            raise ValueError("player_roster.json must contain a list field named 'units'")

        normalized: list[dict[str, object]] = []
        for entry in units:
            if not isinstance(entry, dict):
                continue
            if "type" not in entry:
                continue
            normalized.append(dict(entry))
        return normalized

    def get_deployable_units(self) -> list[dict[str, object]]:
        """返回可部署单位列表（拷贝），供部署界面读取。"""
        return [dict(unit) for unit in self._units]
