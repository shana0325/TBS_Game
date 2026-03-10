"""战斗场景模块：定义关卡绑定、单位编成与胜利条件。"""

from __future__ import annotations


SCENARIO_1: dict[str, object] = {
    "level": "level_1",
    "player_roster": [
        {"type": "Hero"},
        {"type": "Knight"},
    ],
    "enemy_units": [
        {"type": "Goblin", "spawn": 0},
        {"type": "Orc", "spawn": 1},
    ],
    "victory_condition": "eliminate_all_enemies",
}
