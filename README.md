# TBS Game Prototype

This repository contains a Python 2D turn-based strategy (TBS) prototype focused on validating core battle systems and screen flow end-to-end.

## Project Structure

```text
TBS_Game/
  main.py
  README.md
  AGENTS.md
  ARCHITECTURE.md
  requirements.txt

  assets/
    maps/
    units/
    skills/

  docs/
    tbs_game_system_design_v2.md
    dev_log.md

  game/
    core/
      game.py
      game_state.py
      game_app.py
      scene_manager.py
      input_handler.py

    screens/
      screen_base.py
      screen_manager.py
      main_menu_screen.py
      level_select_screen.py
      deployment_screen.py
      battle_screen.py
      result_screen.py

    levels/
      level/
        level_1.py
        level_loader.py
      scenario/
        scenario_1.py
        scenario_loader.py
      systems/
        spawn_system.py

    state/
      game_state_base.py
      idle_state.py
      move_state.py
      attack_state.py

    controllers/
      enemy_controller.py
      player_controller.py

    battle/
      battle_system.py
      action_queue.py
      movement/
        tile.py
        grid.py
        pathfinder.py
      combat/
        damage_calculator.py
        combat_system.py
        highlight_system.py
      turn/
        turn_manager.py

    entity/
      unit.py
      skill.py
      buff.py

    ai/
      enemy_ai.py

    render/
      map_renderer.py
      highlight_renderer.py
      path_renderer.py
      attack_highlight_renderer.py
      unit_renderer.py
      effect_renderer.py

    ui/
      ui_system.py
      hud.py
      action_menu.py
      unit_info_panel.py
      menu.py
      battle_log.py

    data/
      config_loader.py
      schema_validator.py

    save/
      save_manager.py
```

## Current Development Status

- Screen System: `ScreenManager` + `MainMenu/LevelSelect/Deployment/Battle/Result` 已接入主循环。
- Level / Scenario / Spawn System: 关卡地图数据、场景配置、实体生成职责已分离。
- Deployment Phase: 战斗前部署阶段已实现，支持部署区高亮、名单选择、放置与开战传参。
- Grid / Tile System: `Grid`、`Tile`、`DualGrid` 已实现，支持双战场与中间 gap。
- Unit System: `UnitConfig`、`UnitState`、`Unit` 已实现，支持基础状态操作。
- Movement System (Dijkstra): 可达范围与路径预览计算可用。
- Combat System: `damage_calculator.py` 负责纯伤害计算，`combat_system.py` 负责攻击距离判断。
- Turn System: `TurnManager` 管理阵营切换、已行动状态与回合结束判断。
- Enemy AI: `enemy_ai.py` 支持攻击/移动/等待决策。
- Pygame Rendering/UI: 地图、单位、高亮、路径预览、底部面板和单位信息显示已接入。

## Gameplay (Current Prototype)

- 主流程：`Main Menu -> Level Select -> Deployment -> Battle -> Result`。
- 部署阶段可在玩家部署区放置 `player_roster` 单位，全部完成后进入战斗。
- 战斗中可点击任意存活单位查看信息；仅玩家未行动单位可执行 `Move/Attack/Wait`。
- 移动模式显示可达格与路径预览；攻击模式显示可攻击范围。
- 敌方在敌方回合自动依次行动，回合自动切换。

## Next Possible Improvements

- 部署阶段增加拖拽放置、撤回与一键自动部署。
- 多场景配置与章节化关卡选择。
- 技能系统、Buff/Debuff 与更完整的战斗日志。
- 更丰富的 AI 策略（仇恨、站位、集火、风险评估）。
- 结果页统计信息（伤害、击杀、回合数）。

## Notes

- Current prototype focuses on architecture validation and modularity.
- Logic and rendering are intentionally split for easier scaling and testing.
