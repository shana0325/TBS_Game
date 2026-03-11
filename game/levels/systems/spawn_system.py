"""实体生成系统：根据关卡与场景数据创建单位并放置到网格。"""

from __future__ import annotations

from game.data.config_loader import ConfigLoader
from game.data.game_database import GameDatabase
from game.entity.skill import Skill
from game.entity.unit import Unit, UnitConfig, UnitState


class SpawnSystem:
    """根据 Scenario 单位配置与 Level 出生点生成实体。"""

    # 中文注释：先加载配置，再由 GameDatabase 提供统一访问接口。
    _config_loader = ConfigLoader()
    _game_db = GameDatabase(_config_loader)

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
            units.append(
                cls._create_unit_from_template(
                    grid=grid,
                    unit_type=unit_type,
                    pos=pos,
                    team_id=player_team_id,
                    unit_overrides=roster_entry,
                )
            )
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
    def spawn_unit_at(
        cls,
        grid: object,
        unit_type: str,
        pos: tuple[int, int],
        team_id: int,
        unit_overrides: dict[str, object] | None = None,
    ) -> Unit:
        """在指定位置生成单个单位，供召唤等系统调用。"""
        return cls._create_unit_from_template(
            grid=grid,
            unit_type=unit_type,
            pos=pos,
            team_id=team_id,
            unit_overrides=unit_overrides,
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
            units.append(
                cls._create_unit_from_template(
                    grid=grid,
                    unit_type=unit_type,
                    pos=spawn_pos,
                    team_id=team_id,
                    unit_overrides=spec,
                )
            )

        return units

    @classmethod
    def _create_unit_from_template(
        cls,
        grid: object,
        unit_type: str,
        pos: tuple[int, int],
        team_id: int,
        unit_overrides: dict[str, object] | None = None,
    ) -> Unit:
        tile = grid.get_tile(pos[0], pos[1])
        if tile is None:
            raise ValueError(f"Invalid spawn position {pos} for unit type {unit_type}")

        template = cls._game_db.get_unit(unit_type)
        if template is None:
            raise ValueError(f"Unknown unit type: {unit_type}")

        overrides = unit_overrides if isinstance(unit_overrides, dict) else {}
        allocated_stats = cls._normalize_stat_map(overrides.get("allocated_stats", {}))

        config = UnitConfig(
            hp=int(template["hp"]) + allocated_stats.get("hp", 0),
            atk=int(template["atk"]) + allocated_stats.get("attack", 0) + allocated_stats.get("atk", 0),
            defense=int(template["defense"]) + allocated_stats.get("defense", 0),
            move=int(template["move"]) + allocated_stats.get("move", 0),
            range_min=int(template["range_min"]),
            range_max=int(template["range_max"]),
        )
        state = UnitState(
            pos=pos,
            hp=config.hp,
            acted=False,
            alive=True,
            team_id=team_id,
        )
        skills = cls._build_skills_for_unit(template, overrides)
        unit = Unit(config=config, state=state, skills=skills)
        setattr(unit, "name", unit_type)
        if "id" in overrides:
            setattr(unit, "player_unit_id", str(overrides.get("id", "")))
        if "level" in overrides:
            setattr(unit, "level", int(overrides.get("level", 1)))
        return unit

    @classmethod
    def _build_skills_for_unit(
        cls,
        unit_template: dict[str, object],
        unit_overrides: dict[str, object] | None = None,
    ) -> list[Skill]:
        # 中文注释：单位技能来源 = 模板技能 + learned/equipped/extra，按顺序合并并去重。
        result: list[Skill] = []

        overrides = unit_overrides if isinstance(unit_overrides, dict) else {}
        template_skill_ids = cls._normalize_skill_ids(unit_template.get("skills", []))
        learned_skill_ids = cls._normalize_skill_ids(overrides.get("learned_skills", []))
        equipped_skill_ids = cls._normalize_skill_ids(overrides.get("equipped_skills", []))
        extra_skill_ids = cls._normalize_skill_ids(overrides.get("extra_skills", []))

        merged_skill_ids: list[str] = []
        for skill_id in template_skill_ids + learned_skill_ids + equipped_skill_ids + extra_skill_ids:
            if skill_id not in merged_skill_ids:
                merged_skill_ids.append(skill_id)

        for skill_name in merged_skill_ids:
            skill_data = cls._game_db.get_skill(skill_name)
            if skill_data is None:
                raise ValueError(f"Unknown skill id in unit config: {skill_name}")

            raw_effects = skill_data.get("effects", [])
            effects: list[dict[str, object]] = []
            if isinstance(raw_effects, list):
                for raw_effect in raw_effects:
                    if isinstance(raw_effect, dict):
                        effects.append(dict(raw_effect))

            # 中文注释：兼容旧格式（仅 power），自动映射为 damage 效果。
            power_value = float(skill_data.get("power", 1.0))
            if not effects:
                effects = [{"type": "damage", "power": power_value}]

            result.append(
                Skill(
                    name=str(skill_data.get("name", skill_name)),
                    power=power_value,
                    min_range=int(skill_data.get("min_range", 1)),
                    max_range=int(skill_data.get("max_range", 1)),
                    effects=effects,
                )
            )

        return result

    @staticmethod
    def _normalize_skill_ids(raw_skill_ids: object) -> list[str]:
        # 中文注释：将配置中的技能列表标准化为字符串数组。
        if not isinstance(raw_skill_ids, list):
            return []

        result: list[str] = []
        for skill_id in raw_skill_ids:
            skill_name = str(skill_id).strip()
            if skill_name:
                result.append(skill_name)
        return result

    @staticmethod
    def _normalize_stat_map(raw_stats: object) -> dict[str, int]:
        # 中文注释：将角色成长中的属性加点标准化为数值映射。
        if not isinstance(raw_stats, dict):
            return {}

        result: dict[str, int] = {}
        for key, value in raw_stats.items():
            stat_name = str(key).strip().lower()
            if not stat_name:
                continue
            result[stat_name] = int(value)
        return result
