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


def get_path_to_tile(
    grid: Grid,
    start_tile: Tile,
    goal_tile: Tile,
    move_points: int,
) -> list[Tile]:
    """使用 Dijkstra 计算从起点到目标格子的最短路径（仅用于预览显示）。"""
    if move_points < 0:
        return []
    if not start_tile.passable or not goal_tile.passable:
        return []

    start_key = (start_tile.x, start_tile.y)
    goal_key = (goal_tile.x, goal_tile.y)

    distances: dict[tuple[int, int], int] = {start_key: 0}
    previous: dict[tuple[int, int], tuple[int, int] | None] = {start_key: None}
    heap: list[tuple[int, int, int]] = [(0, start_tile.x, start_tile.y)]

    while heap:
        current_cost, x, y = heappop(heap)
        key = (x, y)

        if current_cost > distances.get(key, inf):
            continue
        if current_cost > move_points:
            continue
        if key == goal_key:
            break

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
            previous[n_key] = key
            heappush(heap, (next_cost, neighbor.x, neighbor.y))

    if goal_key not in previous:
        return []

    path_keys: list[tuple[int, int]] = []
    node: tuple[int, int] | None = goal_key
    while node is not None:
        path_keys.append(node)
        node = previous.get(node)
    path_keys.reverse()

    path_tiles: list[Tile] = []
    for x, y in path_keys:
        tile = grid.get_tile(x, y)
        if tile is not None:
            path_tiles.append(tile)

    return path_tiles
