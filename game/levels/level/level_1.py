"""关卡数据模块：定义地图尺寸、地形与出生点。"""

from __future__ import annotations


LEVEL_1: dict[str, object] = {
    "map": {
        # 中文注释：逻辑地图尺寸（不含中间 gap），用于关卡数据展示与校验。
        "width": 8,
        "height": 3,
        # 中文注释：DualGrid 构建参数，保持当前双战场结构不变。
        "side_width": 4,
        "gap_width": 2,
    },
    "terrain": [
        {"pos": (2, 1), "type": "forest"},
        {"pos": (8, 1), "type": "forest"},
    ],
    "spawns": {
        # 中文注释：出生点使用 DualGrid 的全局坐标（含 gap 偏移）。
        "player": [(0, 0), (1, 2)],
        "enemy": [(9, 0), (8, 2)],
    },
}
