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
        # 中文注释：兼容旧数据（player_units+spawns）与新流程（player_roster+deployment_zones）。
        player_specs = list(scenario_data.get("player_units", scenario_data.get("player_roster", [])))
        player_spawns = list(level_data.get("spawns", {}).get("player", []))

        if player_spawns and all("spawn" in spec for spec in player_specs):
            player_units = cls._spawn_camp_units(
                grid=grid,
                unit_specs=player_specs,
                spawn_points=player_spawns,
                team_id=player_team_id,
            )
        else:
            deployment_zone = list(level_data.get("deployment_zones", {}).get("player", []))
            deployment_positions = deployment_zone[: len(player_specs)]
            player_units = cls.spawn_player_units(
                grid=grid,
                roster=player_specs,
                deployment_positions=deployment_positions,
                player_team_id=player_team_id,
            )

        enemy_units = cls.spawn_enemy_units(
            grid=grid,
            level_data=level_data,
            scenario_data=scenario_data,
            enemy_team_id=enemy_team_id,
        )
        return player_units, enemy_units

    @classmethod
    def spawn_player_units(
        cls,
        grid: object,
        roster: list[dict[str, object]],
        deployment_positions: list[tuple[int, int]],
        player_team_id: int = 1,
    ) -> list[Unit]:
        """根据部署结果生成玩家单位。"""
        if len(roster) != len(deployment_positions):
            raise ValueError("Deployment positions count must match roster size")

        units: list[Unit] = []
        for index, roster_entry in enumerate(roster):
            unit_type = str(roster_entry.get("type", ""))
            pos = deployment_positions[index]
            units.append(cls._create_unit_from_template(grid, unit_type, pos, player_team_id))
        return units

    @classmethod
    def spawn_enemy_units(
        cls,
        grid: object,
        level_data: dict[str, object],
        scenario_data: dict[str, object],
        enemy_team_id: int = 2,
    ) -> list[Unit]:
        """仅生成敌方单位，供部署后进入战斗时使用。"""
        enemy_spawns = list(level_data.get("spawns", {}).get("enemy", []))
        return cls._spawn_camp_units(
            grid=grid,
            unit_specs=list(scenario_data.get("enemy_units", [])),
            spawn_points=enemy_spawns,
            team_id=enemy_team_id,
        )

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
            units.append(cls._create_unit_from_template(grid, unit_type, spawn_pos, team_id))

        return units

    @classmethod
    def _create_unit_from_template(
        cls,
        grid: object,
        unit_type: str,
        pos: tuple[int, int],
        team_id: int,
    ) -> Unit:
        tile = grid.get_tile(pos[0], pos[1])
        if tile is None:
            raise ValueError(f"Invalid spawn position {pos} for unit type {unit_type}")

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
            pos=pos,
            hp=config.hp,
            acted=False,
            alive=True,
            team_id=team_id,
        )
        unit = Unit(config=config, state=state)
        setattr(unit, "name", unit_type)
        return unit
