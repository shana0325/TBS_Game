"""Skill entity definition."""

from dataclasses import dataclass


@dataclass
class Skill:
    """Minimal skill model."""

    skill_id: str
