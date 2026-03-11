"""战斗事件系统：集中分发战斗事件到 Buff 监听器。"""

from __future__ import annotations

from game.battle.events.battle_event import BattleEvent
from game.entity.unit import Unit


class EventSystem:
    """Central dispatcher for battle events."""

    def __init__(self, game: object | None = None) -> None:
        self.game = game

    def set_game(self, game: object | None) -> None:
        """Attach game context for unit traversal."""
        self.game = game

    def dispatch(self, event: BattleEvent) -> None:
        """Dispatch one event to all buff listeners on battlefield units."""
        game = self._resolve_game(event)
        if game is None:
            return

        units = getattr(game, "units", [])
        for unit in units:
            if not isinstance(unit, Unit):
                continue
            for buff in list(unit.buffs):
                trigger = getattr(buff, "trigger", None)
                if trigger != event.event_type:
                    continue
                buff.on_trigger(unit, event, game)

    def _resolve_game(self, event: BattleEvent) -> object | None:
        game = event.data.get("game") if isinstance(event.data, dict) else None
        if game is not None:
            return game
        return self.game
