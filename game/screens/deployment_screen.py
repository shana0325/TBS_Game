"""部署屏幕：玩家在战斗前放置出战单位。"""

from __future__ import annotations

import pygame

from game.battle.movement.grid import DualGrid
from game.core.game import BOTTOM_UI_RATIO, ENEMY_TEAM_ID, PLAYER_TEAM_ID
from game.levels.level.level_loader import load_level
from game.levels.scenario.scenario_loader import load_scenario
from game.levels.systems.spawn_system import SpawnSystem
from game.player.player_army import PlayerArmy
from game.render.map_renderer import TILE_SIZE, render_map
from game.screens.screen_base import ScreenBase

# 中文注释：部署区高亮颜色。
DEPLOYMENT_BORDER_COLOR = (80, 150, 255)
SELECTED_SLOT_BG = (70, 100, 145)
SLOT_BG = (50, 60, 75)
START_BTN_BG = (70, 130, 85)
START_BTN_DISABLED_BG = (75, 85, 95)

# 中文注释：与战斗屏幕保持一致的地形预设。
TERRAIN_PRESETS: dict[str, dict[str, int]] = {
    "plain": {"move_cost": 1, "defense_bonus": 0},
    "forest": {"move_cost": 2, "defense_bonus": 1},
}


class DeploymentScreen(ScreenBase):
    """部署 Screen：选择 roster 并放置到部署区。"""

    def __init__(self, manager: object, level_name: str, scenario_name: str) -> None:
        super().__init__(manager)
        self.level_name = level_name
        self.scenario_name = scenario_name

        self.level_data = load_level(level_name)
        self.scenario_data = load_scenario(scenario_name)

        self.grid = self._create_grid_from_level(self.level_data)
        self._apply_level_terrain(self.grid, self.level_data)

        # 中文注释：玩家部署名单来自全局 PlayerArmy，而不是 Scenario。
        self.roster = PlayerArmy().get_deployable_units()
        self.deployment_zone = list(self.level_data.get("deployment_zones", {}).get("player", []))

        if len(self.deployment_zone) < len(self.roster):
            raise ValueError("Deployment zone is smaller than player roster size")

        self.enemy_units = SpawnSystem.spawn_enemy_units(
            grid=self.grid,
            level_data=self.level_data,
            scenario_data=self.scenario_data,
            enemy_team_id=ENEMY_TEAM_ID,
        )

        # 中文注释：记录 roster 索引到部署坐标的映射。
        self.placements: dict[int, tuple[int, int]] = {}
        # 中文注释：记录部署格占用情况，便于交换与清理。
        self.cell_to_slot: dict[tuple[int, int], int] = {}
        self.selected_slot = 0

        self.tile_size = TILE_SIZE
        self.map_pixel_width = self.grid.width * self.tile_size
        self.map_pixel_height = self.grid.height * self.tile_size

        # 字体设置
        FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
        self.title_font = pygame.font.Font(FONT_PATH, 42)
        self.text_font = pygame.font.Font(FONT_PATH, 28)
        self.small_font = pygame.font.Font(FONT_PATH, 24)

        self.slot_rects: list[pygame.Rect] = []
        self.start_button_rect = pygame.Rect(0, 0, 0, 0)

        self._recalculate_layout()

    def _recalculate_layout(self) -> None:
        # 中文注释：按当前窗口尺寸重算部署界面布局，支持实时缩放。
        self.window_width = self.manager.screen.get_width()
        self.window_height = self.manager.screen.get_height()

        bottom_panel_height = max(160, int(self.window_height * BOTTOM_UI_RATIO))
        battlefield_height = self.window_height - bottom_panel_height

        self.battlefield_rect = pygame.Rect(0, 0, self.window_width, battlefield_height)
        self.bottom_panel_rect = pygame.Rect(0, battlefield_height, self.window_width, bottom_panel_height)
        self.roster_panel_rect = pygame.Rect(0, battlefield_height, int(self.window_width * 0.55), bottom_panel_height)
        self.action_panel_rect = pygame.Rect(
            self.roster_panel_rect.right,
            battlefield_height,
            self.window_width - self.roster_panel_rect.width,
            bottom_panel_height,
        )
        self.battlefield_origin = (
            self.battlefield_rect.x + (self.battlefield_rect.width - self.map_pixel_width) // 2,
            self.battlefield_rect.y + (self.battlefield_rect.height - self.map_pixel_height) // 2,
        )

        self.start_button_rect = pygame.Rect(
            self.action_panel_rect.x + max(12, int(self.action_panel_rect.width * 0.06)),
            self.action_panel_rect.y + max(20, int(self.action_panel_rect.height * 0.58)),
            max(180, int(self.action_panel_rect.width * 0.74)),
            max(42, int(self.action_panel_rect.height * 0.22)),
        )

    def _resize_window(self, width: int, height: int) -> None:
        self.manager.screen = pygame.display.set_mode((max(860, width), max(620, height)), pygame.RESIZABLE)
        self._recalculate_layout()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.running = False
                return

            if event.type == pygame.VIDEORESIZE:
                self._resize_window(event.w, event.h)
                continue
            if event.type == getattr(pygame, "WINDOWSIZECHANGED", -1):
                self._resize_window(event.x, event.y)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from game.screens.level_select_screen import LevelSelectScreen

                self.manager.switch_to(LevelSelectScreen(self.manager))
                return

            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue

            # 中文注释：点击 roster 槽位切换当前待部署单位。
            clicked_slot = self._get_clicked_slot(event.pos)
            if clicked_slot is not None:
                self.selected_slot = clicked_slot
                continue

            # 中文注释：所有单位部署完成后，点击按钮进入战斗。
            if self.start_button_rect.collidepoint(event.pos) and self._is_all_deployed():
                from game.screens.battle_screen import BattleScreen

                self.manager.switch_to(
                    BattleScreen(
                        manager=self.manager,
                        level_name=self.level_name,
                        scenario_name=self.scenario_name,
                        deployed_player_positions=self._ordered_deployment_positions(),
                    )
                )
                return

            # 中文注释：点击部署区格子，放置当前选中单位。
            target = self._screen_to_grid(event.pos)
            if target is None:
                continue
            if target not in self.deployment_zone:
                continue

            self._place_selected_slot(target)

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        screen.fill((245, 245, 245))

        preview_units = self._build_preview_player_units() + self.enemy_units
        render_map(
            screen,
            self.grid,
            preview_units,
            battlefield_rect=self.battlefield_rect,
            origin=self.battlefield_origin,
            tile_size=self.tile_size,
        )
        self._draw_deployment_highlights(screen)
        self._draw_bottom_ui(screen)

        pygame.display.flip()

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

    def _draw_deployment_highlights(self, screen: pygame.Surface) -> None:
        ox, oy = self.battlefield_origin
        for pos in self.deployment_zone:
            rect = pygame.Rect(
                ox + pos[0] * self.tile_size,
                oy + pos[1] * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            pygame.draw.rect(screen, DEPLOYMENT_BORDER_COLOR, rect, width=3)

    def _draw_bottom_ui(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (233, 237, 244), self.bottom_panel_rect)
        pygame.draw.rect(screen, (158, 170, 186), self.bottom_panel_rect, width=2)
        pygame.draw.rect(screen, (158, 170, 186), self.roster_panel_rect, width=1)
        pygame.draw.rect(screen, (158, 170, 186), self.action_panel_rect, width=1)

        title = self.title_font.render("Deployment", True, (30, 40, 55))
        screen.blit(title, (self.roster_panel_rect.x + 16, self.roster_panel_rect.y + 12))

        self.slot_rects = []
        start_y = self.roster_panel_rect.y + 60
        for idx, entry in enumerate(self.roster):
            slot_rect = pygame.Rect(self.roster_panel_rect.x + 16, start_y + idx * 44, self.roster_panel_rect.width - 32, 36)
            self.slot_rects.append(slot_rect)

            is_selected = idx == self.selected_slot
            bg_color = SELECTED_SLOT_BG if is_selected else SLOT_BG
            pygame.draw.rect(screen, bg_color, slot_rect)

            unit_type = str(entry.get("type", "Unknown"))
            placement = self.placements.get(idx)
            suffix = f" -> {placement}" if placement is not None else " -> 未部署"
            line = self.text_font.render(f"{idx + 1}. {unit_type}{suffix}", True, (235, 240, 250))
            screen.blit(line, (slot_rect.x + 10, slot_rect.y + 6))

        tips = self.small_font.render("点击左侧名单选择单位，再点击蓝色部署格放置", True, (48, 60, 78))
        screen.blit(tips, (self.roster_panel_rect.x + 16, self.roster_panel_rect.bottom - 34))

        can_start = self._is_all_deployed()
        btn_bg = START_BTN_BG if can_start else START_BTN_DISABLED_BG
        pygame.draw.rect(screen, btn_bg, self.start_button_rect)
        btn_text = self.text_font.render("Start Battle", True, (245, 250, 245))
        screen.blit(
            btn_text,
            (
                self.start_button_rect.x + (self.start_button_rect.width - btn_text.get_width()) // 2,
                self.start_button_rect.y + (self.start_button_rect.height - btn_text.get_height()) // 2,
            ),
        )

        state_text = "已全部部署，可开始战斗" if can_start else "请先完成全部单位部署"
        state_surface = self.small_font.render(state_text, True, (55, 70, 88))
        screen.blit(state_surface, (self.action_panel_rect.x + 24, self.action_panel_rect.y + 92))

    def _place_selected_slot(self, target_pos: tuple[int, int]) -> None:
        prev_pos = self.placements.get(self.selected_slot)
        if prev_pos is not None:
            self.cell_to_slot.pop(prev_pos, None)

        occupied_slot = self.cell_to_slot.get(target_pos)
        if occupied_slot is not None:
            self.placements.pop(occupied_slot, None)

        self.placements[self.selected_slot] = target_pos
        self.cell_to_slot[target_pos] = self.selected_slot

    def _build_preview_player_units(self) -> list[object]:
        roster = [self.roster[idx] for idx in sorted(self.placements.keys())]
        positions = [self.placements[idx] for idx in sorted(self.placements.keys())]
        if not roster:
            return []
        return SpawnSystem.spawn_player_units(
            grid=self.grid,
            roster=roster,
            deployment_positions=positions,
            player_team_id=PLAYER_TEAM_ID,
        )

    def _ordered_deployment_positions(self) -> list[tuple[int, int]]:
        return [self.placements[idx] for idx in range(len(self.roster))]

    def _is_all_deployed(self) -> bool:
        return len(self.placements) == len(self.roster)

    def _get_clicked_slot(self, pos: tuple[int, int]) -> int | None:
        for idx, rect in enumerate(self.slot_rects):
            if rect.collidepoint(pos):
                return idx
        return None

    def _screen_to_grid(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        if not self.battlefield_rect.collidepoint(pos):
            return None

        ox, oy = self.battlefield_origin
        local_x = pos[0] - ox
        local_y = pos[1] - oy
        if local_x < 0 or local_y < 0:
            return None

        grid_x = local_x // self.tile_size
        grid_y = local_y // self.tile_size
        tile = self.grid.get_tile(grid_x, grid_y)
        if tile is None:
            return None
        return (grid_x, grid_y)


