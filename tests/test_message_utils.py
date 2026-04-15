"""Тесты для утилит обработки сообщений."""

from src.bot.utils.message_utils import is_text_message, parse_integer_text


def test_is_text_message_returns_true_for_regular_text() -> None:
    """Обычный текст должен считаться валидным."""
    assert is_text_message("Привет")


def test_is_text_message_returns_false_for_none() -> None:
    """None не должен считаться текстом."""
    assert not is_text_message(None)


def test_is_text_message_returns_false_for_whitespace() -> None:
    """Строка из пробелов не должна считаться текстом."""
    assert not is_text_message("   ")


def test_parse_integer_text_returns_int_for_numeric_text() -> None:
    """Проверяет распознавание целого числа."""
    assert parse_integer_text("123") == 123


def test_parse_integer_text_returns_none_for_non_numeric_text() -> None:
    """Нечисловая строка не должна распознаваться как число."""
    assert parse_integer_text("Привет 123") is None
