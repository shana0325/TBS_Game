"""游戏主控制模块：集中管理输入、更新和渲染流程。"""

from __future__ import annotations

import pygame

from game.battle.combat.combat_system import CombatSystem
from game.battle.combat.highlight_system import HighlightSystem
from game.battle.movement.grid import DualGrid
from game.battle.turn.turn_manager import ENEMY, PLAYER, TurnManager
from game.controllers.enemy_controller import EnemyController
from game.core.game_state import GameState
from game.entity.skill import Skill
from game.entity.unit import Unit
from game.levels.level.level_loader import load_level
from game.levels.scenario.scenario_loader import load_scenario
from game.levels.systems.spawn_system import SpawnSystem
from game.render.attack_highlight_renderer import draw_attack_highlights
from game.render.highlight_renderer import draw_move_highlights
from game.render.map_renderer import TILE_SIZE, render_map
from game.render.path_renderer import draw_path_preview
from game.state.idle_state import IdleState
from game.ui.action_menu import ActionMenu
from game.ui.battle_log import BattleLog
from game.ui.skill_menu import SkillMenu
from game.ui.ui_system import UISystem

BACKGROUND_COLOR = (245, 245, 245)
WINDOW_TITLE = "TBS Game - Dual Battlefield"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
RIGHT_LOG_RATIO = 0.25
BOTTOM_UI_RATIO = 0.30
UNIT_INFO_RATIO = 0.38
PLAYER_TEAM_ID = 1
ENEMY_TEAM_ID = 2

# 中文注释：地形模板仅用于初始化 tile 属性，不耦合具体玩法计算。
TERRAIN_PRESETS: dict[str, dict[str, int]] = {
    "plain": {"move_cost": 1, "defense_bonus": 0},
    "forest": {"move_cost": 2, "defense_bonus": 1},
}


class Game:
    """游戏控制器：封装主循环中的事件、逻辑更新、渲染。"""

    def __init__(
        self,
        level_data: dict[str, object] | None = None,
        scenario_data: dict[str, object] | None = None,
        grid: DualGrid | None = None,
        player_units: list[Unit] | None = None,
        enemy_units: list[Unit] | None = None,
    ) -> None:
        # 中文注释：允许外部 Screen 注入关卡/场景/实体；未注入时走默认加载流程。
        self.level_data = level_data if level_data is not None else load_level("level_1")
        self.scenario_data = scenario_data if scenario_data is not None else load_scenario("scenario_1")

        if grid is None:
            map_config = self.level_data.get("map", {})
            side_width = int(map_config.get("side_width", 4))
            grid_height = int(map_config.get("height", 3))
            gap_width = int(map_config.get("gap_width", 2))
            self.grid = DualGrid(side_width=side_width, height=grid_height, gap_width=gap_width)
            self._apply_level_terrain(self.level_data)
        else:
            self.grid = grid

        if player_units is None or enemy_units is None:
            self.player_units, self.enemy_units = SpawnSystem.spawn_units(
                grid=self.grid,
                level_data=self.level_data,
                scenario_data=self.scenario_data,
                player_team_id=PLAYER_TEAM_ID,
                enemy_team_id=ENEMY_TEAM_ID,
            )
        else:
            self.player_units = player_units
            self.enemy_units = enemy_units

        self.units = [*self.player_units, *self.enemy_units]
        self.turn_manager = TurnManager(
            units=self.units,
            player_team_id=PLAYER_TEAM_ID,
            enemy_team_id=ENEMY_TEAM_ID,
        )

        # 中文注释：战斗日志由 Game 持有，供状态机、控制器和 UI 统一读写。
        self.battle_log = BattleLog()

        self.tile_size = TILE_SIZE
        self.map_pixel_width = self.grid.width * self.tile_size
        self.map_pixel_height = self.grid.height * self.tile_size

        # 中文注释：窗口尺寸优先沿用当前 display，再按地图最小显示需求兜底扩展。
        current_surface = pygame.display.get_surface()
        if current_surface is not None:
            base_width, base_height = current_surface.get_size()
        else:
            base_width, base_height = WINDOW_WIDTH, WINDOW_HEIGHT

        min_width = int((self.map_pixel_width + 80) / (1.0 - RIGHT_LOG_RATIO))
        min_height = int((self.map_pixel_height + 80) / (1.0 - BOTTOM_UI_RATIO))
        self.window_width = max(base_width, min_width)
        self.window_height = max(base_height, min_height)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption(WINDOW_TITLE)

        self.game_state = GameState.IDLE
        self.current_state = IdleState()
        self.selected_unit: Unit | None = None
        self.selected_skill: Skill | None = None

        # 中文注释：先构造菜单对象，具体位置在 _recalculate_layout 中更新。
        self.action_menu = ActionMenu()
        self.skill_menu = SkillMenu(x=0, y=0)

        self.combat_system = CombatSystem(self.grid)
        self.enemy_controller = EnemyController(
            grid=self.grid,
            units=self.units,
            turn_manager=self.turn_manager,
            enemy_team_id=ENEMY_TEAM_ID,
            battle_log=self.battle_log,
        )
        self.highlight_system = HighlightSystem(
            grid=self.grid,
            selected_unit_provider=self.get_selected_unit,
            turn_manager=self.turn_manager,
            combat_system=self.combat_system,
            tile_size=self.tile_size,
            player_camp=PLAYER,
        )

        # 中文注释：先初始化占位 UISystem，再由 _recalculate_layout 写入真实布局。
        zero = pygame.Rect(0, 0, 1, 1)
        self.ui_system = UISystem(
            screen=self.screen,
            ui_panel_rect=zero,
            unit_info_rect=zero,
            action_panel_rect=zero,
            log_panel_rect=zero,
            action_menu=self.action_menu,
            selected_unit_provider=self.get_selected_unit,
            battle_log=self.battle_log,
        )

        self._recalculate_layout()

        self.running = True
        self.events: list[pygame.event.Event] = []

    def _recalculate_layout(self) -> None:
        """按当前窗口尺寸重算战场与 UI 布局。"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        log_panel_width = max(220, int(screen_width * RIGHT_LOG_RATIO))
        bottom_panel_height = max(160, int(screen_height * BOTTOM_UI_RATIO))
        main_area_width = max(320, screen_width - log_panel_width)
        battlefield_height = max(220, screen_height - bottom_panel_height)

        self.window_width = screen_width
        self.window_height = screen_height

        # 中文注释：区域4是最右侧整列日志栏；区域1/2/3在左侧主内容区。
        self.log_panel_rect = pygame.Rect(
            screen_width - log_panel_width,
            0,
            log_panel_width,
            screen_height,
        )
        self.battlefield_rect = pygame.Rect(0, 0, main_area_width, battlefield_height)
        self.bottom_panel_rect = pygame.Rect(0, battlefield_height, main_area_width, bottom_panel_height)

        unit_panel_width = max(220, int(self.bottom_panel_rect.width * UNIT_INFO_RATIO))
        unit_panel_width = min(unit_panel_width, max(220, self.bottom_panel_rect.width - 220))
        self.unit_info_panel_rect = pygame.Rect(
            self.bottom_panel_rect.x,
            self.bottom_panel_rect.y,
            unit_panel_width,
            self.bottom_panel_rect.height,
        )
        self.action_panel_rect = pygame.Rect(
            self.unit_info_panel_rect.right,
            self.bottom_panel_rect.y,
            self.bottom_panel_rect.width - unit_panel_width,
            self.bottom_panel_rect.height,
        )

        # 中文注释：战场网格在区域1中居中显示。
        self.battlefield_origin = (
            self.battlefield_rect.x + (self.battlefield_rect.width - self.map_pixel_width) // 2,
            self.battlefield_rect.y + (self.battlefield_rect.height - self.map_pixel_height) // 2,
        )

        # 中文注释：Action/Skill 菜单锚点和尺寸按区域3比例计算，避免固定像素。
        action_margin_x = max(12, int(self.action_panel_rect.width * 0.08))
        action_margin_y = max(12, int(self.action_panel_rect.height * 0.18))
        menu_x = self.action_panel_rect.x + action_margin_x
        menu_y = self.action_panel_rect.y + action_margin_y
        menu_width = min(
            max(160, int(self.action_panel_rect.width * 0.55)),
            max(120, self.action_panel_rect.width - action_margin_x * 2),
        )

        self.action_menu.x = menu_x
        self.action_menu.y = menu_y
        self.action_menu.width = menu_width
        self.action_menu.item_height = max(34, int(self.action_panel_rect.height * 0.20))

        self.skill_menu.x = menu_x
        self.skill_menu.y = menu_y
        self.skill_menu.width = menu_width
        self.skill_menu.item_height = max(32, int(self.action_panel_rect.height * 0.18))

        self.ui_system.update_layout(
            screen=self.screen,
            ui_panel_rect=self.bottom_panel_rect,
            unit_info_rect=self.unit_info_panel_rect,
            action_panel_rect=self.action_panel_rect,
            log_panel_rect=self.log_panel_rect,
        )

    def _resize_window(self, width: int, height: int) -> None:
        """处理窗口尺寸变化并实时重排布局。"""
        min_width = int((self.map_pixel_width + 80) / (1.0 - RIGHT_LOG_RATIO))
        min_height = int((self.map_pixel_height + 80) / (1.0 - BOTTOM_UI_RATIO))
        new_width = max(width, min_width)
        new_height = max(height, min_height)

        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        self._recalculate_layout()

    def _apply_level_terrain(self, level_data: dict[str, object]) -> None:
        """将关卡地形数据写入 grid tile。"""
        # 中文注释：只做初始化赋值，不触发额外战斗逻辑。
        terrain_list = list(level_data.get("terrain", []))
        for terrain_item in terrain_list:
            if not isinstance(terrain_item, dict):
                continue

            pos = terrain_item.get("pos")
            terrain_type = str(terrain_item.get("type", "plain"))
            if not isinstance(pos, tuple) or len(pos) != 2:
                continue

            tile = self.grid.get_tile(pos[0], pos[1])
            if tile is None:
                continue

            preset = TERRAIN_PRESETS.get(terrain_type, TERRAIN_PRESETS["plain"])
            tile.move_cost = preset["move_cost"]
            tile.defense_bonus = preset["defense_bonus"]

    def handle_events(self, events: list[pygame.event.Event] | None = None) -> None:
        """处理输入事件：保存当前帧事件并处理退出事件。"""
        self.events = pygame.event.get() if events is None else events
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self._resize_window(event.w, event.h)
            elif event.type == getattr(pygame, "WINDOWSIZECHANGED", -1):
                self._resize_window(event.x, event.y)

    def update(self) -> None:
        """更新游戏逻辑：回合流转、玩家输入处理与 AI 行为。"""
        if not self.running:
            return

        if not self._has_alive_units(PLAYER_TEAM_ID) or not self._has_alive_units(ENEMY_TEAM_ID):
            self.running = False
            return

        if self.turn_manager.current_camp == PLAYER:
            if self.game_state == GameState.ENEMY_TURN:
                self.game_state = GameState.IDLE
                self.current_state = IdleState()
                self.selected_unit = None
                self.selected_skill = None

            if self.selected_unit is not None and not self.selected_unit.state.alive:
                self.selected_unit = None
                self.selected_skill = None
                self.game_state = GameState.IDLE
                self.current_state = IdleState()

            self.current_state = self.current_state.handle_input(
                game=self,
                events=self.events,
                battlefield_rect=self.battlefield_rect,
            )
        elif self.turn_manager.current_camp == ENEMY:
            self.selected_unit = None
            self.selected_skill = None
            self.game_state = GameState.ENEMY_TURN
            self.enemy_controller.update()

        if self.turn_manager.is_turn_finished():
            self.turn_manager.next_turn()
            next_turn_text = "Player Turn" if self.turn_manager.current_camp == PLAYER else "Enemy Turn"
            self.battle_log.add(next_turn_text, category="turn", side="neutral")

    def render(self) -> None:
        """渲染画面：地图、高亮、路径、UI。"""
        move_highlight_tiles = self.highlight_system.get_move_tiles(self.game_state)
        path_preview = self.highlight_system.get_path_preview(
            game_state=self.game_state,
            battlefield_rect=self.battlefield_rect,
            move_tiles=move_highlight_tiles,
            origin=self.battlefield_origin,
        )
        attack_highlight_tiles = self.highlight_system.get_attack_tiles(self.game_state)

        if self._should_show_action_menu():
            self.action_menu.show()
        else:
            self.action_menu.hide()

        if self._should_show_skill_menu():
            if self.selected_unit is not None:
                self.skill_menu.set_skills(self.selected_unit.skills)
            self.skill_menu.show()
        else:
            self.skill_menu.hide()

        self.screen.fill(BACKGROUND_COLOR)
        render_map(
            self.screen,
            self.grid,
            self.units,
            battlefield_rect=self.battlefield_rect,
            origin=self.battlefield_origin,
            tile_size=self.tile_size,
        )
        draw_move_highlights(self.screen, move_highlight_tiles, self.tile_size, origin=self.battlefield_origin)
        draw_attack_highlights(self.screen, attack_highlight_tiles, self.tile_size, origin=self.battlefield_origin)
        draw_path_preview(self.screen, path_preview, self.tile_size, origin=self.battlefield_origin)
        self.ui_system.render(self.units, self.turn_manager.current_camp)
        self.skill_menu.draw(self.screen)
        pygame.display.flip()

    def _should_show_action_menu(self) -> bool:
        # 中文注释：仅当当前选中单位“可由玩家操作”时显示行动菜单。
        return self.game_state == GameState.UNIT_SELECTED and self.can_command_selected_unit()

    def _should_show_skill_menu(self) -> bool:
        # 中文注释：技能菜单仅在技能模式且单位有技能时显示。
        return (
            self.game_state == GameState.SKILL_MODE
            and self.can_command_selected_unit()
            and self.selected_unit is not None
            and len(self.selected_unit.skills) > 0
        )

    def _has_alive_units(self, team_id: int) -> bool:
        return any(unit.state.alive and unit.state.team_id == team_id for unit in self.units)

    def get_selected_unit(self) -> Unit | None:
        return self.selected_unit

    def can_command_selected_unit(self) -> bool:
        # 中文注释：只有玩家回合 + 玩家单位 + 未行动 + 存活，才允许进入行动指令。
        if self.turn_manager.current_camp != PLAYER:
            return False
        if self.selected_unit is None:
            return False
        if not self.selected_unit.state.alive:
            return False
        if self.selected_unit.state.team_id != PLAYER_TEAM_ID:
            return False
        return not self.selected_unit.state.acted

    def get_viewable_unit_at(self, grid_pos: tuple[int, int]) -> Unit | None:
        # 中文注释：可查看单位不限制阵营与 acted，只要存活且位置匹配即可。
        return self.get_unit_at(grid_pos)

    def get_unit_at(self, grid_pos: tuple[int, int]) -> Unit | None:
        for unit in self.units:
            if unit.state.alive and unit.state.pos == grid_pos:
                return unit
        return None

    def get_selectable_player_unit_at(self, grid_pos: tuple[int, int]) -> Unit | None:
        unit = self.get_unit_at(grid_pos)
        if unit is None:
            return None
        if unit.state.team_id != PLAYER_TEAM_ID:
            return None
        if unit.state.acted or not unit.state.alive:
            return None
        return unit

    def screen_to_grid(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        # 中文注释：将屏幕坐标转换为战场格子坐标，仅在有效 tile 内返回结果。
        x, y = pos
        if not self.battlefield_rect.collidepoint(pos):
            return None

        ox, oy = self.battlefield_origin
        local_x = x - ox
        local_y = y - oy
        if local_x < 0 or local_y < 0:
            return None

        grid_x = local_x // self.tile_size
        grid_y = local_y // self.tile_size
        tile = self.grid.get_tile(grid_x, grid_y)
        if tile is None:
            return None
        return (grid_x, grid_y)
