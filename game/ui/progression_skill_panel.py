"""成长技能面板：负责技能页的渲染与交互。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.ui.scrollable_list import ScrollableList

LIST_ITEM_HEIGHT = 72
BUTTON_HEIGHT = 40
BUTTON_GAP = 12


class ProgressionSkillPanel:
    """技能页面板。"""

    def __init__(self, text_font: pygame.font.Font, small_font: pygame.font.Font) -> None:
        self.text_font = text_font
        self.small_font = small_font
        self.scroller = ScrollableList(item_height=LIST_ITEM_HEIGHT)

    def get_list_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect.x, rect.y + 28, rect.width, max(80, rect.height - 28 - BUTTON_HEIGHT - 76))

    def get_button_rects(self, rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
        width = max(90, (rect.width - BUTTON_GAP) // 2)
        y = rect.bottom - BUTTON_HEIGHT
        learn = pygame.Rect(rect.x, y, width, BUTTON_HEIGHT)
        equip = pygame.Rect(learn.right + BUTTON_GAP, y, width, BUTTON_HEIGHT)
        return learn, equip

    def render(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        skills: list[str],
        selected_index: int,
        learned_skills: list[str],
        equipped_skills: list[str],
        game_db: object,
    ) -> None:
        header = self.small_font.render(texts.PROGRESSION_SKILL_SECTION, True, (220, 225, 236))
        screen.blit(header, (rect.x, rect.y))
        list_rect = self.get_list_rect(rect)
        learn_rect, equip_rect = self.get_button_rects(rect)
        if not skills:
            empty_surface = self.text_font.render(texts.PROGRESSION_NO_SKILLS, True, (210, 220, 235))
            screen.blit(empty_surface, (list_rect.x + 4, list_rect.y))
            self._draw_button(screen, learn_rect, texts.PROGRESSION_BUTTON_LEARN)
            self._draw_button(screen, equip_rect, texts.PROGRESSION_BUTTON_EQUIP)
            return

        start, end = self.scroller.get_visible_slice(len(skills), list_rect)
        for visible_index, skill_id in enumerate(skills[start:end]):
            index = start + visible_index
            skill_data = game_db.get_skill(skill_id) or {}
            item_rect = pygame.Rect(list_rect.x, list_rect.y + visible_index * LIST_ITEM_HEIGHT, list_rect.width, 62)
            is_selected = index == selected_index
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

        self.scroller.draw_scrollbar(screen, list_rect, len(skills))
        self._render_description(screen, rect, skills, selected_index, game_db)
        self._draw_button(screen, learn_rect, texts.PROGRESSION_BUTTON_LEARN)
        self._draw_button(screen, equip_rect, texts.PROGRESSION_BUTTON_EQUIP)

    def handle_scroll(self, event: pygame.event.Event, rect: pygame.Rect, skills: list[str]) -> None:
        self.scroller.handle_event(event, self.get_list_rect(rect), len(skills))

    def handle_click(self, pos: tuple[int, int], rect: pygame.Rect, skills: list[str]) -> tuple[str, int | str] | None:
        list_rect = self.get_list_rect(rect)
        start, end = self.scroller.get_visible_slice(len(skills), list_rect)
        for visible_index in range(end - start):
            item_rect = pygame.Rect(list_rect.x, list_rect.y + visible_index * LIST_ITEM_HEIGHT, list_rect.width, 62)
            if item_rect.collidepoint(pos):
                return ("select", start + visible_index)
        learn_rect, equip_rect = self.get_button_rects(rect)
        if learn_rect.collidepoint(pos):
            return ("action", "learn")
        if equip_rect.collidepoint(pos):
            return ("action", "equip")
        return None

    def ensure_visible(self, index: int, total: int, rect: pygame.Rect) -> None:
        self.scroller.ensure_visible(index, total, self.get_list_rect(rect))

    def _render_description(self, screen: pygame.Surface, rect: pygame.Rect, skills: list[str], selected_index: int, game_db: object) -> None:
        if not skills:
            return
        skill_id = skills[selected_index]
        skill_data = game_db.get_skill(skill_id) or {}
        learn_rect, _ = self.get_button_rects(rect)
        top = learn_rect.y - 60
        if top <= rect.y + 40:
            return
        title = self.small_font.render(texts.PROGRESSION_SKILL_DESCRIPTION, True, (220, 225, 236))
        screen.blit(title, (rect.x, top))
        description = texts.get_skill_description(skill_id)
        buff_names: list[str] = []
        for effect in skill_data.get("effects", []):
            if isinstance(effect, dict) and effect.get("type") == "buff":
                buff_id = str(effect.get("buff", effect.get("name", "")))
                if buff_id:
                    buff_names.append(texts.get_buff_name(buff_id))
        if buff_names:
            description = f"{description}  {texts.PROGRESSION_SKILL_BUFFS}：{' / '.join(buff_names)}"
        self._draw_wrapped_text(screen, description, pygame.Rect(rect.x, top + 22, rect.width, 40), (205, 214, 226))

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str) -> None:
        pygame.draw.rect(screen, (78, 92, 112), rect, border_radius=8)
        pygame.draw.rect(screen, (180, 194, 218), rect, width=1, border_radius=8)
        text_surface = self.small_font.render(label, True, (240, 244, 252))
        screen.blit(text_surface, text_surface.get_rect(center=rect.center))

    def _draw_wrapped_text(self, screen: pygame.Surface, text: str, rect: pygame.Rect, color: tuple[int, int, int]) -> None:
        line = ""
        y = rect.y
        for ch in text:
            candidate = line + ch
            if self.small_font.size(candidate)[0] <= rect.width:
                line = candidate
                continue
            if y + self.small_font.get_height() > rect.bottom:
                break
            screen.blit(self.small_font.render(line, True, color), (rect.x, y))
            y += self.small_font.get_height() + 2
            line = ch
        if line and y + self.small_font.get_height() <= rect.bottom:
            screen.blit(self.small_font.render(line, True, color), (rect.x, y))
