# AGENTS.md

Local rules for `game/battle/`.

## Responsibility

This directory contains battle runtime logic only.

It should handle:

- movement
- combat resolution support
- skill effect execution
- combat event dispatch
- turn flow

It must not handle:

- pygame drawing
- screen flow
- menu layout
- persistent player roster editing

## Design Rules

- `combat/damage_calculator.py` must stay calculation-only.
- `combat/combat_system.py` is the correct place for attack-range and combat coordination logic.
- `effects/` executes skill effects. Add new effect types here.
- `events/` broadcasts battle events. Trigger-style logic should react through events instead of being scattered.
- `turn/turn_manager.py` owns turn transitions and turn-based buff/event timing.
- `movement/` stays pathing/range focused and should not absorb unrelated combat rules.

## Extension Guidance

When adding a new mechanic:

- direct effect from a skill -> `effects/`
- event-driven reaction -> `events/` + `entity/buff.py`
- pure calculation -> `damage_calculator.py`
- battle-state coordination -> `combat_system.py` or `turn_manager.py`

## Constraints

- Keep modules pygame-free.
- Prefer adding new effect/event modules instead of bloating existing files.
- Do not move UI or logging presentation rules into battle logic.
