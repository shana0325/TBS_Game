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


class DualGrid:
    """双战场网格：由左右两个独立子战场组成，中间保留不可通行空区。"""

    def __init__(self, side_width: int = 4, height: int = 3, gap_width: int = 2) -> None:
        if side_width <= 0 or height <= 0:
            raise ValueError("side_width and height must be positive integers")
        if gap_width <= 0:
            raise ValueError("gap_width must be a positive integer")

        self.side_width = side_width
        self.height = height
        self.gap_width = gap_width

        self.player_grid = Grid(side_width, height)
        self.enemy_grid = Grid(side_width, height)

        self.player_offset_x = 0
        self.enemy_offset_x = side_width + gap_width
        self.width = side_width * 2 + gap_width

        self._tiles: dict[tuple[int, int], Tile] = {}
        self._build_tiles()

    def get_tile(self, x: int, y: int) -> Tile | None:
        """返回全局坐标的 tile；中间空区与越界坐标返回 None。"""
        if y < 0 or y >= self.height:
            return None
        return self._tiles.get((x, y))

    def get_neighbors(self, tile: Tile) -> list[Tile]:
        """返回上下左右可通行邻居，不会跨越中间空区。"""
        neighbors: list[Tile] = []
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dx, dy in directions:
            nx, ny = tile.x + dx, tile.y + dy
            neighbor = self.get_tile(nx, ny)
            if neighbor is not None and neighbor.passable:
                neighbors.append(neighbor)

        return neighbors

    def get_side_for_position(self, x: int, y: int) -> str | None:
        """根据全局坐标返回所属战场：player / enemy / None。"""
        if y < 0 or y >= self.height:
            return None
        if self.player_offset_x <= x < self.player_offset_x + self.side_width:
            return "player"
        if self.enemy_offset_x <= x < self.enemy_offset_x + self.side_width:
            return "enemy"
        return None

    def _build_tiles(self) -> None:
        # 中文注释：将左右子战场的局部坐标映射到统一全局坐标，供渲染与路径逻辑复用。
        self._tiles.clear()

        for y in range(self.height):
            for local_x in range(self.side_width):
                player_tile = self.player_grid.get_tile(local_x, y)
                if player_tile is not None:
                    gx = self.player_offset_x + local_x
                    self._tiles[(gx, y)] = Tile(
                        x=gx,
                        y=y,
                        move_cost=player_tile.move_cost,
                        defense_bonus=player_tile.defense_bonus,
                        passable=player_tile.passable,
                    )

                enemy_tile = self.enemy_grid.get_tile(local_x, y)
                if enemy_tile is not None:
                    gx = self.enemy_offset_x + local_x
                    self._tiles[(gx, y)] = Tile(
                        x=gx,
                        y=y,
                        move_cost=enemy_tile.move_cost,
                        defense_bonus=enemy_tile.defense_bonus,
                        passable=enemy_tile.passable,
                    )

