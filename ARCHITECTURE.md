# ARCHITECTURE.md

This file contains the project directory structure and module responsibilities.

---

# Directory Structure

```text
TBS_Game/
  main.py                        # 程序入口（初始化 pygame + 驱动 Game 循环）
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
      game.py                    # 游戏主控制器（主流程调度）
      game_state.py              # 保留的状态枚举（IDLE/MOVE/ATTACK 等）
      game_app.py                # 预留：应用容器骨架
      scene_manager.py           # 预留：场景切换骨架
      input_handler.py           # 预留：输入分发骨架

    state/
      game_state_base.py         # State Pattern 基类
      idle_state.py              # IdleState：选中与菜单输入
      move_state.py              # MoveState：移动输入与执行
      attack_state.py            # AttackState：攻击输入与执行

    controllers/
      enemy_controller.py        # 敌方回合控制（AI 决策 + 行动）
      player_controller.py       # 预留：历史控制器实现（当前主流程使用 state/*）

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
      ui_system.py               # UI 面板总渲染（Panel + HUD + ActionMenu）
      hud.py                     # HUD（回合与 HP）
      action_menu.py             # 行动菜单（Move/Attack/Wait）
      menu.py                    # 预留：菜单骨架
      battle_log.py              # 预留：战斗日志骨架

    data/
      config_loader.py           # 预留：配置加载骨架
      schema_validator.py        # 预留：配置校验骨架

    save/
      save_manager.py            # 预留：存档骨架
```

Notes:
- Runtime orchestration is centered in `game/core/game.py`.
- Player turn input is currently driven by State Pattern (`game/state/*`).
- Combat responsibilities are split: `damage_calculator.py` (damage only), `combat_system.py` (range checks), `highlight_system.py` (highlight tile computation).
- UI responsibilities are split: gameplay renderers in `game/render/*`, panel/HUD/menu composition in `game/ui/ui_system.py`.
- Logic modules should stay pygame-free where possible; rendering/UI/main are the primary pygame users.
