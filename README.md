# TBS Game Skeleton

This repository contains a Python 2D turn-based strategy (TBS) prototype focused on validating core battle systems end-to-end.

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
      menu.py
      battle_log.py

    data/
      config_loader.py
      schema_validator.py

    save/
      save_manager.py
```

## Current Development Status

- Grid / Tile System: `Grid`, `Tile`, and `DualGrid` are implemented; the battlefield is split into left/right zones.
- Unit System: `UnitConfig`, `UnitState`, and `Unit` are implemented with core state operations.
- Movement System (Dijkstra): reachable tiles and preview paths are computed with movement costs and passability.
- Combat System: `damage_calculator.py` handles damage only; `combat_system.py` handles attack range checks.
- Highlight System: `highlight_system.py` computes move/path/attack highlight tiles.
- Turn System: `TurnManager` handles camps, acted flags, and turn switching.
- Enemy AI: `enemy_ai.py` handles enemy decision making (`attack` / `move` / `wait`).
- State Pattern: player input flow is split into `IdleState`, `MoveState`, and `AttackState`.
- Pygame Rendering: map, highlights, and path previews are rendered via `game/render/*`.
- UI System: `ui_system.py` renders UI Panel, HUD, and Action Menu.

## Gameplay (Current Prototype)

- Battlefield is split into two zones (player side and enemy side) with a middle gap area.
- Player clicks own unit to select, then chooses action from Action Menu: `Move`, `Attack`, or `Wait`.
- Move mode shows reachable tiles and hover path preview.
- Attack mode shows enemy-side attackable tiles and applies range rules through `CombatSystem`.
- Enemy acts automatically by AI, then turn switches back to player.
- HUD displays current turn and both camps' HP.

## Next Possible Improvements

- Multiple units per camp and unit selection switching.
- Skill system integration with cooldown/effects and targeting rules.
- Map loading from data files and scenario progression.
- Richer enemy AI strategy and threat evaluation.
- Battle log and combat feedback animation improvements.

## Notes

- Current prototype focuses on architecture validation and modularity.
- Logic and rendering are intentionally split for easier scaling and testing.
