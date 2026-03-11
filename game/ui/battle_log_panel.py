"""战斗日志面板模块：负责在 UI 区域显示日志文本。"""

from __future__ import annotations

import pygame

from game.ui.battle_log import BattleLog
from game.ui.font_manager import get_font
from game.ui.scrollable_list import ScrollableList


class BattleLogPanel:
    """将 BattleLog 中的最近消息渲染到指定区域。"""

    def __init__(
        self,
        screen: pygame.Surface,
        battle_log: BattleLog,
        font_size: int = 22,
        text_color: tuple[int, int, int] = (42, 52, 66),
        player_attack_color: tuple[int, int, int] = (35, 90, 220),
        enemy_attack_color: tuple[int, int, int] = (200, 55, 55),
        line_height: int = 24,
    ) -> None:
        self.screen = screen
        self.battle_log = battle_log
        self.font = get_font(font_size)
        self.text_color = text_color
        self.player_attack_color = player_attack_color
        self.enemy_attack_color = enemy_attack_color
        self.line_height = line_height
        # 中文注释：战斗日志以底部为锚点，滚轮向上查看更旧日志。
        self.scroller = ScrollableList(
            item_height=self.line_height,
            wheel_step=3,
            anchor="bottom",
            track_color=(208, 214, 224),
            thumb_color=(124, 138, 162),
            scrollbar_width=6,
            scrollbar_gap=4,
        )
        self._last_rect = pygame.Rect(0, 0, 0, 0)

    def handle_event(self, event: pygame.event.Event) -> None:
        """处理日志面板滚轮输入。"""
        if self._last_rect.width <= 0 or self._last_rect.height <= 0:
            return
        wrapped_rows = self._build_wrapped_rows(max(20, self._last_rect.width - 24))
        self.scroller.handle_event(event, self._last_rect, len(wrapped_rows))

    def render(self, rect: pygame.Rect) -> None:
        """在给定区域内渲染最近日志。"""
        self._last_rect = rect.copy()
        wrapped_rows = self._build_wrapped_rows(max(20, rect.width - 24))
        start_index, end_index = self.scroller.get_visible_slice(len(wrapped_rows), rect)
        rows_to_draw = wrapped_rows[start_index:end_index]

        y = rect.y + 4
        for line, color in rows_to_draw:
            surface = self.font.render(line, True, color)
            self.screen.blit(surface, (rect.x + 6, y))
            y += self.line_height

        self.scroller.draw_scrollbar(self.screen, rect, len(wrapped_rows))

    def _build_wrapped_rows(self, max_text_width: int) -> list[tuple[str, tuple[int, int, int]]]:
        # 中文注释：移动日志保留在数据层，但不显示在战斗 UI。
        raw_entries = self.battle_log.get_recent_entries(200)
        visible_entries = [entry for entry in raw_entries if entry.get("category") != "move"]

        wrapped_rows: list[tuple[str, tuple[int, int, int]]] = []
        for entry in visible_entries:
            text = entry.get("text", "")
            color = self._resolve_color(entry)
            for line in self._wrap_text(text, max_text_width):
                wrapped_rows.append((line, color))
        return wrapped_rows

    def _resolve_color(self, entry: dict[str, str]) -> tuple[int, int, int]:
        # 中文注释：我方/敌方攻击日志分别使用不同颜色显示。
        if entry.get("category") == "attack":
            if entry.get("side") == "player":
                return self.player_attack_color
            if entry.get("side") == "enemy":
                return self.enemy_attack_color
        return self.text_color

    def _wrap_text(self, text: str, max_width: int) -> list[str]:
        # 中文注释：按像素宽度进行简单换行，避免长日志超出面板。
        if not text:
            return [""]

        lines: list[str] = []
        current = ""

        for ch in text:
            candidate = current + ch
            if self.font.size(candidate)[0] <= max_width:
                current = candidate
                continue

            if current:
                lines.append(current)
                current = ch
            else:
                lines.append(ch)
                current = ""

        if current:
            lines.append(current)

        return lines
