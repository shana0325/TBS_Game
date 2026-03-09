# Development Log

## Stage 1 - Project Skeleton
- Created base folder structure for game, assets, and docs.
- Added minimal module scaffolding files and package init files.

## Stage 2 - System Design Document
- Added initial system design document under `docs/`.
- Refined and aligned project architecture with `tbs_game_system_design_v2.md`.

## Stage 3 - Grid / Tile System
- Implemented `Tile` model with movement and terrain fields.
- Implemented `Grid` storage, tile access, and passable neighbor query.

## Stage 4 - Unit System
- Implemented `UnitConfig`, `UnitState`, and `Unit`.
- Added movement and damage state operations with pure logic structure.

## Stage 5 - Movement System (Dijkstra)
- Implemented reachable-tile calculation using Dijkstra.
- Applied `move_cost` and blocked `passable=False` tiles.

## Stage 6 - Combat System
- Implemented `calculate_damage(attacker, defender, terrain_bonus)`.
- Kept calculation pure with no state mutation.

## Stage 7 - Turn System
- Implemented `TurnManager` for camp switching and acted-state management.
- Added active unit query and turn-finished check.

## Stage 8 - Enemy AI
- Implemented `choose_enemy_action(unit, grid, units)` decision flow.
- Added attack priority (killable target), move-toward-target, and wait fallback.

## Stage 9 - CLI Integration Test
- Integrated systems in CLI battle loop for end-to-end validation.
- Verified player action, enemy AI action, and turn switching flow.

## Stage 10 - Pygame Rendering
- Implemented `map_renderer` with grid and unit rendering.
- Integrated pygame main loop and per-frame rendering refresh.

## Stage 11 - HUD
- Added HUD text rendering with `pygame.font`.
- Displayed current turn plus player/enemy HP.
