"""Сервис простого rate-limit для защиты от спама."""

from __future__ import annotations

import time


class RateLimitService:
    """Ограничивает частоту запросов от одного пользователя."""

    def __init__(self, min_interval_seconds: float = 1.0) -> None:
        self._min_interval_seconds = min_interval_seconds
        self._last_seen_at: dict[int, float] = {}

    def is_allowed(self, user_id: int) -> bool:
        """Проверяет, можно ли принять новое сообщение пользователя прямо сейчас."""
        now = time.monotonic()
        last_seen = self._last_seen_at.get(user_id)
        if last_seen is not None and now - last_seen < self._min_interval_seconds:
            return False

        self._last_seen_at[user_id] = now
        return True
