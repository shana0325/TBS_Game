# AGENTS.md

Local rules for `game/ui/`.

## Responsibility

This directory contains battle UI panels, menus, and reusable UI helpers.

It should handle:

- panel drawing
- menu drawing
- scroll behavior
- battle log presentation
- unit info presentation

It should not contain:

- combat rules
- movement rules
- progression logic
- battle state mutation beyond UI input routing

## Design Rules

- `ui_system.py` composes battle UI regions.
- `scrollable_list.py` is the shared scrolling primitive for overflow-prone list UIs.
- Prefer reusing `ScrollableList` instead of duplicating scroll math.
- Keep layout responsive to screen size.
- UI rendering can depend on pygame, but logic ownership should stay elsewhere.

## Current Style Constraints

- Battle layout semantics remain `11114 / 11114 / 22334`.
- Battle log is a dedicated right-side column.
- Long text should wrap or scroll instead of overflowing out of panel bounds.
- Mouse-first UI is preferred where interaction density is high.

## Extension Guidance

- new list-like panel -> use `ScrollableList`
- new battle-side panel -> integrate through `UISystem`
- new modal/selection list -> keep drawing and input mapping here, not in battle logic
