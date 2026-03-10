# TBS Game Prototype

This repository contains a Python 2D turn-based strategy (TBS) prototype focused on validating modular battle systems and screen flow end-to-end.

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
      skill_state.py

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
      skill_menu.py
      unit_info_panel.py
      battle_log.py
      battle_log_panel.py
      menu.py

    data/
      config_loader.py
      schema_validator.py

    save/
      save_manager.py
```

## Current Development Status

- Screen System: `ScreenManager` + `MainMenu / LevelSelect / Deployment / Battle / Result` 已接入。
- Level/Scenario/Spawn: `Level`（地图数据）/`Scenario`（战斗配置）/`SpawnSystem`（实体生成）职责分离。
- Deployment Phase: 战前部署可选择 roster 单位并放置到部署区，再进入战斗。
- Dual Battlefield: 双战场 + 中间 gap 规则已实现，跨战场攻击可判定。
- Unit/Turn/AI: 多单位回合、已行动状态、敌方逐单位行动已实现。
- Movement/Combat: Dijkstra 可达范围、路径预览、基础伤害与射程判定已实现。
- Skill System (MVP):
  - 新增 `Skill` 实体与 `SkillMenu`、`SkillState`
  - 支持示例技能 `Power Strike`（150% 伤害）
  - `Knight` 默认携带该技能
- Battle Log System:
  - 记录开战、回合切换、攻击、击杀、等待、结算
  - 玩家/敌方攻击日志分色显示
  - 长日志自动换行
  - 移动日志保留数据但默认不在战斗 UI 显示
- Responsive UI Layout:
  - 布局保持 `11114 / 11114 / 22334`
  - 1: 战场，2: 单位信息，3: 行动/技能，4: 战斗日志
  - 基于 `screen.get_width()/get_height()` 比例计算
  - 支持运行中拖拽窗口实时重排（battle/deployment/menu/result）

## Gameplay (Current Prototype)

- 主流程：`Main Menu -> Level Select -> Deployment -> Battle -> Result`。
- 部署阶段：选择单位并放置到玩家部署区，完成后开始战斗。
- 战斗阶段：
  - 选择单位后可执行 `Move / Attack / Skill / Wait`
  - `Skill` 可选择技能后点目标释放
  - 右键可取消 `Move/Attack/Skill` 状态，避免无目标时卡住
- 敌方回合自动行动，回合自动切换。
- 右侧日志栏实时显示关键战斗事件。

## Next Possible Improvements

- 技能系统扩展：冷却、消耗、AOE、治疗、Buff/Debuff。
- 技能选择体验优化：范围高亮、无效目标提示、键盘快捷键。
- 战斗日志增强：分页/滚动、筛选、历史回放。
- 地图与场景扩展：多关卡、多胜利条件、脚本事件。
- 更高级 AI：仇恨、站位、集火和风险评估。

## Notes

- 当前版本重点是架构验证和模块边界清晰。
- 游戏逻辑与渲染/UI 仍保持分层，便于后续扩展。
