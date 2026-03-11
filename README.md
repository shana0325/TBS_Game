# TBS Game Prototype

This repository contains a Python 2D turn-based strategy (TBS) prototype focused on validating modular battle systems, screen flow, and data-driven combat growth end-to-end.

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

  data/
    unit/
      units.json
    skill/
      skills.json
    buff/
      buffs.json
    player/
      player_roster.json

  docs/
    tbs_game_system_design_v2.md
    dev_log.md

  game/
    ai/
      enemy_ai.py

    battle/
      combat/
        combat_system.py
        damage_calculator.py
        highlight_system.py
      effects/
        effect_system.py
        damage_effect.py
        heal_effect.py
        buff_effect.py
        summon_effect.py
        revive_effect.py
      events/
        battle_event.py
        event_system.py
        event_types.py
      movement/
        grid.py
        pathfinder.py
        tile.py
      turn/
        turn_manager.py

    controllers/
      enemy_controller.py
      player_controller.py

    core/
      game.py
      game_state.py
      game_app.py
      input_handler.py
      scene_manager.py

    data/
      config_loader.py
      game_database.py
      schema_validator.py

    entity/
      buff.py
      skill.py
      unit.py

    levels/
      level/
        level_1.py
        level_loader.py
      scenario/
        scenario_1.py
        scenario_loader.py
      systems/
        spawn_system.py

    player/
      player_army.py
      player_unit_data.py
      progression_system.py

    render/
      attack_highlight_renderer.py
      highlight_renderer.py
      map_renderer.py
      path_renderer.py

    screens/
      battle_screen.py
      deployment_screen.py
      level_select_screen.py
      main_menu_screen.py
      progression_screen.py
      result_screen.py
      screen_base.py
      screen_manager.py

    state/
      attack_state.py
      game_state_base.py
      idle_state.py
      move_state.py
      skill_state.py

    ui/
      action_menu.py
      battle_log.py
      battle_log_panel.py
      hud.py
      menu.py
      scrollable_list.py
      skill_menu.py
      ui_system.py
      unit_info_panel.py

    save/
      save_manager.py
```

## Current Development Status

- Grid / Tile System: 已完成普通地块与双战场 `DualGrid`，支持左右独立战场与中间 gap。
- Unit System: `UnitConfig / UnitState / Unit` 已完成，并支持技能、Buff、护盾、控制状态与持久化角色元数据挂载。
- Movement System (Dijkstra): 已完成移动范围计算与路径预览基础，仍保持纯逻辑实现。
- Combat System: 已完成伤害计算、攻击距离判定、跨战场攻击规则，以及事件驱动的反击/触发能力。
- Turn System: 已完成阵营切换、已行动状态管理、Buff 回合节点处理与事件派发。
- Enemy AI: 已支持基础攻击、移动、等待逻辑，并可在敌方回合逐单位执行。
- CLI integration test: 早期已完成 CLI 验证，用于确认核心逻辑可独立运行。
- Pygame rendering: 已完成地图、单位、移动范围、攻击范围、路径预览渲染。
- HUD UI: 基础 HUD 已保留，当前主战斗信息主要由 `UnitInfoPanel`、`ActionMenu`、`BattleLogPanel` 承担。
- Screen System: 已完成 `MainMenu -> LevelSelect -> Deployment -> Battle -> Result` 流程。
- Deployment System: 已支持部署阶段读取全局玩家编成并放置到部署区。
- Skill / Effect System: 技能已切换为 `EffectSystem` 驱动，支持 `damage / heal / buff / summon / revive`。
- Buff System: 已支持属性增益、DOT/HOT、Stun、Silence、Shield、Counter、Aura 等效果基础。
- Event System: 已完成集中式战斗事件分发，用于命中、击杀、回合开始/结束等触发逻辑。
- Progression System: 已支持 EXP、升级、属性点、技能点、学习技能、装备技能，并写回 `player_roster.json`。
- Scrollable UI: 已新增通用 `ScrollableList` 组件，统一战斗日志与成长界面的滚动行为与滚动条样式。

## Gameplay (Current Prototype)

- 主流程：`Main Menu -> Level Select -> Progression / Deployment -> Battle -> Result`
- 选关界面可进入成长界面，在战斗前查看并调整角色成长。
- 成长界面当前支持：
  - 鼠标点击选择角色
  - 鼠标点击属性 `+` 按钮加点
  - 鼠标选择技能并点击 `Learn / Equip`
  - 滚轮滚动单位列表、属性列表、技能列表
- 部署阶段会从全局 `PlayerArmy` 读取玩家单位，并决定出战位置。
- 战斗阶段支持 `Move / Attack / Skill / Wait`，敌方回合自动执行 AI 行动。
- 右侧 Battle Log 实时显示回合、攻击、击杀、成长等关键事件，并支持滚动查看历史日志。
- 战斗胜利后会给参战玩家单位发放固定 EXP，并自动处理升级与点数增长。

## Next Possible Improvements

- 为 `ProgressionScreen` 增加技能说明、职业限制、前置技能和禁用态提示。
- 将 `SkillMenu`、`ActionMenu` 也统一迁移到 `ScrollableList` 风格。
- 增加成长界面中的技能分类、分页和角色详情面板。
- 增加装备系统、背包系统和更完整的存档读写。
- 扩展战斗技能效果：AOE、位移、召唤控制区、持续光环刷新提示。
- 为 Battle Log 增加筛选、自动跳到最新、分页与高亮关键事件能力。

## Notes

- 当前版本重点仍然是架构验证、模块边界清晰，以及 data-driven 设计可扩展性。
- 游戏逻辑与 pygame 渲染/UI 保持分层，便于后续继续扩展成长、关卡与复杂战斗机制。
