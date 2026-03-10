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

## Stage 12 - Move Range Highlight & Path Preview
- Added move range highlight rendering with blue tile outlines.
- Added hover path preview rendering using pathfinding result from current tile to hovered reachable tile.

## Stage 13 - Action Menu
- Added `ActionMenu` UI module with Move / Attack / Wait options.
- Integrated menu rendering and click handling for state transitions in player turn.

## Stage 14 - Attack Range Highlight
- Added attack range highlight renderer with red tile outlines.
- Integrated attack-mode range visualization in pygame render loop.

## Stage 15 - Game Class Refactor
- Added `game/core/game.py` with `Game` class to encapsulate event handling, update, and rendering.
- Simplified `main.py` to pygame initialization, game instance creation, and loop execution only.

## Stage 16 - Dual Battlefield System
- Reworked battlefield into two independent 3-row x 4-column grids with a middle gap.
- Updated rendering and movement constraints so units cannot move across battlefields.


## Stage 17 - UI Panel Layout
- Increased window height and split screen into Battlefield + bottom UI Panel.
- Moved Action Menu and HUD rendering into the UI Panel area.

## Stage 18 - Cross-Battlefield Attack Range Rule
- Updated attack range check to use distance-to-middle sum across battlefields and ignore Y-axis offset.
- Synced player attack check, enemy AI attack decision, and attack highlight rendering rule.

## Stage 19 - Player Controller Refactor
- Added `game/controllers/player_controller.py` and moved player turn input/move/attack logic into `PlayerController.update()`.
- `Game` now delegates player-turn behavior to controller while preserving existing gameplay behavior.

## Stage 20 - Enemy Controller Refactor
- Added `game/controllers/enemy_controller.py` and moved enemy turn AI action execution into `EnemyController.update()`.
- `Game` now delegates enemy-turn behavior to controller while preserving existing gameplay behavior.

## Stage 21 - Combat Range Refactor
- Added `game/battle/combat/combat_system.py` with `CombatSystem` for attack range/distance checks.
- `Game` and `PlayerController` now use `CombatSystem`; `damage_calculator.py` remains damage-only.

## Stage 22 - Highlight System Refactor
- Added `game/battle/combat/highlight_system.py` to centralize move/path/attack highlight tile calculations.
- `Game` now delegates highlight tile computation to `HighlightSystem` while renderers remain unchanged.

## Stage 23 - State Pattern (Player States)
- Added `game/state/` with `GameStateBase`, `IdleState`, `MoveState`, and `AttackState`.
- `Game` now keeps `current_state` and delegates player input handling via `current_state.handle_input(...)`.

## Stage 24 - UI System Refactor
- Added `game/ui/ui_system.py` to centralize UI Panel, HUD, and ActionMenu rendering.
- `Game.render()` now delegates UI drawing to `UISystem.render(...)` without behavior changes.

## Stage 25 - Dual Battlefield UI Layout
- Redesigned layout into three regions: Battlefield Area (top), Unit Info Panel (bottom-left), and Action Panel (bottom-right).
- Added centered battlefield rendering with left/right grid borders, visible gap area, and non-overlapping bottom UI system.

## Stage 26 - Multi-Unit Support
- Expanded game initialization to spawn multiple player and enemy units, and unified unit list management.
- Updated state-driven selection/action flow to target selectable unacted player units; enemy controller now executes all enemy units sequentially per enemy turn.

## Stage 27 - Level / Scenario / SpawnSystem
- Added `level` (map/spawn data), `scenario` (battle composition/rules), and `spawn_system` (unit instantiation) modules with clear responsibilities.
- Updated `Game` initialization to load level/scenario data and spawn units through `SpawnSystem` without changing combat/movement/AI runtime logic.
