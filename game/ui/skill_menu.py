"""技能菜单模块：显示当前单位可用技能列表。"""

from __future__ import annotations

import pygame

from game.entity.skill import Skill

MENU_BG_COLOR = (248, 248, 252)
MENU_BORDER_COLOR = (84, 84, 96)
MENU_TEXT_COLOR = (24, 24, 34)
MENU_HOVER_COLOR = (232, 240, 255)
MENU_TITLE_COLOR = (44, 44, 58)


class SkillMenu:
    """Simple skill menu for current selected unit."""

    def __init__(self, x: int, y: int, width: int = 220, item_height: int = 40) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.item_height = item_height
        self.skills: list[Skill] = []
        self.visible = False
        self._font: pygame.font.Font | None = None
        self._title_font: pygame.font.Font | None = None

    def set_skills(self, skills: list[Skill]) -> None:
        # 中文注释：每帧由 Game 更新当前单位技能列表。
        self.skills = list(skills)

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return

        if self._font is None:
            self._font = pygame.font.Font(None, 26)
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, 30)

        title_surface = self._title_font.render("Skills", True, MENU_TITLE_COLOR)
        screen.blit(title_surface, (self.x, self.y - 34))

        mouse_pos = pygame.mouse.get_pos()
        for index, skill in enumerate(self.skills):
            rect = self._item_rect(index)
            bg_color = MENU_HOVER_COLOR if rect.collidepoint(mouse_pos) else MENU_BG_COLOR
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, MENU_BORDER_COLOR, rect, width=1)

            label = f"{skill.name} x{skill.power:.1f}"
            text_surface = self._font.render(label, True, MENU_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def get_skill_at_pos(self, pos: tuple[int, int]) -> Skill | None:
        if not self.visible:
            return None

        for index, skill in enumerate(self.skills):
            if self._item_rect(index).collidepoint(pos):
                return skill
        return None

    def _item_rect(self, index: int) -> pygame.Rect:
        return pygame.Rect(
            self.x,
            self.y + index * self.item_height,
            self.width,
            self.item_height,
        )
