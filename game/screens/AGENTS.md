# AGENTS.md

Local rules for `game/screens/`.

## Responsibility

This directory manages application flow outside battle.

Current flow is:

```text
Main Menu
-> Level Select
-> Progression (optional)
-> Deployment
-> Battle
-> Result
```

## Design Rules

- Each screen should stay focused on one phase of flow.
- `BattleScreen` prepares level/scenario/grid/units, then hands control to `game/core/game.py`.
- Do not duplicate battle runtime logic inside screen classes.
- Keep resize handling working when editing screens.

## Current Key Screens

- `level_select_screen.py`: entry point to progression or deployment
- `progression_screen.py`: pre-battle growth UI
- `deployment_screen.py`: placement before battle starts
- `battle_screen.py`: battle setup + result handoff
- `result_screen.py`: post-battle exit point

## Extension Guidance

- new app phase -> new screen
- pre-battle setup -> usually `screens/` plus `player/` or `levels/`
- post-battle reward flow -> prefer `result_screen.py` or a new screen, not `Game`

## Constraints

- Screens can use pygame.
- Keep gameplay rules in logic modules, not screen methods.
- Avoid turning screens into large god-objects.
