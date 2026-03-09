"""Pathfinding helpers for movement range calculation."""

from __future__ import annotations

from heapq import heappop, heappush
from math import inf

from .grid import Grid
from .tile import Tile


def get_reachable_tiles(grid: Grid, start_tile: Tile, move_points: int) -> list[Tile]:
    """Return all tiles reachable within move points using Dijkstra."""
    if move_points < 0:
        return []
    if not start_tile.passable:
        return []

    start_key = (start_tile.x, start_tile.y)
    distances: dict[tuple[int, int], int] = {start_key: 0}
    heap: list[tuple[int, int, int]] = [(0, start_tile.x, start_tile.y)]

    while heap:
        current_cost, x, y = heappop(heap)
        key = (x, y)

        if current_cost > distances.get(key, inf):
            continue
        if current_cost > move_points:
            continue

        current_tile = grid.get_tile(x, y)
        if current_tile is None:
            continue

        for neighbor in grid.get_neighbors(current_tile):
            step_cost = max(0, neighbor.move_cost)
            next_cost = current_cost + step_cost
            n_key = (neighbor.x, neighbor.y)

            if next_cost > move_points:
                continue
            if next_cost >= distances.get(n_key, inf):
                continue

            distances[n_key] = next_cost
            heappush(heap, (next_cost, neighbor.x, neighbor.y))

    reachable_tiles: list[Tile] = []
    for x, y in distances:
        tile = grid.get_tile(x, y)
        if tile is not None:
            reachable_tiles.append(tile)

    return reachable_tiles
