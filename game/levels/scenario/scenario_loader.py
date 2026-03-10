"""场景加载模块：按名称返回战斗场景配置。"""

from __future__ import annotations

from game.levels.scenario.scenario_1 import SCENARIO_1


_SCENARIO_REGISTRY: dict[str, dict[str, object]] = {
    "scenario_1": SCENARIO_1,
}


def load_scenario(scenario_name: str) -> dict[str, object]:
    """根据场景名加载场景数据。"""
    # 中文注释：复制数据，避免运行期改动污染静态配置。
    scenario = _SCENARIO_REGISTRY.get(scenario_name)
    if scenario is None:
        raise ValueError(f"Unknown scenario: {scenario_name}")
    return {
        "level": scenario["level"],
        "player_units": list(scenario.get("player_units", [])),
        "enemy_units": list(scenario.get("enemy_units", [])),
        "victory_condition": scenario.get("victory_condition", "eliminate_all_enemies"),
    }

