# TBS Game Skeleton

This repository contains a Python 2D turn-based strategy (TBS) prototype focused on validating core battle systems end-to-end.

## Project Structure

```text
TBS_Game/
  main.py
  README.md
  docs/
    tbs_game_system_design_v2.md
  assets/
    maps/
    units/
    skills/
  game/
    core/
      game_app.py
      scene_manager.py
      input_handler.py
    battle/
      battle_system.py
      action_queue.py
      combat/
        damage_calculator.py
      turn/
        turn_manager.py
      movement/
        pathfinder.py
    entity/
      unit.py
      skill.py
      buff.py
    ai/
      enemy_ai.py
    data/
      config_loader.py
      schema_validator.py
    ui/
      hud.py
      menu.py
      battle_log.py
    render/
      map_renderer.py
      unit_renderer.py
      effect_renderer.py
    save/
      save_manager.py
```

## Current Development Status

- Grid / Tile System: `Tile` defines map tile data (`move_cost`, `defense_bonus`, `passable`), and `Grid` stores 2D tiles with tile/neighbor queries.
- Unit System: `UnitConfig`, `UnitState`, and `Unit` are implemented with core state operations (`move_to`, `take_damage`, `attack` placeholder).
- Movement System (Dijkstra): Reachable tiles are computed by movement points and terrain move cost, while blocking impassable tiles.
- Combat System: Damage is calculated by a dedicated calculator using attack, defense, and terrain bonus without mutating state.
- Turn System: `TurnManager` handles player/enemy camps, acted flags, active unit retrieval, and turn switching.
- Enemy AI: Basic decision flow returns `attack`, `move`, or `wait`; prioritizes killable targets, otherwise moves closer.
- CLI integration test: A terminal battle loop exists to verify that movement, combat, AI, and turn flow work together.
- Pygame rendering: Grid and units are rendered in pygame; player is blue and enemy is red on a tile map.
- HUD UI: A basic HUD renders current turn plus player/enemy HP via `pygame.font`.

## Gameplay (Current Prototype)

- Player can click a reachable tile to move during the player turn.
- Player can press `Space` to attack when the enemy is in range.
- Enemy acts automatically using the current AI decision logic.
- Turn flow switches between player and enemy based on action completion.
- HUD shows current turn and both camps' HP in real time.

## Next Possible Improvements

- Movement range highlight on the map.
- Unit selection system for multiple controllable units.
- Skill system integration with cooldown/effects.
- Multi-unit battle scenarios and team deployment.
- A* path visualization/animation for movement feedback.

## Notes

- Current prototype focuses on system integration rather than content depth.
- Rendering and logic are separated into dedicated modules for future expansion.
