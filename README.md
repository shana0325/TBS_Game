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

  tools/
    generate_unit_sprites.py
    generate_unit_sprites.md
    unit_sprite_presets.json

  assets/
    fonts/
      LXGWWenKai-Light.ttf
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
    equipment/
      equipments.json
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
      texts.py
      i18n/
        __init__.py
        zh_cn.py
        en_us.py

    data/
      config_loader.py
      game_database.py
      schema_validator.py

    entity/
      buff.py
      equipment.py
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
      equipment_system.py
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
      progression_character_select_screen.py
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
      font_manager.py
      hud.py
      language_shortcut.py
      menu.py
      scrollable_list.py
      skill_menu.py
      ui_system.py
      unit_info_panel.py
      progression_tabs.py
      progression_stat_panel.py
      progression_skill_panel.py
      progression_equipment_panel.py
      progression_unit_summary_panel.py

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
- Screen System: 已完成 `MainMenu -> LevelSelect -> ProgressionCharacterSelect -> Progression -> Deployment -> Battle -> Result` 流程。
- Deployment System: 已支持部署阶段读取全局玩家编成并放置到部署区。
- Skill / Effect System: 技能已切换为 `EffectSystem` 驱动，支持 `damage / heal / buff / summon / revive`。
- Buff System: 已支持属性增益、DOT/HOT、Stun、Silence、Shield、Counter、Aura 等效果基础。
- Event System: 已完成集中式战斗事件分发，用于命中、击杀、回合开始/结束等触发逻辑。
- Progression System: 已支持 EXP、升级、属性点、技能点、学习技能、装备技能，并写回 `player_roster.json`。
- Equipment System: 已支持 `weapon / offhand / accessory` 三槽位、装备属性修正、装备赋予技能，并在 `SpawnSystem` 中装配到战斗单位。
- Progression UI: 已改为两段式流程，先选择角色，再进入单角色成长界面；成长界面内部拆为 `属性 / 技能 / 装备` 三个子页。
- Scrollable UI: 已新增通用 `ScrollableList` 组件，统一战斗日志与成长界面的滚动行为与滚动条样式。
- Text / Font / i18n System: 已完成统一字体入口、统一文案入口与中英文语言包拆分，支持运行时切换语言。

## Gameplay (Current Prototype)

- 主流程：`Main Menu -> Level Select -> Progression Character Select / Deployment -> Battle -> Result`
- 选关界面可进入角色选择成长界面，再选择一个角色进入单角色成长页面。
- 单角色成长界面当前支持：
  - `属性` 页签：查看角色信息并进行属性加点
  - `技能` 页签：学习技能、装备技能、查看技能与 Buff 说明
  - `装备` 页签：查看装备槽、切换装备、卸下装备、查看装备说明
- 角色选择界面会显示角色名称、等级、职业占位与当前装备，并支持横向切换多个角色。
- 部署阶段会从全局 `PlayerArmy` 读取玩家单位，并决定出战位置。
- 战斗阶段支持 `Move / Attack / Skill / Wait`，敌方回合自动执行 AI 行动。
- 运行中按 `F2` 可切换中文 / 英文；启动时可通过 `TBS_LANG` 设定默认语言。
- 右侧 Battle Log 实时显示回合、攻击、击杀、成长等关键事件，并支持滚动查看历史日志。
- 战斗胜利后会给参战玩家单位发放固定 EXP，并自动处理升级与点数增长。

## Next Possible Improvements

- 为角色选择界面增加职业图标、角色立绘、战斗定位标签与筛选条件。
- 在单角色成长界面显示装备带来的属性汇总变化和技能来源（模板/学习/装备）。
- 为装备系统补充职业限制、装备类型限制和背包库存概念。
- 增加成长界面中的技能分类、分页和前置技能关系。
- 扩展战斗技能效果：AOE、位移、召唤控制区、持续光环刷新提示。
- 为 Battle Log 增加筛选、自动跳到最新、分页与高亮关键事件能力。

## Notes

- 当前版本重点仍然是架构验证、模块边界清晰，以及 data-driven 设计可扩展性。
- 游戏逻辑与 pygame 渲染/UI 保持分层，便于后续继续扩展成长、关卡与复杂战斗机制。
- 文本显示当前统一经由 `game/core/texts.py` 入口分发；字体统一经由 `game/ui/font_manager.py` 管理。
