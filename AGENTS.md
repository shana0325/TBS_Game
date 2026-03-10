# AGENTS.md

This file describes the architecture, coding rules, and development workflow for AI agents (e.g., Codex) working on this repository.

The goal is to ensure that future automated code changes remain consistent with the existing architecture and design decisions.

---

# Project Overview

This repository contains a **grid-based turn-based strategy (TBS) prototype** implemented in **Python with pygame**.

The project is designed as a **clean modular architecture** separating:

* Game logic
* Rendering
* AI decision logic
* Data models
* App state flow

The current version is a **playable MVP prototype**.

Core features include:

* Tile-based map
* Unit system
* Dijkstra movement range
* Damage-based combat system
* Turn-based control
* Basic enemy AI
* Pygame rendering
* HUD display
* GameState-driven input flow

---

# Architecture Overview

The project follows a **layered architecture**.

Game rules must remain independent from UI or rendering.

```
Game Logic Layer
 ├─ Grid / Tile
 ├─ Unit System
 ├─ Movement (Dijkstra)
 ├─ Combat
 ├─ Turn Manager
 └─ Enemy AI

Application State Layer
 └─ GameState (input/action flow)

Rendering Layer
 ├─ Map Renderer
 └─ HUD

Application Layer
 └─ main.py (game loop + input)
```

Important rule:

**Game logic must not depend on pygame.**

Only the rendering, UI, and application loop should import pygame.

---

# Directory Structure

Directory structure and module responsibilities have been moved to `ARCHITECTURE.md`.

---

# Core Systems
## Grid / Tile

Defines the battlefield map.

Tile contains:

* position
* move_cost
* defense_bonus
* passable

Grid provides:

* get_tile()
* get_neighbors()

---

## Unit System

Unit is composed of:

```
UnitConfig (static attributes)
UnitState (runtime state)
Unit
```

Examples:

```
UnitConfig
  hp
  atk
  defense
  move
  range_min
  range_max
```

```
UnitState
  pos
  hp
  acted
  alive
  team_id
```

---

## Movement System

File:

```
battle/movement/pathfinder.py
```

Algorithm:

```
Dijkstra
```

Function:

```
get_reachable_tiles(grid, start_tile, move_points)
```

---

## Combat System

File:

```
battle/combat/damage_calculator.py
```

Damage formula:

```
damage = max(1, attacker.config.atk - (defender.config.defense + terrain_bonus))
```

The function **must not modify unit state**.

---

## Turn System

File:

```
battle/turn/turn_manager.py
```

Responsibilities:

* manage turn order
* switch camps
* track acted units

Turn flow:

```
Player Turn
-> Enemy Turn
-> Repeat
```

---

## Enemy AI

File:

```
ai/enemy_ai.py
```

Function:

```
choose_enemy_action()
```

Decision priority:

```
1 attack killable target
2 attack target
3 move closer to player
4 wait
```

---

## GameState System

File:

```
core/game_state.py
```

States:

* IDLE
* UNIT_SELECTED
* MOVE_MODE
* ATTACK_MODE
* ENEMY_TURN

Purpose:

* make input handling explicit by state
* keep loop flow readable and extensible

---

# Rendering Rules

All pygame rendering must stay inside:

```
render/
ui/
main.py
```

Examples:

```
render_map()
render_hud()
```

Game logic modules must remain **pygame-free**.

---

# Game Loop (main.py)

Main loop structure:

```
handle input (state-driven)
update game logic
AI decisions
render map
render HUD
```

FPS:

```
60
```

---

# Coding Guidelines

AI agents must follow these rules:

### 1. Do not mix logic and rendering

Incorrect:

```
damage calculation inside renderer
```

Correct:

```
combat module handles damage
renderer only draws results
```

---

### 2. Do not modify architecture without reason

Avoid merging modules or collapsing directories.

Keep the current structure.

---

### 3. Prefer small functions

Example:

```
render_map()
_draw_grid()
_draw_units()
```

instead of large monolithic functions.

---

### 4. Avoid hidden side effects

Functions that compute values should not modify game state.

Example:

```
calculate_damage() -> return damage
```

Not:

```
calculate_damage() modifies HP
```

---

# Current Development Status

The project currently includes:

* grid system
* unit system
* movement (Dijkstra)
* combat system
* turn manager
* enemy AI
* pygame integration prototype
* pygame rendering
* HUD UI
* GameState-based input flow

This version is considered a **playable MVP prototype**.

---

# Future Improvements

Potential next steps:

* movement range highlighting
* multiple player units
* skill system
* path animation
* improved enemy AI
* map loading
* scenario system

---

# Collaboration Preferences

- Prefer responding in Chinese unless the user explicitly requests another language.
- Prefer adding new feature modules instead of changing existing behavior directly, unless refactor/fix is explicitly requested.
- Implementing module functionality must include at least Chinese comments describing the module functionality.

---

# Instructions for AI Agents

When implementing new features:

1. Follow existing architecture
2. Avoid introducing new dependencies
3. Keep game logic independent from pygame
4. Keep input flow controlled by GameState when extending main loop
5. Maintain modular structure

If unsure, extend existing systems rather than rewriting them.


