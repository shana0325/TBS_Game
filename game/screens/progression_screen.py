"""角色成长屏幕：负责单角色成长页签切换、属性/技能/装备操作。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.data.config_loader import ConfigLoader
from game.data.game_database import GameDatabase
from game.player.player_army import PlayerArmy
from game.screens.screen_base import ScreenBase
from game.ui.font_manager import get_font
from game.ui.language_shortcut import handle_language_toggle
from game.ui.progression_equipment_panel import ProgressionEquipmentPanel
from game.ui.progression_skill_panel import ProgressionSkillPanel
from game.ui.progression_stat_panel import ProgressionStatPanel
from game.ui.progression_tabs import ProgressionTabs
from game.ui.progression_unit_summary_panel import ProgressionUnitSummaryPanel

PANEL_CONTENT_TOP = 54
TAB_BAR_HEIGHT = 56


class ProgressionScreen(ScreenBase):
    """单角色成长 Screen。"""

    STAT_OPTIONS: list[tuple[str, str]] = [
        ("attack", "ATK"),
        ("defense", "DEF"),
        ("move", "MOVE"),
        ("hp", "HP"),
    ]

    def __init__(self, manager: object, unit_id: str, return_screen: ScreenBase | None = None) -> None:
        super().__init__(manager)
        self.return_screen = return_screen
        self.player_army = PlayerArmy()
        self._game_db = GameDatabase(ConfigLoader())
        self.title_font = get_font(56)
        self.section_font = get_font(34)
        self.text_font = get_font(28)
        self.small_font = get_font(24)

        self.unit_id = unit_id
        self.selected_skill_index = 0
        self.selected_equipment_index = 0
        self.selected_equipment_slot = "weapon"
        self.current_tab = "stats"
        self.message = ""

        self.tabs = ProgressionTabs(self.small_font)
        self.summary_panel = ProgressionUnitSummaryPanel(self.section_font, self.text_font, self.small_font)
        self.stat_panel = ProgressionStatPanel(self.text_font, self.small_font)
        self.skill_panel = ProgressionSkillPanel(self.text_font, self.small_font)
        self.equipment_panel = ProgressionEquipmentPanel(self.text_font, self.small_font)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.running = False
                return
            if event.type == pygame.VIDEORESIZE:
                self.manager.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                continue
            if event.type == getattr(pygame, "WINDOWSIZECHANGED", -1):
                self.manager.screen = pygame.display.set_mode((event.x, event.y), pygame.RESIZABLE)
                continue
            if event.type in (pygame.MOUSEWHEEL, pygame.MOUSEBUTTONDOWN):
                self._handle_scroll_event(event)
                if event.type == pygame.MOUSEWHEEL:
                    continue
                if event.button in (4, 5):
                    continue
                if event.button == 1:
                    self._handle_mouse_click(event.pos)
                    continue
            if handle_language_toggle(event):
                continue
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_1, pygame.K_F1):
                self.current_tab = "stats"
                continue
            if event.key in (pygame.K_2, pygame.K_F2):
                self.current_tab = "skills"
                continue
            if event.key in (pygame.K_3, pygame.K_F3):
                self.current_tab = "equipment"
                continue
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self._return_to_previous_screen()
                return

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        screen.fill((22, 28, 36))

        title_surface = self.title_font.render(texts.PROGRESSION_TITLE, True, (236, 240, 248))
        screen.blit(title_surface, (36, 24))

        left_rect, right_rect = self._get_layout_rects(screen_width, screen_height)
        self._draw_panel(screen, left_rect, texts.PROGRESSION_SUMMARY_TITLE)
        self._draw_panel(screen, right_rect, texts.PROGRESSION_PANEL_SKILLS)

        unit = self._get_selected_unit()
        if unit is not None:
            self.summary_panel.render(screen, self._get_content_rect(left_rect), unit)
            tab_bar_rect = self._get_tab_bar_rect(right_rect)
            self.tabs.render(screen, tab_bar_rect, self.current_tab)
            self._render_active_panel(screen, right_rect, unit)

        self._render_bottom_buttons(screen, screen_width, screen_height)
        self._render_help(screen, screen_height)

        if self.message:
            message_surface = self.small_font.render(self.message, True, (255, 220, 150))
            screen.blit(message_surface, (36, screen_height - 34))

        pygame.display.flip()

    def _get_layout_rects(self, screen_width: int, screen_height: int) -> tuple[pygame.Rect, pygame.Rect]:
        left_rect = pygame.Rect(36, 96, int(screen_width * 0.32), screen_height - 170)
        right_rect = pygame.Rect(left_rect.right + 20, 96, screen_width - left_rect.right - 56, screen_height - 170)
        return left_rect, right_rect

    def _get_content_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect.x + 10, rect.y + PANEL_CONTENT_TOP, rect.width - 28, rect.height - PANEL_CONTENT_TOP - 12)

    def _get_tab_bar_rect(self, right_rect: pygame.Rect) -> pygame.Rect:
        content_rect = self._get_content_rect(right_rect)
        return pygame.Rect(content_rect.x, content_rect.y, content_rect.width, TAB_BAR_HEIGHT)

    def _get_active_panel_rect(self, right_rect: pygame.Rect) -> pygame.Rect:
        content_rect = self._get_content_rect(right_rect)
        return pygame.Rect(content_rect.x, content_rect.y + TAB_BAR_HEIGHT + 8, content_rect.width, content_rect.height - TAB_BAR_HEIGHT - 8)

    def _get_back_button_rect(self, screen_width: int, screen_height: int) -> pygame.Rect:
        return pygame.Rect(screen_width - 160, screen_height - 56, 116, 36)

    def _draw_panel(self, screen: pygame.Surface, rect: pygame.Rect, title: str) -> None:
        pygame.draw.rect(screen, (42, 50, 62), rect, border_radius=10)
        pygame.draw.rect(screen, (96, 112, 140), rect, width=2, border_radius=10)
        title_surface = self.section_font.render(title, True, (210, 225, 245))
        screen.blit(title_surface, (rect.x + 14, rect.y + 10))

    def _render_active_panel(self, screen: pygame.Surface, right_rect: pygame.Rect, unit: object) -> None:
        panel_rect = self._get_active_panel_rect(right_rect)
        if self.current_tab == "stats":
            self.stat_panel.render(screen, panel_rect, self._build_stat_entries(unit))
        elif self.current_tab == "skills":
            self.skill_panel.render(screen, panel_rect, self._get_available_skills(), self.selected_skill_index, unit.learned_skills, unit.equipped_skills, self._game_db)
        else:
            self.equipment_panel.render(screen, panel_rect, unit, self.selected_equipment_slot, self._get_available_equipments(), self.selected_equipment_index, self._game_db)

    def _render_bottom_buttons(self, screen: pygame.Surface, screen_width: int, screen_height: int) -> None:
        rect = self._get_back_button_rect(screen_width, screen_height)
        pygame.draw.rect(screen, (78, 92, 112), rect, border_radius=8)
        pygame.draw.rect(screen, (180, 194, 218), rect, width=1, border_radius=8)
        text_surface = self.small_font.render(texts.PROGRESSION_BUTTON_BACK, True, (240, 244, 252))
        screen.blit(text_surface, text_surface.get_rect(center=rect.center))

    def _render_help(self, screen: pygame.Surface, screen_height: int) -> None:
        help_surface = self.small_font.render(texts.PROGRESSION_HELP, True, (190, 205, 225))
        screen.blit(help_surface, (36, screen_height - 64))

    def _build_stat_entries(self, unit: object) -> list[dict[str, object]]:
        entries = [
            {"kind": "text", "text": f"{texts.PROGRESSION_NAME}: {unit.unit_type}"},
            {"kind": "text", "text": f"{texts.PROGRESSION_LEVEL}: {unit.level}"},
            {"kind": "text", "text": f"{texts.PROGRESSION_EXP}: {unit.exp}"},
            {"kind": "text", "text": f"{texts.PROGRESSION_STAT_POINTS}: {unit.stat_points}"},
            {"kind": "text", "text": f"{texts.PROGRESSION_SKILL_POINTS}: {unit.skill_points}"},
            {"kind": "spacer", "text": ""},
            {"kind": "text", "text": texts.PROGRESSION_STATS_HEADER},
        ]
        for stat_key, label in self.STAT_OPTIONS:
            value = unit.allocated_stats.get(stat_key, 0)
            entries.append({"kind": "stat", "text": texts.format_stat_line(label, value), "stat_name": stat_key})
        entries.extend([
            {"kind": "spacer", "text": ""},
            {"kind": "text", "text": f"{texts.PROGRESSION_LEARNED_COUNT}: {len(unit.learned_skills)}"},
            {"kind": "text", "text": f"{texts.PROGRESSION_EQUIPPED_COUNT}: {len(unit.equipped_skills)}"},
        ])
        return entries

    def _handle_scroll_event(self, event: pygame.event.Event) -> None:
        _, right_rect = self._get_layout_rects(self.manager.screen.get_width(), self.manager.screen.get_height())
        panel_rect = self._get_active_panel_rect(right_rect)
        if self.current_tab == "stats":
            unit = self._get_selected_unit()
            entries = self._build_stat_entries(unit) if unit is not None else []
            self.stat_panel.handle_scroll(event, panel_rect, entries)
        elif self.current_tab == "skills":
            self.skill_panel.handle_scroll(event, panel_rect, self._get_available_skills())
        else:
            self.equipment_panel.handle_scroll(event, panel_rect, self._get_available_equipments())

    def _handle_mouse_click(self, pos: tuple[int, int]) -> None:
        screen_width = self.manager.screen.get_width()
        screen_height = self.manager.screen.get_height()
        _, right_rect = self._get_layout_rects(screen_width, screen_height)
        tab = self.tabs.get_clicked_tab(pos, self._get_tab_bar_rect(right_rect))
        if tab is not None:
            self.current_tab = tab
            self.message = ""
            return
        if self._get_back_button_rect(screen_width, screen_height).collidepoint(pos):
            self._return_to_previous_screen()
            return
        panel_rect = self._get_active_panel_rect(right_rect)
        if self.current_tab == "stats":
            self._handle_stat_panel_click(pos, panel_rect)
        elif self.current_tab == "skills":
            self._handle_skill_panel_click(pos, panel_rect)
        else:
            self._handle_equipment_panel_click(pos, panel_rect)

    def _handle_stat_panel_click(self, pos: tuple[int, int], panel_rect: pygame.Rect) -> None:
        unit = self._get_selected_unit()
        if unit is None:
            return
        stat_name = self.stat_panel.handle_click(pos, panel_rect, self._build_stat_entries(unit))
        if stat_name is None:
            return
        if self.player_army.spend_stat_point(unit.unit_id, stat_name):
            self.message = texts.format_progression_message_gain(unit.unit_type, stat_name)
        else:
            self.message = texts.format_progression_message_no_stat_points(unit.unit_type)

    def _handle_skill_panel_click(self, pos: tuple[int, int], panel_rect: pygame.Rect) -> None:
        unit = self._get_selected_unit()
        if unit is None:
            return
        result = self.skill_panel.handle_click(pos, panel_rect, self._get_available_skills())
        if result is None:
            return
        action, value = result
        if action == "select":
            self.selected_skill_index = int(value)
            self.message = ""
            return
        skill_id = self._get_available_skills()[self.selected_skill_index]
        if value == "learn":
            self.message = texts.format_progression_message_learn(unit.unit_type, skill_id) if self.player_army.learn_skill(unit.unit_id, skill_id) else texts.format_progression_message_cannot_learn(skill_id)
        else:
            self.message = texts.format_progression_message_equip(unit.unit_type, skill_id) if self.player_army.equip_skill(unit.unit_id, skill_id) else texts.format_progression_message_cannot_equip(skill_id)

    def _handle_equipment_panel_click(self, pos: tuple[int, int], panel_rect: pygame.Rect) -> None:
        unit = self._get_selected_unit()
        if unit is None:
            return
        result = self.equipment_panel.handle_click(pos, panel_rect, self._get_available_equipments())
        if result is None:
            return
        action, value = result
        if action == "slot":
            self.selected_equipment_slot = str(value)
            self.selected_equipment_index = 0
            self.message = ""
            return
        if action == "select":
            self.selected_equipment_index = int(value)
            self.message = ""
            return
        slot_name = texts.get_slot_name(self.selected_equipment_slot)
        if value == "equip":
            equipments = self._get_available_equipments()
            if not equipments:
                return
            equipment_id = equipments[self.selected_equipment_index]
            self.message = texts.format_progression_message_item_equip(unit.unit_type, equipment_id, slot_name) if self.player_army.equip_item(unit.unit_id, self.selected_equipment_slot, equipment_id) else texts.format_progression_message_item_cannot_equip(equipment_id)
        else:
            self.message = texts.format_progression_message_item_unequip(unit.unit_type, slot_name) if self.player_army.unequip_item(unit.unit_id, self.selected_equipment_slot) else texts.format_progression_message_item_cannot_unequip(slot_name)

    def _get_selected_unit(self):
        unit = self.player_army.find_unit(self.unit_id)
        if unit is not None:
            return unit
        units = self.player_army.get_units()
        return units[0] if units else None

    def _get_available_skills(self) -> list[str]:
        skill_ids = sorted(self._game_db.skills.keys())
        if not skill_ids:
            self.selected_skill_index = 0
            return []
        self.selected_skill_index = max(0, min(self.selected_skill_index, len(skill_ids) - 1))
        return skill_ids

    def _get_available_equipments(self) -> list[str]:
        equipment_ids = [equipment_id for equipment_id, equipment_data in sorted(self._game_db.equipments.items()) if str(equipment_data.get("slot", "")).strip().lower() == self.selected_equipment_slot]
        if not equipment_ids:
            self.selected_equipment_index = 0
            return []
        self.selected_equipment_index = max(0, min(self.selected_equipment_index, len(equipment_ids) - 1))
        return equipment_ids

    def _return_to_previous_screen(self) -> None:
        if self.return_screen is not None:
            self.manager.switch_to(self.return_screen)
            return
        from game.screens.progression_character_select_screen import ProgressionCharacterSelectScreen
        self.manager.switch_to(ProgressionCharacterSelectScreen(self.manager))
