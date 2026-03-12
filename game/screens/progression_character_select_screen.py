"""角色成长角色选择屏幕：先选择一个角色，再进入单角色成长界面。"""

from __future__ import annotations

import math

import pygame

from game.core import texts
from game.player.player_army import PlayerArmy
from game.screens.screen_base import ScreenBase
from game.ui.font_manager import get_font
from game.ui.language_shortcut import handle_language_toggle

CARD_WIDTH = 260
CARD_HEIGHT = 250
CARD_GAP = 20


class ProgressionCharacterSelectScreen(ScreenBase):
    """成长前置角色选择 Screen。"""

    def __init__(self, manager: object, return_screen: ScreenBase | None = None) -> None:
        super().__init__(manager)
        self.return_screen = return_screen
        self.player_army = PlayerArmy()
        self.title_font = get_font(52)
        self.text_font = get_font(28)
        self.small_font = get_font(22)
        self.selected_index = 0
        self.scroll_index = 0

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.running = False
                return
            if event.type == pygame.VIDEORESIZE:
                self.manager.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                continue
            if event.type == getattr(pygame, 'WINDOWSIZECHANGED', -1):
                self.manager.screen = pygame.display.set_mode((event.x, event.y), pygame.RESIZABLE)
                continue
            if handle_language_toggle(event):
                continue
            if event.type == pygame.MOUSEWHEEL:
                self._scroll(-event.y)
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._handle_click(event.pos):
                    return
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_LEFT:
                self._move_selection(-1)
                continue
            if event.key == pygame.K_RIGHT:
                self._move_selection(1)
                continue
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._open_selected_unit()
                return
            if event.key == pygame.K_ESCAPE:
                self._return_to_previous_screen()
                return

    def update(self) -> None:
        return

    def render(self) -> None:
        screen = self.manager.screen
        width = screen.get_width()
        height = screen.get_height()
        screen.fill((22, 28, 36))

        title_surface = self.title_font.render(texts.PROGRESSION_SELECT_TITLE, True, (236, 240, 248))
        screen.blit(title_surface, (36, 24))

        carousel_rect = pygame.Rect(36, 110, width - 72, min(320, height - 220))
        self._draw_carousel(screen, carousel_rect)

        help_surface = self.small_font.render(texts.PROGRESSION_SELECT_HELP, True, (190, 205, 225))
        screen.blit(help_surface, (36, height - 56))
        pygame.display.flip()

    def _draw_carousel(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        pygame.draw.rect(screen, (42, 50, 62), rect, border_radius=10)
        pygame.draw.rect(screen, (96, 112, 140), rect, width=2, border_radius=10)
        units = self.player_army.get_units()
        visible_count = max(1, rect.width // (CARD_WIDTH + CARD_GAP))
        self.scroll_index = max(0, min(self.scroll_index, max(0, len(units) - visible_count)))
        start = self.scroll_index
        end = min(len(units), start + visible_count)
        x = rect.x + 18
        y = rect.y + 28
        for visible_index, unit in enumerate(units[start:end]):
            actual_index = start + visible_index
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            selected = actual_index == self.selected_index
            bg = (72, 92, 120) if selected else (54, 62, 76)
            border = (186, 206, 232) if selected else (124, 144, 170)
            pygame.draw.rect(screen, bg, card_rect, border_radius=10)
            pygame.draw.rect(screen, border, card_rect, width=2, border_radius=10)
            self._draw_unit_card(screen, card_rect, unit)
            x += CARD_WIDTH + CARD_GAP

    def _draw_unit_card(self, screen: pygame.Surface, rect: pygame.Rect, unit: object) -> None:
        name_surface = self.text_font.render(unit.unit_type, True, (244, 246, 252))
        level_surface = self.small_font.render(texts.format_progression_level_exp(unit.level, unit.exp), True, (200, 214, 232))
        profession = getattr(unit, 'profession', texts.PROGRESSION_PROFESSION_UNKNOWN)
        profession_surface = self.small_font.render(f"{texts.PROGRESSION_PROFESSION_LABEL}: {profession}", True, (214, 220, 230))
        screen.blit(name_surface, (rect.x + 14, rect.y + 14))
        screen.blit(level_surface, (rect.x + 14, rect.y + 54))
        screen.blit(profession_surface, (rect.x + 14, rect.y + 84))

        equip_title = self.small_font.render(texts.PROGRESSION_EQUIPMENT_HEADER, True, (228, 232, 240))
        screen.blit(equip_title, (rect.x + 14, rect.y + 126))
        y = rect.y + 156
        for slot in ("weapon", "offhand", "accessory"):
            equipment_id = unit.equipment.get(slot)
            equipment_name = texts.get_equipment_name(equipment_id) if equipment_id else texts.PROGRESSION_EQUIP_STATE_EMPTY
            line = texts.format_equipment_line(texts.get_slot_name(slot), equipment_name)
            surface = self.small_font.render(line, True, (206, 214, 226))
            screen.blit(surface, (rect.x + 20, y))
            y += 24

    def _handle_click(self, pos: tuple[int, int]) -> bool:
        width = self.manager.screen.get_width()
        height = self.manager.screen.get_height()
        rect = pygame.Rect(36, 110, width - 72, min(320, height - 220))
        units = self.player_army.get_units()
        visible_count = max(1, rect.width // (CARD_WIDTH + CARD_GAP))
        start = self.scroll_index
        end = min(len(units), start + visible_count)
        x = rect.x + 18
        y = rect.y + 28
        for visible_index in range(end - start):
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            if card_rect.collidepoint(pos):
                self.selected_index = start + visible_index
                self._open_selected_unit()
                return True
            x += CARD_WIDTH + CARD_GAP
        return False

    def _move_selection(self, delta: int) -> None:
        units = self.player_army.get_units()
        if not units:
            return
        self.selected_index = (self.selected_index + delta) % len(units)
        self._ensure_visible()

    def _scroll(self, delta: int) -> None:
        units = self.player_army.get_units()
        visible_count = max(1, (self.manager.screen.get_width() - 72) // (CARD_WIDTH + CARD_GAP))
        max_scroll = max(0, len(units) - visible_count)
        self.scroll_index = max(0, min(self.scroll_index + delta, max_scroll))
        self.selected_index = max(self.scroll_index, min(self.selected_index, self.scroll_index + visible_count - 1))

    def _ensure_visible(self) -> None:
        visible_count = max(1, (self.manager.screen.get_width() - 72) // (CARD_WIDTH + CARD_GAP))
        if self.selected_index < self.scroll_index:
            self.scroll_index = self.selected_index
        elif self.selected_index >= self.scroll_index + visible_count:
            self.scroll_index = self.selected_index - visible_count + 1

    def _open_selected_unit(self) -> None:
        units = self.player_army.get_units()
        if not units:
            return
        unit = units[self.selected_index]
        from game.screens.progression_screen import ProgressionScreen
        self.manager.switch_to(ProgressionScreen(self.manager, unit.unit_id, return_screen=self))

    def _return_to_previous_screen(self) -> None:
        if self.return_screen is not None:
            self.manager.switch_to(self.return_screen)
            return
        from game.screens.level_select_screen import LevelSelectScreen
        self.manager.switch_to(LevelSelectScreen(self.manager))
