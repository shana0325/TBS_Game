# AGENTS.md

Local rules for `game/player/`.

## Responsibility

This directory owns persistent player-side data and growth logic.

It should contain:

- player-owned unit data
- EXP and level progression
- stat point and skill point spending
- learned/equipped skill state
- roster load/save behavior

## Design Rules

- Persistent progression data belongs here, not in battle runtime classes.
- `PlayerUnitData` is the source of truth for owned-unit growth state.
- `ProgressionSystem` applies growth rules.
- `PlayerArmy` loads, exposes, mutates, and saves roster data.

## Integration Rule

Battle units should be built from:

- template data from `data/unit/units.json`
- persistent player data from `data/player/player_roster.json`

That assembly happens in `game/levels/systems/spawn_system.py`.

Do not bypass that layering by hardcoding progression directly into `UnitConfig` creation elsewhere.

## Constraints

- Keep modules pygame-free.
- Favor data-driven fields that can be serialized to JSON cleanly.
- If adding new persistent progression fields, update both model normalization and serialization.
