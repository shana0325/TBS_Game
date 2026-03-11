# AGENTS.md

This file describes the architecture, coding rules, and development workflow for AI agents working on this repository.

The goal is to keep future automated changes aligned with the current project structure, gameplay rules, and collaboration preferences.

---

# Project Overview

This repository contains a **grid-based turn-based strategy (TBS) prototype** implemented in **Python with pygame**.

The project is no longer just a battle sandbox. It now includes:

- battle runtime systems
- screen flow outside battle
- data-driven unit / skill / buff config
- persistent player roster and progression
- pre-battle deployment and progression UI
- event-driven combat triggers

Current flow:

```text
Main Menu
-> Level Select
-> Progression (optional)
-> Deployment
-> Battle
-> Result
```

This is still an MVP, but it is now a **playable vertical slice prototype** rather than only a combat sandbox.

---

# Architectural Principles

## 1. Keep logic and pygame separated

Game logic must remain independent from pygame.

Only these layers should import pygame:

- `game/screens/`
- `game/render/`
- `game/ui/`
- `main.py`
- `game/core/game.py` as battle runtime integration layer

Pure logic modules such as:

- `battle/`
- `entity/`
- `player/`
- `levels/`
- `data/`

must stay pygame-free.

## 2. Prefer extension over rewriting

When adding features:

- prefer new modules
- reuse current systems
- avoid collapsing layers
- avoid rewriting working modules unless refactor/fix is explicitly needed

## 3. Data-driven first

The project already uses JSON for:

- units
- skills
- buffs
- player roster

New gameplay content should prefer config-driven design before hardcoding new branches into logic.

## 4. Runtime responsibilities are split

Use the correct layer for the correct responsibility:

- `screens/`: app flow outside battle
- `core/game.py`: battle runtime orchestration
- `state/`: player battle input state flow
- `battle/effects/`: skill effect execution
- `battle/events/`: combat event dispatch
- `entity/buff.py`: buff behavior and trigger response
- `player/`: persistent roster and progression
- `ui/`: panel/menu drawing and input helpers

---

# Current Core Runtime

Battle runtime layering is:

```text
Skill
-> EffectSystem
-> Effect modules
-> CombatSystem / TurnManager
-> EventSystem
-> Buff / Trigger logic
```

Important consequence:

- not every skill effect goes through `CombatSystem`
- `CombatSystem` is for attack/range/combat-event-related flow
- `TurnManager` is also an event source
- `Buff` trigger logic should react through `EventSystem`

Do not reintroduce ad-hoc trigger logic into unrelated modules if it can be routed through events cleanly.

---

# Project Status Summary

The current codebase includes:

- Dual battlefield map structure
- Unit, skill, buff, and combat systems
- Dijkstra movement and path preview
- Turn manager with multi-unit support
- Enemy AI turn execution
- Deployment phase
- Data-driven skill effects and buffs
- Event system for combat triggers
- Player roster and progression backend
- Progression screen before battle
- Shared scrollable UI behavior
- Battle log with wrapping, color, and scrolling

This means AI agents should assume the project already supports:

- multiple units per camp
- skill selection and execution
- buff lifecycle and trigger-style effects
- persistent player-owned unit data
- pre-battle preparation flow

Do not implement new features as if this were still a one-unit prototype.

---

# Files To Read First

When making changes, start with these files:

- `ARCHITECTURE.md`
- `README.md`
- `docs/dev_log.md`
- `game/core/game.py`
- `game/screens/screen_manager.py`

Then read the local subsystem files you are changing.

---

# Subsystem Rules

## Battle

Relevant directories:

- `game/battle/`
- `game/entity/`
- `game/state/`

Rules:

- keep `damage_calculator.py` calculation-only
- keep attack range / combat coordination in `combat_system.py`
- keep skill behavior in `effects/`
- keep combat triggers in `events/`
- keep buff state/behavior in `entity/buff.py`
- do not move rendering concerns into battle logic

## Screens

Relevant directory:

- `game/screens/`

Rules:

- screens manage application flow outside battle
- `BattleScreen` prepares battle inputs, then hands runtime to `Game`
- do not duplicate battle logic inside screen classes
- resizing behavior must remain supported

## Progression

Relevant directory:

- `game/player/`

Rules:

- persistent player-owned data belongs here, not in `UnitConfig`
- battle units are assembled from templates plus roster/progression data by `SpawnSystem`
- do not treat `player_roster.json` as a raw battle unit list; it is persistent ownership/progression data

## UI

Relevant directory:

- `game/ui/`

Rules:

- `UISystem` owns battle panel composition
- use `ScrollableList` for new overflow-prone list UIs instead of inventing one-off scroll math
- keep layout responsive to screen size
- keep UI behavior separate from game rules

---

# Collaboration Preferences

- Prefer responding in Chinese unless the user explicitly requests another language.
- Prefer adding new feature modules instead of changing existing behavior directly, unless refactor/fix is explicitly requested.
- Implementing module functionality must include at least Chinese comments describing the module functionality.

---

# Coding Guidelines

## 1. Preserve architecture

Do not merge unrelated layers just because it is faster.

## 2. Small focused functions

Prefer small composable functions over monolithic methods.

## 3. Avoid hidden side effects

If a function computes a value, it should return the value rather than silently mutating unrelated state.

## 4. Keep new code consistent with current naming

Use current module vocabulary:

- `PlayerArmy`
- `ProgressionSystem`
- `SpawnSystem`
- `EffectSystem`
- `EventSystem`
- `ScrollableList`

Avoid introducing parallel abstractions with overlapping meaning unless there is a strong reason.

## 5. Respect current UI model

Current battle layout is:

```text
11114
11114
22334
```

Meaning:

- `1` battlefield
- `2` unit info
- `3` action / skill area
- `4` battle log

Do not break this layout unintentionally when editing battle UI.

---

# When Extending Features

Use these preferred extension paths:

- new skill behavior -> `battle/effects/` or `entity/buff.py`
- new combat trigger -> `battle/events/` + `entity/buff.py`
- new persistent growth feature -> `player/`
- new pre/post-battle app flow -> `screens/`
- new battle panel/list UI -> `ui/`
- new battle rendering overlay -> `render/`

If unsure, extend existing systems rather than rewriting them.
