"""游戏主控制模块：集中管理输入、更新和渲染流程。"""

from __future__ import annotations

import pygame

from game.battle.combat.combat_system import CombatSystem
from game.battle.combat.highlight_system import HighlightSystem
from game.battle.turn.turn_manager import ENEMY, PLAYER, TurnManager
from game.battle.movement.grid import DualGrid
from game.controllers.enemy_controller import EnemyController
from game.core.game_state import GameState
from game.entity.unit import Unit, UnitConfig, UnitState
from game.render.attack_highlight_renderer import draw_attack_highlights
from game.render.highlight_renderer import draw_move_highlights
from game.render.map_renderer import TILE_SIZE, render_map
from game.render.path_renderer import draw_path_preview
from game.state.idle_state import IdleState
from game.ui.action_menu import ActionMenu
from game.ui.ui_system import UISystem

BACKGROUND_COLOR = (245, 245, 245)
WINDOW_TITLE = "TBS Game - Dual Battlefield"

BATTLEFIELD_AREA_HEIGHT = 320
BOTTOM_PANEL_HEIGHT = 220
WINDOW_WIDTH = 980
PLAYER_TEAM_ID = 1
ENEMY_TEAM_ID = 2


class Game:
    """游戏控制器：封装主循环中的事件、逻辑更新、渲染。"""

    def __init__(self) -> None:
        # 中文注释：战场由左右两个独立 3x4 子网格组成，中间空区不可通行。
        self.grid = DualGrid(side_width=4, height=3, gap_width=2)

        self.tile_size = TILE_SIZE
        self.map_pixel_width = self.grid.width * self.tile_size
        self.map_pixel_height = self.grid.height * self.tile_size

        self.window_width = max(WINDOW_WIDTH, self.map_pixel_width + 80)
        self.window_height = BATTLEFIELD_AREA_HEIGHT + BOTTOM_PANEL_HEIGHT

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)

        # 中文注释：屏幕分区，上方是战场区域，下方是信息与行动面板。
        self.battlefield_rect = pygame.Rect(0, 0, self.window_width, BATTLEFIELD_AREA_HEIGHT)
        self.bottom_panel_rect = pygame.Rect(0, BATTLEFIELD_AREA_HEIGHT, self.window_width, BOTTOM_PANEL_HEIGHT)

        unit_panel_width = int(self.window_width * 0.38)
        self.unit_info_panel_rect = pygame.Rect(
            self.bottom_panel_rect.x,
            self.bottom_panel_rect.y,
            unit_panel_width,
            self.bottom_panel_rect.height,
        )
        self.action_panel_rect = pygame.Rect(
            self.unit_info_panel_rect.right,
            self.bottom_panel_rect.y,
            self.window_width - unit_panel_width,
            self.bottom_panel_rect.height,
        )

        # 中文注释：战场网格在上方区域居中显示。
        self.battlefield_origin = (
            self.battlefield_rect.x + (self.battlefield_rect.width - self.map_pixel_width) // 2,
            self.battlefield_rect.y + (self.battlefield_rect.height - self.map_pixel_height) // 2,
        )

        # 中文注释：初始化双方多个单位。
        self.player_units = [
            self._create_unit(
                name="Knight",
                team_id=PLAYER_TEAM_ID,
                pos=(0, 0),
                hp=20,
                atk=6,
                defense=5,
                move=4,
                range_min=1,
                range_max=2,
            ),
            self._create_unit(
                name="Archer",
                team_id=PLAYER_TEAM_ID,
                pos=(1, 2),
                hp=16,
                atk=5,
                defense=2,
                move=4,
                range_min=2,
                range_max=4,
            ),
        ]
        self.enemy_units = [
            self._create_unit(
                name="Bandit",
                team_id=ENEMY_TEAM_ID,
                pos=(self.grid.enemy_offset_x + self.grid.side_width - 1, 0),
                hp=18,
                atk=5,
                defense=1,
                move=3,
                range_min=1,
                range_max=1,
            ),
            self._create_unit(
                name="Hunter",
                team_id=ENEMY_TEAM_ID,
                pos=(self.grid.enemy_offset_x + self.grid.side_width - 2, 2),
                hp=15,
                atk=4,
                defense=1,
                move=3,
                range_min=2,
                range_max=3,
            ),
        ]

        self.units = [*self.player_units, *self.enemy_units]
        self.turn_manager = TurnManager(
            units=self.units,
            player_team_id=PLAYER_TEAM_ID,
            enemy_team_id=ENEMY_TEAM_ID,
        )

        # 中文注释：保留原有 enum，用于渲染条件与兼容旧逻辑。
        self.game_state = GameState.IDLE
        # 中文注释：引入 State Pattern，Game 仅维护当前状态对象并调用其 handle_input。
        self.current_state = IdleState()
        # 中文注释：当前选中单位（用于 UI 信息查看）。
        self.selected_unit: Unit | None = None

        # 中文注释：行动菜单放在底部右侧 Action Panel，按钮垂直排列。
        self.action_menu = ActionMenu(
            x=self.action_panel_rect.x + 24,
            y=self.action_panel_rect.y + 86,
            width=min(220, self.action_panel_rect.width - 48),
            item_height=44,
        )

        # 中文注释：CombatSystem 统一负责攻击距离与范围判定。
        self.combat_system = CombatSystem(self.grid)

        # 中文注释：敌方回合逻辑委托给 EnemyController 处理。
        self.enemy_controller = EnemyController(
            grid=self.grid,
            units=self.units,
            turn_manager=self.turn_manager,
            enemy_team_id=ENEMY_TEAM_ID,
        )

        # 中文注释：高亮系统负责移动范围/路径预览/攻击范围的 tile 计算。
        self.highlight_system = HighlightSystem(
            grid=self.grid,
            selected_unit_provider=self.get_selected_unit,
            turn_manager=self.turn_manager,
            combat_system=self.combat_system,
            tile_size=self.tile_size,
            player_camp=PLAYER,
        )

        # 中文注释：UI 系统统一负责面板、HUD、单位信息与行动菜单的绘制。
        self.ui_system = UISystem(
            screen=self.screen,
            ui_panel_rect=self.bottom_panel_rect,
            unit_info_rect=self.unit_info_panel_rect,
            action_panel_rect=self.action_panel_rect,
            action_menu=self.action_menu,
            selected_unit_provider=self.get_selected_unit,
        )

        self.running = True
        self.events: list[pygame.event.Event] = []

    def _create_unit(
        self,
        name: str,
        team_id: int,
        pos: tuple[int, int],
        hp: int,
        atk: int,
        defense: int,
        move: int,
        range_min: int,
        range_max: int,
    ) -> Unit:
        config = UnitConfig(
            hp=hp,
            atk=atk,
            defense=defense,
            move=move,
            range_min=range_min,
            range_max=range_max,
        )
        state = UnitState(pos=pos, hp=hp, acted=False, alive=True, team_id=team_id)
        unit = Unit(config, state)
        setattr(unit, "name", name)
        return unit

    def handle_events(self) -> None:
        """处理输入事件：保存当前帧事件并处理退出事件。"""
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

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

            if self.selected_unit is not None and not self.selected_unit.state.alive:
                self.selected_unit = None
                self.game_state = GameState.IDLE
                self.current_state = IdleState()

            self.current_state = self.current_state.handle_input(
                game=self,
                events=self.events,
                battlefield_rect=self.battlefield_rect,
            )
        elif self.turn_manager.current_camp == ENEMY:
            self.selected_unit = None
            self.game_state = GameState.ENEMY_TURN
            self.enemy_controller.update()

        if self.turn_manager.is_turn_finished():
            self.turn_manager.next_turn()

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
        pygame.display.flip()

    def _should_show_action_menu(self) -> bool:
        # 中文注释：仅当当前选中单位“可由玩家操作”时显示行动菜单。
        return self.game_state == GameState.UNIT_SELECTED and self.can_command_selected_unit()

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



