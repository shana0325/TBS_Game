"""角色成长屏幕：在战斗前为玩家角色分配属性点并学习技能。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.data.config_loader import ConfigLoader
from game.data.game_database import GameDatabase
from game.player.player_army import PlayerArmy
from game.screens.screen_base import ScreenBase
from game.ui.font_manager import get_font
from game.ui.language_shortcut import handle_language_toggle
from game.ui.scrollable_list import ScrollableList

LIST_ITEM_HEIGHT = 72
STAT_LINE_HEIGHT = 36
PANEL_CONTENT_TOP = 54
BUTTON_HEIGHT = 40
BUTTON_GAP = 12


class ProgressionScreen(ScreenBase):
    """角色成长 Screen。"""

    STAT_OPTIONS: list[tuple[str, str]] = [
        ("attack", "ATK"),
        ("defense", "DEF"),
        ("move", "MOVE"),
        ("hp", "HP"),
    ]

    def __init__(self, manager: object, return_screen: ScreenBase | None = None) -> None:
        super().__init__(manager)
        self.return_screen = return_screen
        self.player_army = PlayerArmy()
        self._game_db = GameDatabase(ConfigLoader())
        self.title_font = get_font(56)
        self.section_font = get_font(34)
        self.text_font = get_font(28)
        self.small_font = get_font(24)
        self.selected_unit_index = 0
        self.selected_skill_index = 0
        self.message = ""

        self.unit_scroller = ScrollableList(item_height=LIST_ITEM_HEIGHT)
        self.stat_scroller = ScrollableList(item_height=STAT_LINE_HEIGHT)
        self.skill_scroller = ScrollableList(item_height=LIST_ITEM_HEIGHT)

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

            if event.key == pygame.K_UP:
                self._move_unit_selection(-1)
                continue
            if event.key == pygame.K_DOWN:
                self._move_unit_selection(1)
                continue
            if event.key == pygame.K_LEFT:
                self._move_skill_selection(-1)
                continue
            if event.key == pygame.K_RIGHT:
                self._move_skill_selection(1)
                continue
            if event.key == pygame.K_a:
                self._apply_stat_point("attack")
                continue
            if event.key == pygame.K_s:
                self._apply_stat_point("defense")
                continue
            if event.key == pygame.K_d:
                self._apply_stat_point("move")
                continue
            if event.key == pygame.K_f:
                self._apply_stat_point("hp")
                continue
            if event.key == pygame.K_l:
                self._learn_selected_skill()
                continue
            if event.key == pygame.K_e:
                self._equip_selected_skill()
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

        left_rect, center_rect, right_rect = self._get_layout_rects(screen_width, screen_height)
        self._draw_panel(screen, left_rect, texts.PROGRESSION_PANEL_UNITS)
        self._draw_panel(screen, center_rect, texts.PROGRESSION_PANEL_STATS)
        self._draw_panel(screen, right_rect, texts.PROGRESSION_PANEL_SKILLS)

        self._render_unit_list(screen, left_rect)
        self._render_unit_details(screen, center_rect)
        self._render_skill_panel(screen, right_rect)
        self._render_bottom_buttons(screen, screen_width, screen_height)
        self._render_help(screen, screen_height)

        if self.message:
            message_surface = self.small_font.render(self.message, True, (255, 220, 150))
            screen.blit(message_surface, (36, screen_height - 34))

        pygame.display.flip()

    def _get_layout_rects(self, screen_width: int, screen_height: int) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        left_rect = pygame.Rect(36, 96, int(screen_width * 0.34), screen_height - 170)
        center_rect = pygame.Rect(left_rect.right + 20, 96, int(screen_width * 0.28), screen_height - 170)
        right_rect = pygame.Rect(center_rect.right + 20, 96, screen_width - center_rect.right - 56, screen_height - 170)
        return left_rect, center_rect, right_rect

    def _get_content_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect.x + 10, rect.y + PANEL_CONTENT_TOP, rect.width - 28, rect.height - PANEL_CONTENT_TOP - 12)

    def _get_skill_buttons_rects(self, right_rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
        button_width = max(90, (right_rect.width - 42) // 2)
        button_y = right_rect.bottom - BUTTON_HEIGHT - 14
        learn_rect = pygame.Rect(right_rect.x + 12, button_y, button_width, BUTTON_HEIGHT)
        equip_rect = pygame.Rect(learn_rect.right + BUTTON_GAP, button_y, button_width, BUTTON_HEIGHT)
        return learn_rect, equip_rect

    def _get_back_button_rect(self, screen_width: int, screen_height: int) -> pygame.Rect:
        return pygame.Rect(screen_width - 160, screen_height - 56, 116, 36)

    def _draw_panel(self, screen: pygame.Surface, rect: pygame.Rect, title: str) -> None:
        pygame.draw.rect(screen, (42, 50, 62), rect, border_radius=10)
        pygame.draw.rect(screen, (96, 112, 140), rect, width=2, border_radius=10)
        title_surface = self.section_font.render(title, True, (210, 225, 245))
        screen.blit(title_surface, (rect.x + 14, rect.y + 10))

    def _render_unit_list(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        units = self.player_army.get_units()
        view_rect = self._get_content_rect(rect)
        start, end = self.unit_scroller.get_visible_slice(len(units), view_rect)

        for visible_index, unit in enumerate(units[start:end]):
            index = start + visible_index
            item_rect = self._get_unit_item_rect(view_rect, visible_index)
            is_selected = index == self.selected_unit_index
            bg_color = (70, 92, 120) if is_selected else (54, 62, 76)
            pygame.draw.rect(screen, bg_color, item_rect, border_radius=8)
            pygame.draw.rect(screen, (128, 156, 196), item_rect, width=1, border_radius=8)

            name_surface = self.text_font.render(unit.unit_type, True, (240, 244, 252))
            level_surface = self.small_font.render(texts.format_progression_level_exp(unit.level, unit.exp), True, (190, 210, 232))
            point_surface = self.small_font.render(texts.format_progression_points(unit.stat_points, unit.skill_points), True, (210, 230, 180))
            screen.blit(name_surface, (item_rect.x + 10, item_rect.y + 8))
            screen.blit(level_surface, (item_rect.x + 10, item_rect.y + 33))
            screen.blit(point_surface, (item_rect.x + item_rect.width - 120, item_rect.y + 33))

        self.unit_scroller.draw_scrollbar(screen, view_rect, len(units))

    def _render_unit_details(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        unit = self._get_selected_unit()
        if unit is None:
            return

        entries = self._build_stat_entries(unit)
        view_rect = self._get_content_rect(rect)
        start, end = self.stat_scroller.get_visible_slice(len(entries), view_rect)

        for draw_index, entry in enumerate(entries[start:end]):
            line_y = view_rect.y + draw_index * STAT_LINE_HEIGHT
            if entry["kind"] == "spacer":
                continue

            surface = self.text_font.render(str(entry["text"]), True, (230, 236, 245))
            screen.blit(surface, (view_rect.x + 4, line_y))

            stat_name = entry.get("stat_name")
            if isinstance(stat_name, str):
                button_rect = self._get_stat_button_rect(view_rect, draw_index)
                self._draw_button(screen, button_rect, "+")

        self.stat_scroller.draw_scrollbar(screen, view_rect, len(entries))

    def _render_skill_panel(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        skills = self._get_available_skills()
        view_rect = self._get_content_rect(rect)
        learn_rect, equip_rect = self._get_skill_buttons_rects(rect)
        view_rect.height = max(40, learn_rect.y - view_rect.y - 12)

        if not skills:
            empty_surface = self.text_font.render(texts.PROGRESSION_NO_SKILLS, True, (210, 220, 235))
            screen.blit(empty_surface, (view_rect.x + 4, view_rect.y))
            self._draw_button(screen, learn_rect, texts.PROGRESSION_BUTTON_LEARN)
            self._draw_button(screen, equip_rect, texts.PROGRESSION_BUTTON_EQUIP)
            return

        selected_unit = self._get_selected_unit()
        learned_skills = selected_unit.learned_skills if selected_unit is not None else []
        equipped_skills = selected_unit.equipped_skills if selected_unit is not None else []
        start, end = self.skill_scroller.get_visible_slice(len(skills), view_rect)

        for visible_index, skill_id in enumerate(skills[start:end]):
            index = start + visible_index
            skill_data = self._game_db.get_skill(skill_id) or {}
            item_rect = self._get_skill_item_rect(view_rect, visible_index)
            is_selected = index == self.selected_skill_index
            bg_color = (108, 78, 52) if is_selected else (58, 62, 74)
            pygame.draw.rect(screen, bg_color, item_rect, border_radius=8)
            pygame.draw.rect(screen, (188, 164, 118), item_rect, width=1, border_radius=8)

            learned = skill_id in learned_skills
            equipped = skill_id in equipped_skills
            name_surface = self.text_font.render(texts.get_skill_name(skill_id), True, (245, 240, 228))
            range_surface = self.small_font.render(texts.format_range(int(skill_data.get('min_range', 1)), int(skill_data.get('max_range', 1))), True, (224, 210, 180))
            state_text = texts.PROGRESSION_SKILL_STATE_EQUIPPED if equipped else (texts.PROGRESSION_SKILL_STATE_LEARNED if learned else texts.PROGRESSION_SKILL_STATE_LOCKED)
            state_color = (170, 230, 170) if equipped else ((180, 210, 255) if learned else (220, 190, 170))
            state_surface = self.small_font.render(state_text, True, state_color)

            screen.blit(name_surface, (item_rect.x + 10, item_rect.y + 8))
            screen.blit(range_surface, (item_rect.x + 10, item_rect.y + 35))
            screen.blit(state_surface, (item_rect.right - 90, item_rect.y + 20))

        self.skill_scroller.draw_scrollbar(screen, view_rect, len(skills))
        self._render_selected_skill_description(screen, rect)
        self._draw_button(screen, learn_rect, texts.PROGRESSION_BUTTON_LEARN)
        self._draw_button(screen, equip_rect, texts.PROGRESSION_BUTTON_EQUIP)

    def _render_bottom_buttons(self, screen: pygame.Surface, screen_width: int, screen_height: int) -> None:
        self._draw_button(screen, self._get_back_button_rect(screen_width, screen_height), texts.PROGRESSION_BUTTON_BACK)

    def _render_help(self, screen: pygame.Surface, screen_height: int) -> None:
        help_surface = self.small_font.render(texts.PROGRESSION_HELP, True, (190, 205, 225))
        screen.blit(help_surface, (36, screen_height - 64))

    def _render_selected_skill_description(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        """渲染当前选中技能的说明与附带 Buff。"""
        skills = self._get_available_skills()
        if not skills:
            return

        skill_id = skills[self.selected_skill_index]
        skill_data = self._game_db.get_skill(skill_id) or {}
        learn_rect, _ = self._get_skill_buttons_rects(rect)
        desc_top = learn_rect.y - 88
        if desc_top <= rect.y + 70:
            return

        title_surface = self.small_font.render(texts.PROGRESSION_SKILL_DESCRIPTION, True, (220, 225, 236))
        screen.blit(title_surface, (rect.x + 14, desc_top))

        description = texts.get_skill_description(skill_id)
        buff_names = self._extract_buff_names(skill_data)
        if buff_names:
            description = f"{description}  {texts.PROGRESSION_SKILL_BUFFS}：{' / '.join(buff_names)}"

        text_rect = pygame.Rect(rect.x + 14, desc_top + 24, rect.width - 28, 58)
        self._draw_wrapped_text(screen, description, text_rect, self.small_font, (205, 214, 226))

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str) -> None:
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        bg_color = (102, 122, 150) if hovered else (78, 92, 112)
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, (180, 194, 218), rect, width=1, border_radius=8)
        text_surface = self.small_font.render(label, True, (240, 244, 252))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def _build_stat_entries(self, unit: object) -> list[dict[str, object]]:
        entries: list[dict[str, object]] = [
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
        left_rect, center_rect, right_rect = self._get_layout_rects(self.manager.screen.get_width(), self.manager.screen.get_height())
        units = self.player_army.get_units()
        selected_unit = self._get_selected_unit()
        stat_entries = self._build_stat_entries(selected_unit) if selected_unit is not None else []
        skills = self._get_available_skills()

        self.unit_scroller.handle_event(event, self._get_content_rect(left_rect), len(units))
        self.stat_scroller.handle_event(event, self._get_content_rect(center_rect), len(stat_entries))

        skill_view_rect = self._get_content_rect(right_rect)
        learn_rect, _ = self._get_skill_buttons_rects(right_rect)
        skill_view_rect.height = max(40, learn_rect.y - skill_view_rect.y - 12)
        self.skill_scroller.handle_event(event, skill_view_rect, len(skills))

    def _handle_mouse_click(self, pos: tuple[int, int]) -> None:
        screen_width = self.manager.screen.get_width()
        screen_height = self.manager.screen.get_height()
        left_rect, center_rect, right_rect = self._get_layout_rects(screen_width, screen_height)

        if self._handle_unit_click(pos, left_rect):
            return
        if self._handle_stat_click(pos, center_rect):
            return
        if self._handle_skill_click(pos, right_rect):
            return

        learn_rect, equip_rect = self._get_skill_buttons_rects(right_rect)
        if learn_rect.collidepoint(pos):
            self._learn_selected_skill()
            return
        if equip_rect.collidepoint(pos):
            self._equip_selected_skill()
            return

        if self._get_back_button_rect(screen_width, screen_height).collidepoint(pos):
            self._return_to_previous_screen()

    def _handle_unit_click(self, pos: tuple[int, int], left_rect: pygame.Rect) -> bool:
        units = self.player_army.get_units()
        view_rect = self._get_content_rect(left_rect)
        start, end = self.unit_scroller.get_visible_slice(len(units), view_rect)
        for visible_index in range(end - start):
            item_rect = self._get_unit_item_rect(view_rect, visible_index)
            if item_rect.collidepoint(pos):
                self.selected_unit_index = start + visible_index
                self.message = ""
                return True
        return False

    def _handle_stat_click(self, pos: tuple[int, int], center_rect: pygame.Rect) -> bool:
        unit = self._get_selected_unit()
        if unit is None:
            return False
        entries = self._build_stat_entries(unit)
        view_rect = self._get_content_rect(center_rect)
        start, end = self.stat_scroller.get_visible_slice(len(entries), view_rect)
        for draw_index, entry in enumerate(entries[start:end]):
            stat_name = entry.get("stat_name")
            if isinstance(stat_name, str) and self._get_stat_button_rect(view_rect, draw_index).collidepoint(pos):
                self._apply_stat_point(stat_name)
                return True
        return False

    def _handle_skill_click(self, pos: tuple[int, int], right_rect: pygame.Rect) -> bool:
        skills = self._get_available_skills()
        view_rect = self._get_content_rect(right_rect)
        learn_rect, _ = self._get_skill_buttons_rects(right_rect)
        view_rect.height = max(40, learn_rect.y - view_rect.y - 12)
        start, end = self.skill_scroller.get_visible_slice(len(skills), view_rect)
        for visible_index in range(end - start):
            item_rect = self._get_skill_item_rect(view_rect, visible_index)
            if item_rect.collidepoint(pos):
                self.selected_skill_index = start + visible_index
                self.message = ""
                return True
        return False

    def _get_unit_item_rect(self, view_rect: pygame.Rect, visible_index: int) -> pygame.Rect:
        return pygame.Rect(view_rect.x, view_rect.y + visible_index * LIST_ITEM_HEIGHT, view_rect.width, 62)

    def _get_skill_item_rect(self, view_rect: pygame.Rect, visible_index: int) -> pygame.Rect:
        return pygame.Rect(view_rect.x, view_rect.y + visible_index * LIST_ITEM_HEIGHT, view_rect.width, 62)

    def _get_stat_button_rect(self, view_rect: pygame.Rect, draw_index: int) -> pygame.Rect:
        return pygame.Rect(view_rect.right - 44, view_rect.y + draw_index * STAT_LINE_HEIGHT + 2, 36, 28)

    def _get_selected_unit(self):
        units = self.player_army.get_units()
        if not units:
            return None
        self.selected_unit_index = max(0, min(self.selected_unit_index, len(units) - 1))
        left_rect, _, _ = self._get_layout_rects(self.manager.screen.get_width(), self.manager.screen.get_height())
        self.unit_scroller.ensure_visible(self.selected_unit_index, len(units), self._get_content_rect(left_rect))
        return units[self.selected_unit_index]

    def _extract_buff_names(self, skill_data: dict[str, object]) -> list[str]:
        """提取技能效果中引用的 Buff 文案。"""
        names: list[str] = []
        for effect in skill_data.get("effects", []):
            if not isinstance(effect, dict) or effect.get("type") != "buff":
                continue
            buff_id = str(effect.get("buff", effect.get("name", "")))
            if not buff_id:
                continue
            names.append(texts.get_buff_name(buff_id))
        return names

    def _draw_wrapped_text(
        self,
        screen: pygame.Surface,
        text: str,
        rect: pygame.Rect,
        font: pygame.font.Font,
        color: tuple[int, int, int],
    ) -> None:
        """按像素宽度换行渲染短说明。"""
        line = ""
        y = rect.y
        for ch in text:
            candidate = line + ch
            if font.size(candidate)[0] <= rect.width:
                line = candidate
                continue
            if y + font.get_height() > rect.bottom:
                break
            screen.blit(font.render(line, True, color), (rect.x, y))
            y += font.get_height() + 2
            line = ch
        if line and y + font.get_height() <= rect.bottom:
            screen.blit(font.render(line, True, color), (rect.x, y))

    def _get_available_skills(self) -> list[str]:
        skill_ids = sorted(self._game_db.skills.keys())
        if not skill_ids:
            self.selected_skill_index = 0
            return []
        self.selected_skill_index = max(0, min(self.selected_skill_index, len(skill_ids) - 1))
        _, _, right_rect = self._get_layout_rects(self.manager.screen.get_width(), self.manager.screen.get_height())
        skill_view_rect = self._get_content_rect(right_rect)
        learn_rect, _ = self._get_skill_buttons_rects(right_rect)
        skill_view_rect.height = max(40, learn_rect.y - skill_view_rect.y - 12)
        self.skill_scroller.ensure_visible(self.selected_skill_index, len(skill_ids), skill_view_rect)
        return skill_ids

    def _move_unit_selection(self, offset: int) -> None:
        units = self.player_army.get_units()
        if not units:
            return
        self.selected_unit_index = (self.selected_unit_index + offset) % len(units)
        left_rect, _, _ = self._get_layout_rects(self.manager.screen.get_width(), self.manager.screen.get_height())
        self.unit_scroller.ensure_visible(self.selected_unit_index, len(units), self._get_content_rect(left_rect))
        self.message = ""

    def _move_skill_selection(self, offset: int) -> None:
        skills = self._get_available_skills()
        if not skills:
            return
        self.selected_skill_index = (self.selected_skill_index + offset) % len(skills)
        _, _, right_rect = self._get_layout_rects(self.manager.screen.get_width(), self.manager.screen.get_height())
        skill_view_rect = self._get_content_rect(right_rect)
        learn_rect, _ = self._get_skill_buttons_rects(right_rect)
        skill_view_rect.height = max(40, learn_rect.y - skill_view_rect.y - 12)
        self.skill_scroller.ensure_visible(self.selected_skill_index, len(skills), skill_view_rect)
        self.message = ""

    def _apply_stat_point(self, stat_name: str) -> None:
        unit = self._get_selected_unit()
        if unit is None:
            return
        if self.player_army.spend_stat_point(unit.unit_id, stat_name):
            self.message = texts.format_progression_message_gain(unit.unit_type, stat_name)
        else:
            self.message = texts.format_progression_message_no_stat_points(unit.unit_type)

    def _learn_selected_skill(self) -> None:
        unit = self._get_selected_unit()
        skills = self._get_available_skills()
        if unit is None or not skills:
            return
        skill_id = skills[self.selected_skill_index]
        if self.player_army.learn_skill(unit.unit_id, skill_id):
            self.message = texts.format_progression_message_learn(unit.unit_type, skill_id)
        else:
            self.message = texts.format_progression_message_cannot_learn(skill_id)

    def _equip_selected_skill(self) -> None:
        unit = self._get_selected_unit()
        skills = self._get_available_skills()
        if unit is None or not skills:
            return
        skill_id = skills[self.selected_skill_index]
        if self.player_army.equip_skill(unit.unit_id, skill_id):
            self.message = texts.format_progression_message_equip(unit.unit_type, skill_id)
        else:
            self.message = texts.format_progression_message_cannot_equip(skill_id)

    def _return_to_previous_screen(self) -> None:
        if self.return_screen is not None:
            self.manager.switch_to(self.return_screen)
            return
        from game.screens.level_select_screen import LevelSelectScreen
        self.manager.switch_to(LevelSelectScreen(self.manager))





