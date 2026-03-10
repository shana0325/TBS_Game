"""战斗日志模块：维护战斗过程中的文本日志。"""

from __future__ import annotations


class BattleLog:
    """保存并管理战斗日志消息。"""

    def __init__(self, max_lines: int = 100) -> None:
        # 中文注释：messages 保存按时间顺序的日志文本（原始数据）。
        self.messages: list[str] = []
        # 中文注释：entries 保存每条日志的元信息，供 UI 过滤和着色。
        self.entries: list[dict[str, str]] = []
        self.max_lines = max_lines

    def add(self, message: str, category: str = "info", side: str = "neutral") -> None:
        """添加一条日志，超出上限时移除最旧项。"""
        self.messages.append(message)
        self.entries.append(
            {
                "text": message,
                "category": category,
                "side": side,
            }
        )

        if len(self.messages) > self.max_lines:
            overflow = len(self.messages) - self.max_lines
            self.messages = self.messages[overflow:]
            self.entries = self.entries[overflow:]

    def get_recent(self, n: int) -> list[str]:
        """返回最近 n 条日志文本。"""
        if n <= 0:
            return []
        return self.messages[-n:]

    def get_recent_entries(self, n: int) -> list[dict[str, str]]:
        """返回最近 n 条带元信息日志。"""
        if n <= 0:
            return []
        return self.entries[-n:]

    def clear(self) -> None:
        """清空日志。"""
        self.messages.clear()
        self.entries.clear()
