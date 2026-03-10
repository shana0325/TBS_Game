# ARCHITECTURE.md

This file contains the project directory structure and module responsibilities.

---

# Directory Structure

```text
TBS_Game/
  main.py                        # 程序入口（初始化 pygame + 驱动 ScreenManager 循环）
  AGENTS.md                      # AI 代理协作规范
  ARCHITECTURE.md                # 架构与目录说明（本文件）
  README.md                      # 项目说明
  requirements.txt               # Python 依赖

  assets/
    maps/                        # 地图资源占位
    units/                       # 单位资源占位
    skills/                      # 技能资源占位

  docs/
    tbs_game_system_design_v2.md # 系统设计文档
    dev_log.md                   # 开发阶段日志

  game/
    core/
      game.py                    # 战斗运行时控制器（输入/更新/渲染）
      game_state.py              # 保留状态枚举（IDLE/UNIT_SELECTED/MOVE/ATTACK/ENEMY_TURN）
      game_app.py                # 预留：应用容器骨架
      scene_manager.py           # 预留：场景切换骨架
      input_handler.py           # 预留：输入分发骨架

    screens/
      screen_base.py             # Screen 抽象基类（handle_input/update/render）
      screen_manager.py          # Screen 切换与主循环转发
      main_menu_screen.py        # 主菜单
      level_select_screen.py     # 关卡/场景选择
      deployment_screen.py       # 战前部署（部署区高亮/放置/开战）
      battle_screen.py           # 战斗入口（加载 level/scenario，调用 SpawnSystem，创建 Game）
      result_screen.py           # 结算界面

    levels/
      level/
        level_1.py               # 关卡数据（map/terrain/deployment_zones/spawns）
        level_loader.py          # 关卡加载器
      scenario/
        scenario_1.py            # 场景配置（level/player_roster/enemy_units/victory_condition）
        scenario_loader.py       # 场景加载器
      systems/
        spawn_system.py          # 单位生成系统（player/enemy 分离生成）

    state/
      game_state_base.py         # State Pattern 基类
      idle_state.py              # IdleState：选中与菜单输入
      move_state.py              # MoveState：移动输入与执行
      attack_state.py            # AttackState：攻击输入与执行

    controllers/
      enemy_controller.py        # 敌方回合控制（AI 决策 + 行动）
      player_controller.py       # 历史控制器（当前主流程主要使用 state/*）

    battle/
      battle_system.py           # 预留：战斗系统总入口骨架
      action_queue.py            # 预留：行动队列骨架

      movement/
        tile.py                  # Tile 数据结构（地块属性）
        grid.py                  # Grid / DualGrid（双战场结构）
        pathfinder.py            # 可达范围与路径预览（Dijkstra）

      combat/
        damage_calculator.py     # 伤害计算（纯计算，不改状态）
        combat_system.py         # 攻击距离/范围判定
        highlight_system.py      # 移动/路径/攻击高亮 tile 计算

      turn/
        turn_manager.py          # 回合管理（阵营切换/已行动标记）

    entity/
      unit.py                    # UnitConfig / UnitState / Unit
      skill.py                   # 预留：技能实体骨架
      buff.py                    # 预留：Buff 实体骨架

    ai/
      enemy_ai.py                # 敌方决策（attack/move/wait）

    render/
      map_renderer.py            # 地图与单位渲染
      highlight_renderer.py      # 移动范围高亮渲染
      path_renderer.py           # 路径预览渲染
      attack_highlight_renderer.py # 攻击范围高亮渲染
      unit_renderer.py           # 预留：单位渲染骨架
      effect_renderer.py         # 预留：特效渲染骨架

    ui/
      ui_system.py               # UI 面板总渲染（Panel + UnitInfo + ActionMenu）
      hud.py                     # HUD 兼容接口（当前主要信息由 Unit Info Panel 提供）
      action_menu.py             # 行动菜单（Move/Attack/Wait）
      unit_info_panel.py         # 选中单位信息面板
      menu.py                    # 预留：菜单骨架
      battle_log.py              # 预留：战斗日志骨架

    data/
      config_loader.py           # 预留：配置加载骨架
      schema_validator.py        # 预留：配置校验骨架

    save/
      save_manager.py            # 预留：存档骨架
```

Notes:
- 非战斗界面流程由 `game/screens/*` 管理；战斗运行时由 `game/core/game.py` 负责。
- 战斗准备阶段职责分离：`Level`（地图数据）/`Scenario`（编成与规则）/`SpawnSystem`（实体生成）。
- 部署阶段在 `deployment_screen.py`：只处理部署交互与结果传递，不改 battle 核心系统。
- Combat 职责拆分：`damage_calculator.py`（伤害计算），`combat_system.py`（距离判定），`highlight_system.py`（高亮计算）。
- 约束：逻辑模块保持 pygame-free；pygame 主要出现在 `screens`、`render`、`ui`、`main.py`。
