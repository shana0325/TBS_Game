"""中文注释：根据预设批量生成统一风格的像素占位角色 PNG。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pygame

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRESET_PATH = PROJECT_ROOT / "tools" / "unit_sprite_presets.json"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "units"


def _draw_rect(surface: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
    """中文注释：用整像素矩形拼接角色局部部件。"""
    pygame.draw.rect(surface, color, rect)


def _draw_outline_rect(
    surface: pygame.Surface,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int],
    rect: tuple[int, int, int, int],
) -> None:
    """中文注释：先画描边再画主体，保持低分辨率轮廓清晰。"""
    x, y, w, h = rect
    _draw_rect(surface, outline, (x - 1, y - 1, w + 2, h + 2))
    _draw_rect(surface, fill, rect)


def _draw_human_base(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    """中文注释：绘制人形基础模板，后续叠加职业特征。"""
    outline = palette["outline"]
    skin = palette["skin"]
    primary = palette["primary"]
    secondary = palette["secondary"]

    _draw_outline_rect(surface, skin, outline, (12, 3, 8, 7))
    _draw_outline_rect(surface, primary, outline, (10, 11, 12, 10))
    _draw_outline_rect(surface, secondary, outline, (11, 21, 4, 8))
    _draw_outline_rect(surface, secondary, outline, (17, 21, 4, 8))
    _draw_outline_rect(surface, skin, outline, (7, 12, 3, 8))
    _draw_outline_rect(surface, skin, outline, (22, 12, 3, 8))


def _draw_goblin_base(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    """中文注释：绘制哥布林基础模板，体型更矮更宽。"""
    outline = palette["outline"]
    skin = palette["skin"]
    primary = palette["primary"]
    secondary = palette["secondary"]

    _draw_outline_rect(surface, skin, outline, (11, 4, 10, 7))
    _draw_outline_rect(surface, primary, outline, (9, 11, 14, 9))
    _draw_outline_rect(surface, secondary, outline, (11, 20, 4, 7))
    _draw_outline_rect(surface, secondary, outline, (17, 20, 4, 7))
    _draw_outline_rect(surface, skin, outline, (6, 12, 3, 7))
    _draw_outline_rect(surface, skin, outline, (23, 12, 3, 7))


def _draw_orc_base(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    """中文注释：绘制兽人体型模板，强调肩膀与上身厚度。"""
    outline = palette["outline"]
    skin = palette["skin"]
    primary = palette["primary"]
    secondary = palette["secondary"]

    _draw_outline_rect(surface, skin, outline, (11, 3, 10, 8))
    _draw_outline_rect(surface, primary, outline, (8, 11, 16, 11))
    _draw_outline_rect(surface, secondary, outline, (11, 22, 4, 7))
    _draw_outline_rect(surface, secondary, outline, (17, 22, 4, 7))
    _draw_outline_rect(surface, skin, outline, (5, 13, 3, 8))
    _draw_outline_rect(surface, skin, outline, (24, 13, 3, 8))


def _draw_cape(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    accent = palette["accent"]
    _draw_outline_rect(surface, accent, outline, (9, 12, 14, 13))


def _draw_headband(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    _draw_rect(surface, palette["accent"], (12, 5, 8, 2))


def _draw_sword(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    secondary = palette["secondary"]
    accent = palette["accent"]
    _draw_outline_rect(surface, secondary, outline, (23, 13, 2, 10))
    _draw_rect(surface, accent, (22, 20, 4, 2))


def _draw_helmet(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    secondary = palette["secondary"]
    _draw_outline_rect(surface, secondary, outline, (11, 2, 10, 6))
    _draw_rect(surface, outline, (15, 6, 2, 3))


def _draw_shield(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    primary = palette["primary"]
    accent = palette["accent"]
    _draw_outline_rect(surface, primary, outline, (4, 13, 5, 9))
    _draw_rect(surface, accent, (5, 16, 3, 2))


def _draw_spear(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    accent = palette["accent"]
    secondary = palette["secondary"]
    _draw_outline_rect(surface, secondary, outline, (23, 7, 1, 18))
    _draw_rect(surface, accent, (22, 5, 3, 3))


def _draw_ears(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    skin = palette["skin"]
    outline = palette["outline"]
    _draw_outline_rect(surface, skin, outline, (8, 5, 2, 4))
    _draw_outline_rect(surface, skin, outline, (22, 5, 2, 4))


def _draw_dagger(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    accent = palette["accent"]
    secondary = palette["secondary"]
    _draw_outline_rect(surface, secondary, outline, (24, 15, 1, 7))
    _draw_rect(surface, accent, (23, 19, 3, 1))


def _draw_tusks(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    accent = palette["accent"]
    _draw_rect(surface, accent, (12, 9, 2, 2))
    _draw_rect(surface, accent, (18, 9, 2, 2))


def _draw_axe(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    secondary = palette["secondary"]
    accent = palette["accent"]
    _draw_outline_rect(surface, secondary, outline, (24, 10, 1, 14))
    _draw_outline_rect(surface, accent, outline, (22, 9, 4, 4))


def _draw_shoulders(surface: pygame.Surface, palette: dict[str, tuple[int, int, int]]) -> None:
    outline = palette["outline"]
    accent = palette["accent"]
    _draw_outline_rect(surface, accent, outline, (6, 10, 5, 4))
    _draw_outline_rect(surface, accent, outline, (21, 10, 5, 4))


BASE_DRAWERS = {
    "human": _draw_human_base,
    "goblin": _draw_goblin_base,
    "orc": _draw_orc_base,
}

FEATURE_DRAWERS = {
    "cape": _draw_cape,
    "headband": _draw_headband,
    "sword": _draw_sword,
    "helmet": _draw_helmet,
    "shield": _draw_shield,
    "spear": _draw_spear,
    "ears": _draw_ears,
    "dagger": _draw_dagger,
    "tusks": _draw_tusks,
    "axe": _draw_axe,
    "shoulders": _draw_shoulders,
}


def _load_presets(path: Path) -> dict[str, dict[str, object]]:
    """中文注释：读取单位小人预设，后续新增角色只需要改 JSON。"""
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def _normalize_palette(raw_palette: dict[str, list[int]]) -> dict[str, tuple[int, int, int]]:
    return {name: tuple(values[:3]) for name, values in raw_palette.items()}


def generate_sprite(unit_id: str, preset: dict[str, object], output_dir: Path) -> Path:
    """中文注释：根据单个单位预设生成一张透明背景像素 PNG。"""
    size = int(preset.get("size", 32))
    palette = _normalize_palette(dict(preset["palette"]))
    base_name = str(preset["base"])
    features = list(preset.get("features", []))

    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    base_drawer = BASE_DRAWERS[base_name]
    base_drawer(surface, palette)

    for feature in features:
        drawer = FEATURE_DRAWERS.get(str(feature))
        if drawer is None:
            raise ValueError(f"Unknown sprite feature: {feature}")
        drawer(surface, palette)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{unit_id}.png"
    pygame.image.save(surface, str(output_path))
    return output_path


def _iter_target_units(presets: dict[str, dict[str, object]], names: Iterable[str] | None) -> Iterable[tuple[str, dict[str, object]]]:
    if not names:
        yield from presets.items()
        return

    for name in names:
        if name not in presets:
            raise KeyError(f"Unknown preset: {name}")
        yield name, presets[name]


def main() -> None:
    """中文注释：命令行入口，支持生成全部或指定单位的占位小人。"""
    parser = argparse.ArgumentParser(description="Generate placeholder pixel unit sprites.")
    parser.add_argument("--preset", default=str(PRESET_PATH), help="Path to preset json file.")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="Output directory for png files.")
    parser.add_argument("units", nargs="*", help="Optional unit ids to generate.")
    args = parser.parse_args()

    preset_path = Path(args.preset).resolve()
    output_dir = Path(args.output).resolve()

    pygame.init()
    try:
        presets = _load_presets(preset_path)
        generated_paths = [
            generate_sprite(unit_id, preset, output_dir)
            for unit_id, preset in _iter_target_units(presets, args.units)
        ]
    finally:
        pygame.quit()

    for path in generated_paths:
        print(f"generated: {path}")


if __name__ == "__main__":
    main()

