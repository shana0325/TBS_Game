"""实体生成系统：根据关卡与场景数据创建单位并放置到网格。"""

from __future__ import annotations

from game.entity.unit import Unit, UnitConfig, UnitState


class SpawnSystem:
    """根据 Scenario 单位配置与 Level 出生点生成实体。"""

    # 中文注释：单位模板集中在生成系统中，后续可替换为配置表加载。
    UNIT_TEMPLATES: dict[str, dict[str, int]] = {
        "Hero": {"hp": 22, "atk": 7, "defense": 5, "move": 4, "range_min": 1, "range_max": 2},
        "Knight": {"hp": 20, "atk": 6, "defense": 4, "move": 4, "range_min": 1, "range_max": 1},
        "Goblin": {"hp": 14, "atk": 4, "defense": 1, "move": 4, "range_min": 1, "range_max": 1},
        "Orc": {"hp": 18, "atk": 5, "defense": 2, "move": 3, "range_min": 1, "range_max": 1},
    }

    @classmethod
    def spawn_units(
        cls,
        grid: object,
        level_data: dict[str, object],
        scenario_data: dict[str, object],
        player_team_id: int = 1,
        enemy_team_id: int = 2,
    ) -> tuple[list[Unit], list[Unit]]:
        """读取关卡与场景并返回双方单位列表。"""
        spawns = level_data.get("spawns", {})
        player_spawns = list(spawns.get("player", []))
        enemy_spawns = list(spawns.get("enemy", []))

        player_units = cls._spawn_camp_units(
            grid=grid,
            unit_specs=list(scenario_data.get("player_units", [])),
            spawn_points=player_spawns,
            team_id=player_team_id,
        )
        enemy_units = cls._spawn_camp_units(
            grid=grid,
            unit_specs=list(scenario_data.get("enemy_units", [])),
            spawn_points=enemy_spawns,
            team_id=enemy_team_id,
        )
        return player_units, enemy_units

    @classmethod
    def _spawn_camp_units(
        cls,
        grid: object,
        unit_specs: list[dict[str, object]],
        spawn_points: list[tuple[int, int]],
        team_id: int,
    ) -> list[Unit]:
        units: list[Unit] = []

        for spec in unit_specs:
            unit_type = str(spec.get("type", ""))
            spawn_index = int(spec.get("spawn", -1))

            if spawn_index < 0 or spawn_index >= len(spawn_points):
                raise ValueError(f"Invalid spawn index {spawn_index} for unit type {unit_type}")

            spawn_pos = spawn_points[spawn_index]
            tile = grid.get_tile(spawn_pos[0], spawn_pos[1])
            if tile is None:
                raise ValueError(f"Invalid spawn position {spawn_pos} for unit type {unit_type}")

            template = cls.UNIT_TEMPLATES.get(unit_type)
            if template is None:
                raise ValueError(f"Unknown unit type: {unit_type}")

            config = UnitConfig(
                hp=template["hp"],
                atk=template["atk"],
                defense=template["defense"],
                move=template["move"],
                range_min=template["range_min"],
                range_max=template["range_max"],
            )
            state = UnitState(
                pos=spawn_pos,
                hp=config.hp,
                acted=False,
                alive=True,
                team_id=team_id,
            )
            unit = Unit(config=config, state=state)
            setattr(unit, "name", unit_type)
            units.append(unit)

        return units
