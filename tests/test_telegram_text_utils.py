"""Тесты для утилит Telegram-текста."""

from src.bot.utils.telegram_text_utils import trim_for_telegram


def test_trim_for_telegram_keeps_short_text() -> None:
    """Короткий текст не должен изменяться."""
    assert trim_for_telegram("Привет", limit=20) == "Привет"


def test_trim_for_telegram_truncates_long_text() -> None:
    """Длинный текст должен обрезаться до заданного лимита."""
    result = trim_for_telegram("x" * 5000, limit=100)
    assert len(result) == 100
    assert result.endswith("[Ответ обрезан из-за ограничения Telegram]")


def test_trim_for_telegram_handles_tiny_limit() -> None:
    """Если лимит очень маленький, возвращается обрезанная пометка."""
    result = trim_for_telegram("x" * 100, limit=10)
    assert len(result) == 10
