"""战斗屏幕：负责加载关卡/场景、生成单位并驱动 Game。"""

from __future__ import annotations

import pygame

from game.battle.movement.grid import DualGrid
from game.core import texts
from game.core.game import ENEMY_TEAM_ID, PLAYER_TEAM_ID, Game
from game.levels.level.level_loader import load_level
from game.levels.scenario.scenario_loader import load_scenario
from game.levels.systems.spawn_system import SpawnSystem
from game.player.player_army import PlayerArmy
from game.screens.screen_base import ScreenBase

TERRAIN_PRESETS: dict[str, dict[str, int]] = {
    "plain": {"move_cost": 1, "defense_bonus": 0},
    "forest": {"move_cost": 2, "defense_bonus": 1},
}
VICTORY_EXP_REWARD = 100


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
        self.player_army = PlayerArmy()

        level_data = load_level(level_name)
        scenario_data = load_scenario(scenario_name)

        grid = self._create_grid_from_level(level_data)
        self._apply_level_terrain(grid, level_data)

        roster = self.player_army.get_deployable_units()
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

        self.game = Game(
            level_data=level_data,
            scenario_data=scenario_data,
            grid=grid,
            player_units=player_units,
            enemy_units=enemy_units,
        )
        self.game.battle_log.add(texts.BATTLE_START, category="system", side="neutral")
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
        if result_text == texts.BATTLE_VICTORY:
            self._apply_victory_rewards()
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
        player_alive = any(unit.state.alive and unit.state.team_id == PLAYER_TEAM_ID for unit in self.game.units)
        enemy_alive = any(unit.state.alive and unit.state.team_id == ENEMY_TEAM_ID for unit in self.game.units)
        if player_alive and not enemy_alive:
            return texts.BATTLE_VICTORY
        if enemy_alive and not player_alive:
            return texts.BATTLE_DEFEAT
        return texts.BATTLE_ENDED

    def _apply_victory_rewards(self) -> None:
        rewarded_units: list[tuple[str, dict[str, int]]] = []
        for unit in self.game.player_units:
            unit_id = getattr(unit, "player_unit_id", "")
            if not unit_id:
                continue
            rewarded_units.append((unit_id, self.player_army.grant_exp(unit_id, VICTORY_EXP_REWARD)))

        for unit_id, reward in rewarded_units:
            if reward.get("exp_gained", 0) <= 0:
                continue
            unit_data = self.player_army.find_unit(unit_id)
            label = unit_data.unit_type if unit_data is not None else unit_id
            self.game.battle_log.add(texts.format_battle_exp(label, reward["exp_gained"]), category="progression", side="player")
            if reward.get("levels_gained", 0) > 0 and unit_data is not None:
                self.game.battle_log.add(texts.format_battle_level_up(label, unit_data.level), category="progression", side="player")
