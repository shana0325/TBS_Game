"""战斗屏幕：负责加载关卡/场景、生成单位并驱动 Game。"""

from __future__ import annotations

import pygame

from game.battle.movement.grid import DualGrid
from game.core.game import ENEMY_TEAM_ID, PLAYER_TEAM_ID, Game
from game.levels.level.level_loader import load_level
from game.levels.scenario.scenario_loader import load_scenario
from game.levels.systems.spawn_system import SpawnSystem
from game.player.player_army import PlayerArmy
from game.screens.screen_base import ScreenBase

# 中文注释：与 Game 中地形默认值保持一致，确保外部构建战场时行为一致。
TERRAIN_PRESETS: dict[str, dict[str, int]] = {
    "plain": {"move_cost": 1, "defense_bonus": 0},
    "forest": {"move_cost": 2, "defense_bonus": 1},
}


class BattleScreen(ScreenBase):
    """战斗 Screen：封装战斗前加载与战斗进行时的转发。"""

    def __init__(
        self,
        manager: object,
        level_name: str,
        scenario_name: str,
        deployed_player_positions: list[tuple[int, int]] | None = None,
    ) -> None:
        super().__init__(manager)
        self.level_name = level_name
        self.scenario_name = scenario_name

        # 中文注释：在 Screen 层完成关卡和场景加载。
        level_data = load_level(level_name)
        scenario_data = load_scenario(scenario_name)

        # 中文注释：由 Screen 构建 Grid 并应用地形。
        grid = self._create_grid_from_level(level_data)
        self._apply_level_terrain(grid, level_data)

        # 中文注释：玩家出战名单统一来自全局 PlayerArmy。
        roster = PlayerArmy().get_deployable_units()
        if deployed_player_positions is None:
            deployment_positions = list(level_data.get("deployment_zones", {}).get("player", []))[: len(roster)]
        else:
            deployment_positions = deployed_player_positions

        player_units = SpawnSystem.spawn_player_units(
            grid=grid,
            roster=roster,
            deployment_positions=deployment_positions,
            player_team_id=PLAYER_TEAM_ID,
        )
        enemy_units = SpawnSystem.spawn_enemy_units(
            grid=grid,
            level_data=level_data,
            scenario_data=scenario_data,
            enemy_team_id=ENEMY_TEAM_ID,
        )

        # 中文注释：BattleScreen 只负责准备数据，具体战斗流程继续由 Game 处理。
        self.game = Game(
            level_data=level_data,
            scenario_data=scenario_data,
            grid=grid,
            player_units=player_units,
            enemy_units=enemy_units,
        )
        self.game.battle_log.add("Battle Start", category="system", side="neutral")

        # 中文注释：同步 ScreenManager 持有的窗口引用。
        self.manager.screen = self.game.screen

    def handle_input(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.manager.running = False
                return

        self.game.handle_events(events)
        self.manager.screen = self.game.screen

    def update(self) -> None:
        self.game.update()

        if self.game.running:
            return

        result_text = self._resolve_result_text()
        self.game.battle_log.add(result_text, category="result", side="neutral")

        from game.screens.result_screen import ResultScreen

        self.manager.switch_to(ResultScreen(self.manager, result_text))

    def render(self) -> None:
        self.game.render()

    def _create_grid_from_level(self, level_data: dict[str, object]) -> DualGrid:
        map_config = level_data.get("map", {})
        side_width = int(map_config.get("side_width", 4))
        height = int(map_config.get("height", 3))
        gap_width = int(map_config.get("gap_width", 2))
        return DualGrid(side_width=side_width, height=height, gap_width=gap_width)

    def _apply_level_terrain(self, grid: DualGrid, level_data: dict[str, object]) -> None:
        terrain_list = list(level_data.get("terrain", []))
        for terrain_item in terrain_list:
            if not isinstance(terrain_item, dict):
                continue

            pos = terrain_item.get("pos")
            terrain_type = str(terrain_item.get("type", "plain"))
            if not isinstance(pos, tuple) or len(pos) != 2:
                continue

            tile = grid.get_tile(pos[0], pos[1])
            if tile is None:
                continue

            preset = TERRAIN_PRESETS.get(terrain_type, TERRAIN_PRESETS["plain"])
            tile.move_cost = preset["move_cost"]
            tile.defense_bonus = preset["defense_bonus"]

    def _resolve_result_text(self) -> str:
        player_alive = any(
            unit.state.alive and unit.state.team_id == PLAYER_TEAM_ID
            for unit in self.game.units
        )
        enemy_alive = any(
            unit.state.alive and unit.state.team_id == ENEMY_TEAM_ID
            for unit in self.game.units
        )

        if player_alive and not enemy_alive:
            return "Victory"
        if enemy_alive and not player_alive:
            return "Defeat"
        return "Battle Ended"





