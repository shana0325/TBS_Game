# ARCHITECTURE.md

This file contains the project directory structure and module responsibilities.

---

# Directory Structure

```text
TBS_Game/
  main.py                        # 程序入口（可缩放窗口 + ScreenManager 主循环）
  AGENTS.md                      # AI 代理协作规范
  ARCHITECTURE.md                # 架构与目录说明（本文件）
  README.md                      # 项目说明
  requirements.txt               # Python 依赖

  assets/
    fonts/
      LXGWWenKai-Light.ttf       # 默认中文字体文件
    maps/                        # 地图资源占位
    units/                       # 单位资源占位
    skills/                      # 技能资源占位

  data/
    unit/
      units.json                 # 单位模板配置
    skill/
      skills.json                # 技能模板配置
    buff/
      buffs.json                 # Buff 模板配置
    equipment/
      equipments.json            # 装备模板配置
    player/
      player_roster.json         # 玩家全局编成（成长/技能/装备/额外元数据）

  docs/
    tbs_game_system_design_v2.md # 系统设计文档
    dev_log.md                   # 开发阶段日志

  game/
    ai/
      enemy_ai.py                # 敌方决策（attack/move/wait）

    battle/
      combat/
        combat_system.py         # 攻击距离、攻击结算入口、事件派发协调
        damage_calculator.py     # 伤害计算（支持 Buff 属性修正与技能倍率）
        highlight_system.py      # 移动/路径/攻击高亮 tile 计算
      effects/
        effect_system.py         # 技能效果分发入口
        damage_effect.py         # 伤害效果
        heal_effect.py           # 治疗效果
        buff_effect.py           # Buff 效果
        summon_effect.py         # 召唤效果
        revive_effect.py         # 复活效果
      events/
        battle_event.py          # 统一战斗事件对象
        event_system.py          # 事件广播系统
        event_types.py           # 战斗事件常量
      movement/
        grid.py                  # Grid / DualGrid（双战场结构）
        pathfinder.py            # 可达范围与路径预览（Dijkstra）
        tile.py                  # Tile 数据结构（地块属性）
      turn/
        turn_manager.py          # 回合管理（阵营切换/Buff 生命周期/事件触发）

    controllers/
      enemy_controller.py        # 敌方回合控制（AI 决策 + 行动 + 日志）
      player_controller.py       # 历史玩家控制器（当前主流程主要使用 state/*）

    core/
      game.py                    # 战斗运行时控制器（输入/更新/渲染 + 自适应布局/实时重排）
      game_state.py              # 交互状态枚举（含 SKILL_MODE）
      game_app.py                # 预留：应用容器骨架
      input_handler.py           # 预留：输入分发骨架
      scene_manager.py           # 预留：场景切换骨架
      texts.py                   # 文案统一访问入口（兼容层，代理到当前语言包）
      i18n/
        __init__.py              # 当前语言状态与语言包管理
        zh_cn.py                 # 简体中文文案、说明文本、动态格式化
        en_us.py                 # 英文文案、说明文本、动态格式化

    data/
      config_loader.py           # JSON 配置加载（units/skills/buffs/equipments）
      game_database.py           # 配置统一访问接口（get_unit/get_skill/get_buff/get_equipment）
      schema_validator.py        # 预留：配置校验骨架

    entity/
      buff.py                    # Buff 实体（持续回合/属性修正/控制/护盾/触发）
      equipment.py               # Equipment 实体（slot/modifiers/granted_skills）
      skill.py                   # Skill 实体（effects 列表 + execute）
      unit.py                    # UnitConfig / UnitState / Unit（skills/buffs/状态辅助）

    levels/
      level/
        level_1.py               # 关卡数据（map/terrain/deployment_zones/spawns）
        level_loader.py          # 关卡加载器
      scenario/
        scenario_1.py            # 场景配置（level/enemy_units/victory_condition）
        scenario_loader.py       # 场景加载器
      systems/
        spawn_system.py          # 单位生成系统（按模板创建玩家/敌方/召唤单位，并应用成长与装备）

    player/
      equipment_system.py        # 装备槽位管理、属性汇总、装备技能汇总
      player_army.py             # 玩家全局编成读取、修改、保存
      player_unit_data.py        # 玩家持有角色持久化数据模型
      progression_system.py      # EXP/升级/加点/学技能/装备技能逻辑

    render/
      attack_highlight_renderer.py # 攻击范围高亮渲染
      highlight_renderer.py      # 移动范围高亮渲染
      map_renderer.py            # 地图与单位渲染
      path_renderer.py           # 路径预览渲染

    screens/
      battle_screen.py           # 战斗入口（加载 level/scenario，调用 SpawnSystem，创建 Game）
      deployment_screen.py       # 战前部署（从 PlayerArmy 读取可部署单位，支持实时重排）
      level_select_screen.py     # 关卡/场景选择
      main_menu_screen.py        # 主菜单
      progression_character_select_screen.py # 战前成长角色选择（横向角色卡片列表）
      progression_screen.py      # 单角色成长界面（左侧角色信息 + 右侧属性/技能/装备页签）
      result_screen.py           # 结算界面
      screen_base.py             # Screen 抽象基类（handle_input/update/render）
      screen_manager.py          # Screen 切换与主循环转发

    state/
      attack_state.py            # AttackState：攻击输入与执行（支持取消）
      game_state_base.py         # State Pattern 基类
      idle_state.py              # IdleState：选中与菜单输入
      move_state.py              # MoveState：移动输入与执行（支持取消）
      skill_state.py             # SkillState：技能选择与释放流程（支持取消）

    ui/
      action_menu.py             # 行动菜单（Move/Attack/Skill/Wait）
      battle_log.py              # 战斗日志数据结构
      battle_log_panel.py        # 战斗日志内容渲染（分色/换行/滚动）
      font_manager.py            # 统一字体加载与缓存
      hud.py                     # HUD 兼容接口（当前主要信息由 Unit Info Panel 提供）
      language_shortcut.py       # F2 语言切换快捷键处理
      menu.py                    # 预留：菜单骨架
      progression_tabs.py        # 成长子页签组件
      progression_stat_panel.py  # 属性页面板
      progression_skill_panel.py # 技能页面板
      progression_equipment_panel.py # 装备页面板
      progression_unit_summary_panel.py # 单角色左侧信息面板
      scrollable_list.py         # 通用滚动列表状态与滚动条组件
      skill_menu.py              # 技能菜单
      ui_system.py               # 战斗 UI 面板总渲染（区域2/3/4）
      unit_info_panel.py         # 选中单位信息面板

    save/
      save_manager.py            # 预留：存档骨架
```

# Layer Notes

- `screens/` 负责战斗外流程和界面切换；`core/game.py` 负责战斗运行时。
- 成长流程拆为两段：
  - `progression_character_select_screen.py`：选择要培养的角色
  - `progression_screen.py`：进入单角色成长页
- `levels/` 负责战斗准备数据：
  - `Level`：地图/地形/部署区/出生点
  - `Scenario`：敌方配置与战斗规则
  - `SpawnSystem`：按模板与成长数据、装备数据生成战斗单位
- `player/` 负责玩家长期持有数据与成长系统，不直接参与 pygame 渲染。
- `player/equipment_system.py` 负责装备槽位与数值整合，不把装备逻辑塞进 `Unit` 或 UI。
- `ui/progression_*` 模块负责成长界面具体子页与组件，`ProgressionScreen` 只负责当前角色、当前页签和动作分发。
- `battle/effects/` 负责执行技能效果；`battle/events/` 负责广播战斗事件；`entity/buff.py` 负责响应触发与持续效果。
- `ui/scrollable_list.py` 为通用滚动行为组件，供成长界面和战斗日志等列表型 UI 复用。
- `core/texts.py + core/i18n/*` 负责统一文本来源；`ui/font_manager.py` 负责统一字体来源。

# Runtime Flow

```text
Main Menu
-> Level Select
-> Progression Character Select (optional)
-> Progression (single unit, optional)
-> Deployment
-> Battle
-> Result
```

Battle runtime layering:

```text
Skill
-> EffectSystem
-> Effect modules
-> CombatSystem / TurnManager
-> EventSystem
-> Buff / Trigger logic
```

Text rendering layering:

```text
UI / Screen / Battle Log
-> game.core.texts
-> game.core.i18n.(zh_cn / en_us)
-> pygame font render
```

# Constraints

- 逻辑模块保持 pygame-free；pygame 主要出现在 `screens/`、`render/`、`ui/`、`main.py`。
- `damage_calculator.py` 只负责数值计算；状态修改应由更高层协调。
- 新功能优先扩展现有模块职责边界，不随意合并层级。
- 成长界面避免把“角色选择 + 属性 + 技能 + 装备”同时堆在一个 Screen 中；优先拆为前置选择与子页签结构。
- 界面文本不要在各模块内随意硬编码；优先写入 `game/core/i18n/` 语言包，并通过 `game/core/texts.py` 访问。
- 当前项目保留 `texts / i18n` 接口结构以保证扩展性，但后续开发默认只维护中文文案；除非用户明确要求，否则不需要同步更新英文文案。
