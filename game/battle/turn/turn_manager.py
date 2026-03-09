"""Turn management logic for camp-based battle flow."""

from __future__ import annotations

from game.entity.unit import Unit

PLAYER = "player"
ENEMY = "enemy"


class TurnManager:
    """Manages turn state for player and enemy camps."""

    def __init__(
        self,
        units: list[Unit],
        player_team_id: int = 1,
        enemy_team_id: int = 2,
    ) -> None:
        self.units = units
        self.player_team_id = player_team_id
        self.enemy_team_id = enemy_team_id
        self.current_camp = PLAYER

        self._reset_current_camp_units()

    def next_turn(self) -> None:
        """Switch current camp and reset acted state for that camp."""
        self.current_camp = ENEMY if self.current_camp == PLAYER else PLAYER
        self._reset_current_camp_units()

    def get_active_units(self) -> list[Unit]:
        """Return alive units in current camp that can still act."""
        team_id = self._current_team_id()
        return [
            unit
            for unit in self.units
            if unit.state.alive and unit.state.team_id == team_id and not unit.state.acted
        ]

    def mark_acted(self, unit: Unit) -> None:
        """Mark one unit as acted if it belongs to current camp."""
        if unit.state.team_id != self._current_team_id() or not unit.state.alive:
            return
        unit.state.acted = True

    def is_turn_finished(self) -> bool:
        """Return True when current camp has no active unit left."""
        return len(self.get_active_units()) == 0

    def _current_team_id(self) -> int:
        return self.player_team_id if self.current_camp == PLAYER else self.enemy_team_id

    def _reset_current_camp_units(self) -> None:
        team_id = self._current_team_id()
        for unit in self.units:
            if unit.state.alive and unit.state.team_id == team_id:
                unit.state.acted = False
