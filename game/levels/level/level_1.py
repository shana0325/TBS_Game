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
    "deployment_zones": {
        # 中文注释：玩家部署区使用 DualGrid 全局坐标。
        "player": [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
    },
    "spawns": {
        # 中文注释：敌方出生点仍用于进入战斗时自动生成敌人。
        "enemy": [(9, 0), (8, 2)],
    },
}
