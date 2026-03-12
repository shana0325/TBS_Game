"""角色信息面板：在单角色成长界面中显示当前角色信息。"""

from __future__ import annotations

import pygame

from game.core import texts


class ProgressionUnitSummaryPanel:
    """单角色信息面板。"""

    def __init__(self, title_font: pygame.font.Font, text_font: pygame.font.Font, small_font: pygame.font.Font) -> None:
        self.title_font = title_font
        self.text_font = text_font
        self.small_font = small_font

    def render(self, screen: pygame.Surface, rect: pygame.Rect, unit: object) -> None:
        title_surface = self.title_font.render(texts.PROGRESSION_SUMMARY_TITLE, True, (220, 225, 236))
        screen.blit(title_surface, (rect.x, rect.y))

        y = rect.y + 40
        lines = [
            f"{texts.PROGRESSION_NAME}: {unit.unit_type}",
            f"{texts.PROGRESSION_LEVEL}: {unit.level}",
            f"{texts.PROGRESSION_EXP}: {unit.exp}",
            f"{texts.PROGRESSION_STAT_POINTS}: {unit.stat_points}",
            f"{texts.PROGRESSION_SKILL_POINTS}: {unit.skill_points}",
            f"{texts.PROGRESSION_PROFESSION_LABEL}: {getattr(unit, 'profession', texts.PROGRESSION_PROFESSION_UNKNOWN)}",
            "",
            texts.PROGRESSION_EQUIPMENT_HEADER,
        ]
        for line in lines:
            if not line:
                y += 10
                continue
            surface = self.text_font.render(line, True, (230, 236, 245))
            screen.blit(surface, (rect.x, y))
            y += 34

        for slot in ("weapon", "offhand", "accessory"):
            equipment_id = unit.equipment.get(slot)
            equipment_name = texts.get_equipment_name(equipment_id) if equipment_id else texts.PROGRESSION_EQUIP_STATE_EMPTY
            equip_line = texts.format_equipment_line(texts.get_slot_name(slot), equipment_name)
            surface = self.small_font.render(equip_line, True, (206, 214, 226))
            screen.blit(surface, (rect.x + 8, y))
            y += 28
