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
        self.game_context: object | None = None

        self._reset_current_camp_units()
        self._process_turn_start(team_id=self._current_team_id())

    def set_game_context(self, game: object | None) -> None:
        """Attach game context so buffs can access battle_log during ticks."""
        self.game_context = game

    def next_turn(self) -> None:
        """Switch current camp and reset acted state for that camp."""
        # 中文注释：先处理当前阵营回合结束（含 Buff 结算），再切到下一阵营。
        self._process_turn_end(team_id=self._current_team_id())

        self.current_camp = ENEMY if self.current_camp == PLAYER else PLAYER
        self._reset_current_camp_units()
        self._refresh_aura_buffs()
        self._process_turn_start(team_id=self._current_team_id())

    def get_active_units(self) -> list[Unit]:
        """Return alive units in current camp that can still act."""
        team_id = self._current_team_id()
        return [
            unit
            for unit in self.units
            if unit.state.alive
            and unit.state.team_id == team_id
            and not unit.state.acted
            and not unit.is_stunned()
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

    def _process_turn_start(self, team_id: int) -> None:
        # 中文注释：调用 Buff 的回合开始钩子，并分发 on_turn_start 事件。
        for unit in self.units:
            if not unit.state.alive or unit.state.team_id != team_id:
                continue
            for buff in list(unit.buffs):
                buff.on_turn_start(unit, self.game_context)

            self._dispatch_turn_event("on_turn_start", unit)

    def _process_turn_end(self, team_id: int) -> None:
        # 中文注释：调用 Buff 的回合结束钩子并清理到期 Buff/召唤单位。
        for unit in self.units:
            if not unit.state.alive or unit.state.team_id != team_id:
                continue

            for buff in list(unit.buffs):
                buff.on_turn_end(unit, self.game_context)

            self._dispatch_turn_event("on_turn_end", unit)

            unit.buffs = [buff for buff in unit.buffs if buff.duration != 0]

            if unit.summon_duration is not None:
                unit.summon_duration -= 1
                if unit.summon_duration <= 0:
                    unit.state.hp = 0
                    unit.state.alive = False
                    self._log_summon_expire(unit)

    def _refresh_aura_buffs(self) -> None:
        # 中文注释：每回合开始前重建 Aura 实例，实现离开范围自动移除。
        for unit in self.units:
            unit.buffs = [buff for buff in unit.buffs if not buff.is_aura_instance]

        for source in self.units:
            if not source.state.alive:
                continue

            source_buffs = [buff for buff in source.buffs if buff.aura_range > 0 and buff.duration != 0]
            if not source_buffs:
                continue

            for aura_buff in source_buffs:
                for target in self.units:
                    if not target.state.alive:
                        continue
                    if target.state.team_id != source.state.team_id:
                        continue
                    if self._distance(source, target) > aura_buff.aura_range:
                        continue
                    target.add_buff(aura_buff.create_aura_instance())

    def _distance(self, src: Unit, dst: Unit) -> int:
        # 中文注释：Aura 距离按逻辑坐标曼哈顿距离计算。
        sx, sy = src.state.pos
        dx, dy = dst.state.pos
        return abs(self._to_logical_x(sx) - self._to_logical_x(dx)) + abs(sy - dy)

    def _to_logical_x(self, x: int) -> int:
        game = self.game_context
        grid = getattr(game, "grid", None)
        if grid is None:
            return x

        enemy_offset = getattr(grid, "enemy_offset_x", None)
        gap_width = getattr(grid, "gap_width", None)
        if enemy_offset is None or gap_width is None:
            return x

        if x >= int(enemy_offset):
            return x - int(gap_width)
        return x

    def _dispatch_turn_event(self, event_type: str, unit: Unit) -> None:
        game = self.game_context
        if game is None:
            return

        combat_system = getattr(game, "combat_system", None)
        if combat_system is None:
            return

        combat_system.dispatch_event(
            event_type,
            {
                "attacker": unit,
                "target": unit,
                "damage": 0,
                "game": game,
            },
        )

    def _log_summon_expire(self, unit: Unit) -> None:
        game = self.game_context
        if game is None:
            return

        battle_log = getattr(game, "battle_log", None)
        if battle_log is None:
            return

        side = "player" if unit.state.team_id == 1 else "enemy"
        unit_name = getattr(unit, "name", "Unit")
        battle_log.add(f"{unit_name} disappears as summon duration ends", category="summon", side=side)
