"""Тесты для сервиса фильтрации устаревших сообщений."""

from datetime import UTC, datetime, timedelta

from src.bot.services.stale_message_service import StaleMessageService


def test_is_stale_returns_true_for_old_message() -> None:
    """Сообщение старше порога должно считаться устаревшим."""
    service = StaleMessageService(max_age_seconds=20)
    now = datetime(2026, 4, 15, 20, 0, 0, tzinfo=UTC)
    old_message_time = now - timedelta(seconds=25)

    assert service.is_stale(old_message_time, now=now) is True


def test_is_stale_returns_false_for_recent_message() -> None:
    """Свежие сообщения не должны отфильтровываться."""
    service = StaleMessageService(max_age_seconds=20)
    now = datetime(2026, 4, 15, 20, 0, 0, tzinfo=UTC)
    recent_message_time = now - timedelta(seconds=5)

    assert service.is_stale(recent_message_time, now=now) is False
