"""Сервис фильтрации устаревших входящих сообщений."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


class StaleMessageService:
    """Определяет, следует ли игнорировать слишком старое сообщение."""

    def __init__(self, max_age_seconds: int = 20) -> None:
        self._max_age = timedelta(seconds=max_age_seconds)

    def is_stale(self, message_date: datetime, now: datetime | None = None) -> bool:
        """Возвращает True, если сообщение старше допустимого порога."""
        current_time = now or datetime.now(UTC)
        normalized_message_date = message_date

        if normalized_message_date.tzinfo is None:
            normalized_message_date = normalized_message_date.replace(tzinfo=UTC)

        return current_time - normalized_message_date > self._max_age
