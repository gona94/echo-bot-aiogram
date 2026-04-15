"""Тесты для сервиса ограничения частоты запросов."""

from src.bot.services.rate_limit_service import RateLimitService


def test_rate_limit_blocks_second_immediate_message() -> None:
    """Второе сообщение подряд должно блокироваться при коротком интервале."""
    service = RateLimitService(min_interval_seconds=10.0)

    assert service.is_allowed(1001)
    assert not service.is_allowed(1001)


def test_rate_limit_is_independent_for_different_users() -> None:
    """Ограничение одного пользователя не должно блокировать другого."""
    service = RateLimitService(min_interval_seconds=10.0)

    assert service.is_allowed(1)
    assert service.is_allowed(2)
