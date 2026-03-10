"""游戏主控制模块：集中管理输入、更新和渲染流程。"""

from __future__ import annotations

import pygame

from game.battle.combat.combat_system import CombatSystem
from game.battle.combat.highlight_system import HighlightSystem
from game.battle.movement.grid import DualGrid
from game.battle.turn.turn_manager import ENEMY, PLAYER, TurnManager
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
UI_PANEL_BG_COLOR = (232, 236, 242)
UI_PANEL_BORDER_COLOR = (160, 170, 185)
WINDOW_TITLE = "TBS Game - Dual Battlefield"
UI_PANEL_HEIGHT = 180


class Game:
    """游戏控制器：封装主循环中的事件、逻辑更新、渲染。"""

    def __init__(self) -> None:
        # 中文注释：战场由左右两个独立 3x4 子网格组成，中间空区不可通行。
        self.grid = DualGrid(side_width=4, height=3, gap_width=2)

        self.tile_size = TILE_SIZE
        self.battlefield_width = self.grid.width * self.tile_size
        self.battlefield_height = self.grid.height * self.tile_size
        self.window_width = self.battlefield_width
        self.window_height = self.battlefield_height + UI_PANEL_HEIGHT

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)

        # 中文注释：屏幕分区，上方是战场，下方是 UI Panel。
        self.battlefield_rect = pygame.Rect(0, 0, self.battlefield_width, self.battlefield_height)
        self.ui_panel_rect = pygame.Rect(0, self.battlefield_height, self.window_width, UI_PANEL_HEIGHT)

        self.player = Unit(
            UnitConfig(hp=20, atk=6, defense=5, move=4, range_min=1, range_max=2),
            UnitState(pos=(0, 1), hp=20, acted=False, alive=True, team_id=1),
        )
        self.enemy = Unit(
            UnitConfig(hp=18, atk=5, defense=1, move=3, range_min=1, range_max=1),
            UnitState(
                pos=(self.grid.enemy_offset_x + self.grid.side_width - 1, 1),
                hp=18,
                acted=False,
                alive=True,
                team_id=2,
            ),
        )

        self.units = [self.player, self.enemy]
        self.turn_manager = TurnManager(units=self.units, player_team_id=1, enemy_team_id=2)

        # 中文注释：保留原有 enum，用于渲染条件与兼容旧逻辑。
        self.game_state = GameState.IDLE
        # 中文注释：引入 State Pattern，Game 仅维护当前状态对象并调用其 handle_input。
        self.current_state = IdleState()

        # 中文注释：行动菜单固定绘制在 UI Panel 内，避免超出可见区域。
        self.action_menu = ActionMenu(x=self.ui_panel_rect.x + 16, y=self.ui_panel_rect.y + 16)

        # 中文注释：CombatSystem 统一负责攻击距离与范围判定。
        self.combat_system = CombatSystem(self.grid)

        # 中文注释：敌方回合逻辑委托给 EnemyController 处理。
        self.enemy_controller = EnemyController(
            grid=self.grid,
            enemy=self.enemy,
            units=self.units,
            turn_manager=self.turn_manager,
        )

        # 中文注释：高亮系统负责移动范围/路径预览/攻击范围的 tile 计算。
        self.highlight_system = HighlightSystem(
            grid=self.grid,
            player=self.player,
            turn_manager=self.turn_manager,
            combat_system=self.combat_system,
            tile_size=self.tile_size,
            player_camp=PLAYER,
        )

        # 中文注释：UI 系统统一负责面板、HUD 与行动菜单的绘制。
        self.ui_system = UISystem(
            screen=self.screen,
            ui_panel_rect=self.ui_panel_rect,
            action_menu=self.action_menu,
            panel_bg_color=UI_PANEL_BG_COLOR,
            panel_border_color=UI_PANEL_BORDER_COLOR,
        )

        self.running = True
        self.events: list[pygame.event.Event] = []

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

        if not self.player.state.alive or not self.enemy.state.alive:
            self.running = False
            return

        if self.turn_manager.current_camp == PLAYER:
            if self.game_state == GameState.ENEMY_TURN:
                self.game_state = GameState.IDLE
                self.current_state = IdleState()

            self.current_state = self.current_state.handle_input(
                game=self,
                events=self.events,
                battlefield_rect=self.battlefield_rect,
            )
        elif self.turn_manager.current_camp == ENEMY:
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
        )
        attack_highlight_tiles = self.highlight_system.get_attack_tiles(self.game_state)

        if self._should_show_action_menu():
            self.action_menu.show()
        else:
            self.action_menu.hide()

        self.screen.fill(BACKGROUND_COLOR)
        render_map(self.screen, self.grid, self.units)
        draw_move_highlights(self.screen, move_highlight_tiles, self.tile_size)
        draw_attack_highlights(self.screen, attack_highlight_tiles, self.tile_size)
        draw_path_preview(self.screen, path_preview, self.tile_size)
        self.ui_system.render(self.units, self.turn_manager.current_camp)
        pygame.display.flip()

    def _should_show_action_menu(self) -> bool:
        # 中文注释：行动菜单仅在玩家回合且单位处于选中状态时显示。
        return (
            self.turn_manager.current_camp == PLAYER
            and self.player.state.alive
            and not self.player.state.acted
            and self.game_state == GameState.UNIT_SELECTED
        )
