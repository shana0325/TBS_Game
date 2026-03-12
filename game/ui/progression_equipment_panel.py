"""成长装备面板：负责装备页的渲染与交互。"""

from __future__ import annotations

import pygame

from game.core import texts
from game.player.equipment_system import EquipmentSystem
from game.ui.scrollable_list import ScrollableList

LIST_ITEM_HEIGHT = 72
SLOT_ITEM_HEIGHT = 46
BUTTON_HEIGHT = 40
BUTTON_GAP = 12


class ProgressionEquipmentPanel:
    """装备页面板。"""

    def __init__(self, text_font: pygame.font.Font, small_font: pygame.font.Font) -> None:
        self.text_font = text_font
        self.small_font = small_font
        self.scroller = ScrollableList(item_height=LIST_ITEM_HEIGHT)

    def get_slot_area_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect.x, rect.y + 8, rect.width, 176)

    def get_list_rect(self, rect: pygame.Rect) -> pygame.Rect:
        slot_area = self.get_slot_area_rect(rect)
        return pygame.Rect(rect.x, slot_area.bottom + 40, rect.width, max(70, rect.height - slot_area.height - BUTTON_HEIGHT - 120))

    def get_button_rects(self, rect: pygame.Rect) -> tuple[pygame.Rect, pygame.Rect]:
        width = max(90, (rect.width - BUTTON_GAP) // 2)
        y = rect.bottom - BUTTON_HEIGHT
        equip = pygame.Rect(rect.x, y, width, BUTTON_HEIGHT)
        unequip = pygame.Rect(equip.right + BUTTON_GAP, y, width, BUTTON_HEIGHT)
        return equip, unequip

    def render(self, screen: pygame.Surface, rect: pygame.Rect, unit: object, selected_slot: str, equipments: list[str], selected_index: int, game_db: object) -> None:
        header = self.small_font.render(texts.PROGRESSION_EQUIPMENT_SLOTS, True, (220, 225, 236))
        screen.blit(header, (rect.x, rect.y))
        slot_rect = self.get_slot_area_rect(rect)
        for index, slot in enumerate(EquipmentSystem.VALID_SLOTS):
            item_rect = pygame.Rect(slot_rect.x, slot_rect.y + 24 + index * SLOT_ITEM_HEIGHT, slot_rect.width, 38)
            is_selected = slot == selected_slot
            bg_color = (82, 96, 122) if is_selected else (56, 62, 78)
            pygame.draw.rect(screen, bg_color, item_rect, border_radius=8)
            pygame.draw.rect(screen, (138, 154, 186), item_rect, width=1, border_radius=8)
            equipment_id = unit.equipment.get(slot)
            equipment_name = texts.get_equipment_name(equipment_id) if equipment_id else texts.PROGRESSION_EQUIP_STATE_EMPTY
            line = texts.format_equipment_line(texts.get_slot_name(slot), equipment_name)
            line_surface = self.small_font.render(line, True, (236, 240, 248))
            screen.blit(line_surface, (item_rect.x + 10, item_rect.y + 10))

        title = self.small_font.render(texts.PROGRESSION_EQUIPMENT_SECTION, True, (220, 225, 236))
        list_rect = self.get_list_rect(rect)
        screen.blit(title, (list_rect.x, list_rect.y - 26))
        equip_rect, unequip_rect = self.get_button_rects(rect)
        if not equipments:
            empty_surface = self.small_font.render(texts.PROGRESSION_NO_EQUIPMENT, True, (210, 220, 235))
            screen.blit(empty_surface, (list_rect.x + 4, list_rect.y + 4))
            self._draw_button(screen, equip_rect, texts.PROGRESSION_BUTTON_EQUIP)
            self._draw_button(screen, unequip_rect, texts.PROGRESSION_BUTTON_UNEQUIP)
            return

        equipped_id = unit.equipment.get(selected_slot)
        start, end = self.scroller.get_visible_slice(len(equipments), list_rect)
        for visible_index, equipment_id in enumerate(equipments[start:end]):
            index = start + visible_index
            equipment_data = game_db.get_equipment(equipment_id) or {}
            item_rect = pygame.Rect(list_rect.x, list_rect.y + visible_index * LIST_ITEM_HEIGHT, list_rect.width, 62)
            is_selected = index == selected_index
            bg_color = (72, 92, 84) if is_selected else (58, 62, 74)
            pygame.draw.rect(screen, bg_color, item_rect, border_radius=8)
            pygame.draw.rect(screen, (146, 182, 156), item_rect, width=1, border_radius=8)
            state_text = texts.PROGRESSION_EQUIP_STATE_EQUIPPED if equipment_id == equipped_id else texts.PROGRESSION_EQUIP_STATE_AVAILABLE
            state_color = (170, 230, 170) if equipment_id == equipped_id else (210, 220, 235)
            name_surface = self.text_font.render(texts.get_equipment_name(equipment_id), True, (236, 240, 248))
            slot_surface = self.small_font.render(texts.get_slot_name(str(equipment_data.get('slot', selected_slot))), True, (196, 212, 220))
            state_surface = self.small_font.render(state_text, True, state_color)
            screen.blit(name_surface, (item_rect.x + 10, item_rect.y + 8))
            screen.blit(slot_surface, (item_rect.x + 10, item_rect.y + 35))
            screen.blit(state_surface, (item_rect.right - 92, item_rect.y + 20))

        self.scroller.draw_scrollbar(screen, list_rect, len(equipments))
        self._render_description(screen, rect, equipments, selected_index)
        self._draw_button(screen, equip_rect, texts.PROGRESSION_BUTTON_EQUIP)
        self._draw_button(screen, unequip_rect, texts.PROGRESSION_BUTTON_UNEQUIP)

    def handle_scroll(self, event: pygame.event.Event, rect: pygame.Rect, equipments: list[str]) -> None:
        self.scroller.handle_event(event, self.get_list_rect(rect), len(equipments))

    def handle_click(self, pos: tuple[int, int], rect: pygame.Rect, equipments: list[str]) -> tuple[str, str | int] | None:
        slot_rect = self.get_slot_area_rect(rect)
        for index, slot in enumerate(EquipmentSystem.VALID_SLOTS):
            item_rect = pygame.Rect(slot_rect.x, slot_rect.y + 24 + index * SLOT_ITEM_HEIGHT, slot_rect.width, 38)
            if item_rect.collidepoint(pos):
                return ("slot", slot)
        list_rect = self.get_list_rect(rect)
        start, end = self.scroller.get_visible_slice(len(equipments), list_rect)
        for visible_index in range(end - start):
            item_rect = pygame.Rect(list_rect.x, list_rect.y + visible_index * LIST_ITEM_HEIGHT, list_rect.width, 62)
            if item_rect.collidepoint(pos):
                return ("select", start + visible_index)
        equip_rect, unequip_rect = self.get_button_rects(rect)
        if equip_rect.collidepoint(pos):
            return ("action", "equip")
        if unequip_rect.collidepoint(pos):
            return ("action", "unequip")
        return None

    def ensure_visible(self, index: int, total: int, rect: pygame.Rect) -> None:
        self.scroller.ensure_visible(index, total, self.get_list_rect(rect))

    def _render_description(self, screen: pygame.Surface, rect: pygame.Rect, equipments: list[str], selected_index: int) -> None:
        if not equipments:
            return
        equip_rect, _ = self.get_button_rects(rect)
        top = equip_rect.y - 54
        if top <= rect.y + 220:
            return
        equipment_id = equipments[selected_index]
        title = self.small_font.render(texts.PROGRESSION_EQUIPMENT_DESCRIPTION, True, (220, 225, 236))
        screen.blit(title, (rect.x, top))
        self._draw_wrapped_text(screen, texts.get_equipment_description(equipment_id), pygame.Rect(rect.x, top + 22, rect.width, 36), (205, 214, 226))

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
