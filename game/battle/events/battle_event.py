"""战斗事件模型：统一事件载体。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BattleEvent:
    """Battle event payload used by EventSystem."""

    event_type: str
    source: object | None = None
    target: object | None = None
    data: dict[str, Any] = field(default_factory=dict)
