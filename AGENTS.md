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

Rendering Layer
 ├─ Map Renderer
 └─ HUD

Application Layer
 └─ main.py (game loop + input)
```

Important rule:

**Game logic must not depend on pygame.**

Only the rendering and UI layers should import pygame.

---

# Directory Structure

```
game/
  core/
  battle/
    combat/
    movement/
    turn/
  entity/
  ai/
  render/
  ui/
  data/
  save/

assets/

docs/

main.py
```

Responsibilities:

### battle/

Contains gameplay systems.

Examples:

* movement/pathfinder.py -> movement logic
* combat/damage_calculator.py -> combat math
* turn/turn_manager.py -> turn control

### entity/

Contains game objects.

Examples:

* Unit
* Skill
* Buff

### ai/

Contains enemy decision logic.

Example:

enemy_ai.py -> choose_enemy_action()

### render/

Handles drawing the map and units.

Uses pygame.

### ui/

HUD and interface elements.

Uses pygame.

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
handle input
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
draw_grid()
draw_units()
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
* CLI validation prototype
* pygame rendering
* HUD UI

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

# Instructions for AI Agents

When implementing new features:

1. Follow existing architecture
2. Avoid introducing new dependencies
3. Keep game logic independent from pygame
4. Maintain modular structure

If unsure, extend existing systems rather than rewriting them.
