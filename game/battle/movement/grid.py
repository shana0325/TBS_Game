"""Grid container for tile-based battle maps."""

from __future__ import annotations

from .tile import Tile


class Grid:
    """Stores 2D tiles and exposes neighbor queries."""

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")

        self.width = width
        self.height = height
        self._tiles: list[list[Tile]] = [
            [Tile(x=x, y=y) for x in range(width)]
            for y in range(height)
        ]

    def get_tile(self, x: int, y: int) -> Tile | None:
        """Return tile at (x, y), or None when out of bounds."""
        if not self._in_bounds(x, y):
            return None
        return self._tiles[y][x]

    def get_neighbors(self, tile: Tile) -> list[Tile]:
        """Return passable orthogonal neighbors (up/down/left/right)."""
        neighbors: list[Tile] = []
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dx, dy in directions:
            nx, ny = tile.x + dx, tile.y + dy
            neighbor = self.get_tile(nx, ny)
            if neighbor is not None and neighbor.passable:
                neighbors.append(neighbor)

        return neighbors

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
