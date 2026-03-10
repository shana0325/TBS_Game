"""关卡加载器模块：按名称返回关卡数据。"""

from __future__ import annotations

from game.levels.level.level_1 import LEVEL_1


_LEVEL_REGISTRY: dict[str, dict[str, object]] = {
    "level_1": LEVEL_1,
}


def load_level(level_name: str) -> dict[str, object]:
    """根据关卡名加载关卡数据。"""
    # 中文注释：复制数据，避免运行期对源配置产生副作用。
    level = _LEVEL_REGISTRY.get(level_name)
    if level is None:
        raise ValueError(f"Unknown level: {level_name}")
    return {
        "map": dict(level["map"]),
        "terrain": list(level.get("terrain", [])),
        "spawns": {
            "player": list(level.get("spawns", {}).get("player", [])),
            "enemy": list(level.get("spawns", {}).get("enemy", [])),
        },
    }

