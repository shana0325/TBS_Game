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
- `Game` and controllers now use `CombatSystem`; `damage_calculator.py` remains damage-only.

## Stage 22 - Highlight System Refactor
- Added `game/battle/combat/highlight_system.py` to centralize move/path/attack highlight tile calculations.
- `Game` now delegates highlight tile computation to `HighlightSystem` while renderers remain unchanged.

## Stage 23 - State Pattern (Player States)
- Added `game/state/` with `GameStateBase`, `IdleState`, `MoveState`, and `AttackState`.
- `Game` now keeps `current_state` and delegates player input handling via `current_state.handle_input(...)`.

## Stage 24 - UI System Refactor
- Added `game/ui/ui_system.py` to centralize UI Panel, ActionMenu, Unit Info, and Battle Log rendering.
- `Game.render()` now delegates battle UI drawing to `UISystem.render(...)`.

## Stage 25 - Dual Battlefield UI Layout
- Redesigned layout into Battlefield Area, Unit Info Panel, Action Panel, and right-side Battle Log column.
- Added centered battlefield rendering, gap visuals, and non-overlapping panel layout.

## Stage 26 - Multi-Unit Support
- Expanded initialization to spawn multiple player and enemy units, and unified unit list management.
- Updated selection/action flow to support view-only selection of acted/enemy units for info display.

## Stage 27 - Level / Scenario / SpawnSystem
- Added `level` (map/spawn data), `scenario` (enemy composition/rules), and `spawn_system` (unit instantiation) modules.
- Updated battle initialization to load level/scenario data and spawn units through `SpawnSystem`.

## Stage 28 - Screen System
- Added `ScreenBase`, `ScreenManager`, and `MainMenu / LevelSelect / Battle / Result` screens to manage non-battle flow.
- `BattleScreen` now loads data, calls `SpawnSystem`, and creates `Game` while preserving battle runtime systems.

## Stage 29 - Deployment Phase
- Added `DeploymentScreen` between LevelSelect and Battle, with deployment-zone highlight and roster-based unit placement.
- Updated level/scenario/spawn flow so player deployment is resolved before battle starts.

## Stage 30 - PlayerArmy Global Roster
- Added global player roster data at `data/player/player_roster.json` to support persistent unit metadata.
- Added `game/player/player_army.py` and switched deployment/battle flow to read player units from `PlayerArmy`.

## Stage 31 - Effect / Buff Foundation
- Refactored skills to use `EffectSystem` and added effect modules for damage, heal, buff, summon, and revive.
- Added `Buff` entity, unit buff containers, buff-aware damage calculation, and timed buff lifecycle.

## Stage 32 - Advanced Combat Events
- Added `EventSystem`, `BattleEvent`, and event type constants for `on_hit`, `on_kill`, `on_turn_start`, and `on_turn_end`.
- Routed trigger-style combat logic through events and migrated counter-like reactions to event-driven flow.

## Stage 33 - Progression Backend
- Added `PlayerUnitData` and `ProgressionSystem` to support EXP gain, level-up, stat points, skill points, and persistent skill loadout data.
- Extended `SpawnSystem` to apply `allocated_stats` and merge template / learned / equipped / extra skills into battle units.

## Stage 34 - Pre-Battle Progression Screen
- Added `ProgressionScreen` entry from `LevelSelect`, allowing players to inspect roster growth before deployment.
- Added fixed victory EXP reward flow in `BattleScreen`, with progression data written back to `player_roster.json`.

## Stage 35 - Unified Scrollable UI
- Added reusable `ScrollableList` component to unify scroll state, visible slice calculation, and scrollbar rendering.
- Applied shared scrolling behavior to `ProgressionScreen` and `BattleLogPanel`, including mouse wheel scrolling and overflow-safe rendering.

## Stage 36 - Mouse-Driven Progression UI
- Reworked `ProgressionScreen` to support mouse-first interaction for unit selection, stat allocation, skill learning, and skill equip.
- Added clickable `+` stat buttons, `Learn/Equip` buttons, and `Back` button while retaining keyboard fallback.

## Stage 37 - Font and i18n Infrastructure
- Added unified font management with `assets/fonts/LXGWWenKai-Light.ttf` and `game/ui/font_manager.py`, so UI modules no longer load fonts independently.
- Split text resources into `game/core/i18n/zh_cn.py` and `game/core/i18n/en_us.py`, kept `game/core/texts.py` as a compatibility facade, and added runtime language switching via `F2` plus `TBS_LANG`.
- Extended text entry points with skill descriptions, buff descriptions, and status texts, then connected them to `ProgressionScreen` and `UnitInfoPanel`.

## Stage 38 - Equipment System
- Added `data/equipment/equipments.json`, `Equipment` entity, and `EquipmentSystem` for slot validation, modifier aggregation, and granted skills.
- Upgraded player roster equipment data to `weapon / offhand / accessory` slots and applied equipment effects in `SpawnSystem`.

## Stage 39 - Progression Tabs Refactor
- Split the old crowded growth UI into `属性 / 技能 / 装备` three-tab panels.
- Extracted `ProgressionTabs`, `ProgressionStatPanel`, `ProgressionSkillPanel`, and `ProgressionEquipmentPanel`, shrinking `ProgressionScreen` into a dispatcher-style screen.

## Stage 40 - Character Select Progression Flow
- Added `ProgressionCharacterSelectScreen` as a pre-growth role selection step with horizontal character cards.
- Converted `ProgressionScreen` into a single-character growth screen and added `ProgressionUnitSummaryPanel` for the left-side character summary.


## Stage 41 - Placeholder Unit Sprite Generator
- Added `tools/generate_unit_sprites.py` and `tools/unit_sprite_presets.json` to batch-generate consistent 32x32 placeholder unit sprites.
- Added `tools/generate_unit_sprites.md` to document sprite generation flow, preset structure, and future feature/base extension steps.
